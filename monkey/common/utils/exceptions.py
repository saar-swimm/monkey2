class FailedExploitationError(Exception):
    """Raise when exploiter fails instead of returning False"""


class InvalidRegistrationCredentialsError(Exception):
    """Raise when server config file changed and island needs to restart"""


class AlreadyRegisteredError(Exception):
    """Raise to indicate the reason why registration is not required"""


class UnknownUserError(Exception):
    """Raise to indicate that authentication failed"""


class IncorrectCredentialsError(Exception):
    """Raise to indicate that authentication failed"""


class NoInternetError(Exception):
    """Raise to indicate problems caused when no internet connection is present"""


class UnknownFindingError(Exception):
    """Raise when provided finding is of unknown type"""


class VersionServerConnectionError(Exception):
    """Raise to indicate that connection to version update server failed"""


class FindingWithoutDetailsError(Exception):
    """Raise when pulling events for a finding, but get none"""


class DomainControllerNameFetchError(FailedExploitationError):
    """Raise on failed attempt to extract domain controller's name"""


class InvalidConfigurationError(Exception):
    """Raise when configuration is invalid"""
