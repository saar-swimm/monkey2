from dataclasses import dataclass
from typing import Dict

from infection_monkey.i_puppet import FingerprintData, PingScanData, PortScanData

Port = int
FingerprinterName = str


@dataclass
class IPScanResults:
    ping_scan_data: PingScanData
    port_scan_data: Dict[Port, PortScanData]
    fingerprint_data: Dict[FingerprinterName, FingerprintData]
