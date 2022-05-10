import logging
import select
import socket
import time
from typing import Iterable, Mapping, Tuple

from infection_monkey.i_puppet import PortScanData, PortStatus
from infection_monkey.network.tools import BANNER_READ, DEFAULT_TIMEOUT, tcp_port_to_service
from infection_monkey.utils.timer import Timer

logger = logging.getLogger(__name__)

POLL_INTERVAL = 0.5
EMPTY_PORT_SCAN = {-1: PortScanData(-1, PortStatus.CLOSED, None, None)}


def scan_tcp_ports(
    host: str, ports_to_scan: Iterable[int], timeout: float
) -> Mapping[int, PortScanData]:
    try:
        return _scan_tcp_ports(host, ports_to_scan, timeout)
    except Exception:
        logger.exception("Unhandled exception occurred while trying to scan tcp ports")
        return EMPTY_PORT_SCAN


def _scan_tcp_ports(host: str, ports_to_scan: Iterable[int], timeout: float):
    open_ports = _check_tcp_ports(host, ports_to_scan, timeout)

    return _build_port_scan_data(ports_to_scan, open_ports)


def _build_port_scan_data(
    ports_to_scan: Iterable[int], open_ports: Mapping[int, str]
) -> Mapping[int, PortScanData]:
    port_scan_data = {}
    for port in ports_to_scan:
        if port in open_ports:
            service = tcp_port_to_service(port)
            banner = open_ports[port]

            port_scan_data[port] = PortScanData(port, PortStatus.OPEN, banner, service)
        else:
            port_scan_data[port] = _get_closed_port_data(port)

    return port_scan_data


def _get_closed_port_data(port: int) -> PortScanData:
    return PortScanData(port, PortStatus.CLOSED, None, None)


def _check_tcp_ports(
    ip: str, ports_to_scan: Iterable[int], timeout: float = DEFAULT_TIMEOUT
) -> Mapping[int, str]:
    """
    Checks whether any of the given ports are open on a target IP.
    :param ip:  IP of host to attack
    :param ports_to_scan: An iterable of ports to scan. Must not be empty.
    :param timeout: Amount of time to wait for connection
    :return: Mapping where the key is an open port and the value is the banner
    :rtype: Mapping
    """
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(len(ports_to_scan))]
    for s in sockets:
        s.setblocking(False)

    possible_ports = set()
    connected_ports = set()
    open_ports = {}

    try:
        logger.debug(
            "Connecting to the following ports %s" % ",".join((str(x) for x in ports_to_scan))
        )
        for sock, port in zip(sockets, ports_to_scan):
            err = sock.connect_ex((ip, port))
            if err == 0:  # immediate connect
                connected_ports.add((port, sock))
                possible_ports.add((port, sock))
            elif err == 10035:  # WSAEWOULDBLOCK is valid.
                # https://docs.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-connect
                # says, "Use the select function to determine the completion of the connection
                # request by checking to see if the socket is writable," which is being done below.
                possible_ports.add((port, sock))
            elif err == 115:  # EINPROGRESS     115     /* Operation now in progress */
                possible_ports.add((port, sock))
            else:
                logger.warning("Failed to connect to port %s, error code is %d", port, err)

        if len(possible_ports) != 0:
            sockets_to_try = possible_ports.copy()

            timer = Timer()
            timer.set(timeout)

            while (not timer.is_expired()) and sockets_to_try:
                # The call to select() may return sockets that are writeable but not actually
                # connected. Adding this sleep prevents excessive looping.
                time.sleep(min(POLL_INTERVAL, timer.time_remaining))

                sock_objects = [s[1] for s in sockets_to_try]

                _, writeable_sockets, _ = select.select([], sock_objects, [], timer.time_remaining)
                for s in writeable_sockets:
                    try:  # actual test
                        connected_ports.add((s.getpeername()[1], s))
                    except socket.error:  # bad socket, select didn't filter it properly
                        pass

                sockets_to_try = sockets_to_try - connected_ports

            logger.debug(
                "On host %s discovered the following ports %s"
                % (str(ip), ",".join([str(s[0]) for s in connected_ports]))
            )

            open_ports = {port: "" for port, _ in connected_ports}
            if len(connected_ports) != 0:
                readable_sockets, _, _ = select.select(
                    [s[1] for s in connected_ports], [], [], timer.time_remaining
                )
                # read first BANNER_READ bytes. We ignore errors because service might not send a
                # decodable byte string.
                for port, sock in connected_ports:
                    if sock in readable_sockets:
                        open_ports[port] = sock.recv(BANNER_READ).decode(errors="ignore")
                    else:
                        open_ports[port] = ""

    except socket.error as exc:
        logger.warning("Exception when checking ports on host %s, Exception: %s", str(ip), exc)

    _clean_up_sockets(possible_ports, connected_ports)

    return open_ports


def _clean_up_sockets(
    possible_ports: Iterable[Tuple[int, socket.socket]],
    connected_ports_sockets: Iterable[Tuple[int, socket.socket]],
):
    # Only call shutdown() on sockets we know to be connected
    for port, s in connected_ports_sockets:
        try:
            s.shutdown(socket.SHUT_RDWR)
        except socket.error as exc:
            logger.warning(f"Error occurred while shutting down socket on port {port}: {exc}")

    # Call close() for all sockets
    for port, s in possible_ports:
        try:
            s.close()
        except socket.error as exc:
            logger.warning(f"Error occurred while closing socket on port {port}: {exc}")
