import itertools
import logging
import socket
from typing import List

from common.network.network_range import InvalidNetworkRangeError, NetworkRange
from infection_monkey.network import NetworkAddress, NetworkInterface

logger = logging.getLogger(__name__)


def compile_scan_target_list(
    local_network_interfaces: List[NetworkInterface],
    ranges_to_scan: List[str],
    inaccessible_subnets: List[str],
    blocklisted_ips: List[str],
    enable_local_network_scan: bool,
) -> List[NetworkAddress]:
    scan_targets = _get_ips_from_ranges_to_scan(ranges_to_scan)

    if enable_local_network_scan:
        scan_targets.extend(_get_ips_to_scan_from_local_interface(local_network_interfaces))

    if inaccessible_subnets:
        inaccessible_subnets = _get_segmentation_check_targets(
            inaccessible_subnets, local_network_interfaces
        )
        scan_targets.extend(inaccessible_subnets)

    scan_targets = _remove_interface_ips(scan_targets, local_network_interfaces)
    scan_targets = _remove_blocklisted_ips(scan_targets, blocklisted_ips)
    scan_targets = _remove_redundant_targets(scan_targets)
    scan_targets.sort(key=lambda network_address: socket.inet_aton(network_address.ip))

    return scan_targets


def _remove_redundant_targets(targets: List[NetworkAddress]) -> List[NetworkAddress]:
    reverse_dns = {}
    for target in targets:
        domain_name = target.domain
        ip = target.ip
        if ip not in reverse_dns or (reverse_dns[ip] is None and domain_name is not None):
            reverse_dns[ip] = domain_name
    return [NetworkAddress(key, value) for (key, value) in reverse_dns.items()]


def _range_to_addresses(range_obj: NetworkRange) -> List[NetworkAddress]:
    addresses = []
    for address in range_obj:
        if hasattr(range_obj, "domain_name"):
            addresses.append(NetworkAddress(address, range_obj.domain_name))
        else:
            addresses.append(NetworkAddress(address, None))
    return addresses


def _get_ips_from_ranges_to_scan(ranges_to_scan: List[str]) -> List[NetworkAddress]:
    scan_targets = []

    ranges_to_scan = NetworkRange.filter_invalid_ranges(
        ranges_to_scan, "Bad network range input for targets to scan:"
    )

    network_ranges = [NetworkRange.get_range_obj(_range) for _range in ranges_to_scan]

    for _range in network_ranges:
        scan_targets.extend(_range_to_addresses(_range))
    return scan_targets


def _get_ips_to_scan_from_local_interface(
    interfaces: List[NetworkInterface],
) -> List[NetworkAddress]:
    ranges = [f"{interface.address}{interface.netmask}" for interface in interfaces]

    ranges = NetworkRange.filter_invalid_ranges(
        ranges, "Local network interface returns an invalid IP:"
    )
    return _get_ips_from_ranges_to_scan(ranges)


def _remove_interface_ips(
    scan_targets: List[NetworkAddress], interfaces: List[NetworkInterface]
) -> List[NetworkAddress]:
    interface_ips = [interface.address for interface in interfaces]
    return _remove_ips_from_scan_targets(scan_targets, interface_ips)


def _remove_blocklisted_ips(
    scan_targets: List[NetworkAddress], blocked_ips: List[str]
) -> List[NetworkAddress]:
    filtered_blocked_ips = NetworkRange.filter_invalid_ranges(
        blocked_ips, "Invalid blocked IP provided:"
    )
    if len(filtered_blocked_ips) != len(blocked_ips):
        raise InvalidNetworkRangeError("Received an invalid blocked IP. Aborting just in case.")
    return _remove_ips_from_scan_targets(scan_targets, filtered_blocked_ips)


def _remove_ips_from_scan_targets(
    scan_targets: List[NetworkAddress], ips_to_remove: List[str]
) -> List[NetworkAddress]:
    ips_to_remove_set = set(ips_to_remove)
    return [address for address in scan_targets if address.ip not in ips_to_remove_set]


def _get_segmentation_check_targets(
    inaccessible_subnets: List[str], local_interfaces: List[NetworkInterface]
) -> List[NetworkAddress]:
    ips_to_scan = []
    local_ips = [interface.address for interface in local_interfaces]

    local_ips = NetworkRange.filter_invalid_ranges(local_ips, "Invalid local IP found: ")
    inaccessible_subnets = NetworkRange.filter_invalid_ranges(
        inaccessible_subnets, "Invalid segmentation scan target: "
    )

    inaccessible_subnets = _convert_to_range_object(inaccessible_subnets)
    subnet_pairs = itertools.product(inaccessible_subnets, inaccessible_subnets)

    for (subnet1, subnet2) in subnet_pairs:
        if _is_segmentation_check_required(local_ips, subnet1, subnet2):
            ips = _get_ips_from_ranges_to_scan(subnet2)
            ips_to_scan.extend(ips)

    return ips_to_scan


def _convert_to_range_object(subnets: List[str]) -> List[NetworkRange]:
    return [NetworkRange.get_range_obj(subnet) for subnet in subnets]


def _is_segmentation_check_required(
    local_ips: List[str], subnet1: NetworkRange, subnet2: NetworkRange
):
    return _is_any_ip_in_subnet(local_ips, subnet1) and not _is_any_ip_in_subnet(local_ips, subnet2)


def _is_any_ip_in_subnet(ip_addresses: List[str], subnet: NetworkRange):
    for ip_address in ip_addresses:
        if subnet.is_in_range(ip_address):
            return True
    return False
