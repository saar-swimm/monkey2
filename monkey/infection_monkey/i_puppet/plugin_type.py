from enum import Enum


class PluginType(Enum):
    CREDENTIAL_COLLECTOR = "CredentialCollector"
    EXPLOITER = "Exploiter"
    FINGERPRINTER = "Fingerprinter"
    PAYLOAD = "Payload"
    POST_BREACH_ACTION = "PBA"
