import logging
from typing import Any, Iterable, Mapping

from common.common_consts.credential_component_type import CredentialComponentType
from infection_monkey.custom_types import PropagationCredentials
from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.i_puppet import Credentials
from infection_monkey.utils.decorators import request_cache

from .i_credentials_store import ICredentialsStore

logger = logging.getLogger(__name__)

CREDENTIALS_POLL_PERIOD_SEC = 10


class AggregatingCredentialsStore(ICredentialsStore):
    def __init__(self, control_channel: IControlChannel):
        self._stored_credentials = {
            "exploit_user_list": set(),
            "exploit_password_list": set(),
            "exploit_lm_hash_list": set(),
            "exploit_ntlm_hash_list": set(),
            "exploit_ssh_keys": [],
        }
        self._control_channel = control_channel

    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        for credentials in credentials_to_add:
            usernames = {
                identity.username
                for identity in credentials.identities
                if identity.credential_type is CredentialComponentType.USERNAME
            }
            self._stored_credentials.setdefault("exploit_user_list", set()).update(usernames)

            for secret in credentials.secrets:
                if secret.credential_type is CredentialComponentType.PASSWORD:
                    self._stored_credentials.setdefault("exploit_password_list", set()).add(
                        secret.password
                    )
                elif secret.credential_type is CredentialComponentType.LM_HASH:
                    self._stored_credentials.setdefault("exploit_lm_hash_list", set()).add(
                        secret.lm_hash
                    )
                elif secret.credential_type is CredentialComponentType.NT_HASH:
                    self._stored_credentials.setdefault("exploit_ntlm_hash_list", set()).add(
                        secret.nt_hash
                    )
                elif secret.credential_type is CredentialComponentType.SSH_KEYPAIR:
                    self._set_attribute(
                        "exploit_ssh_keys",
                        [{"public_key": secret.public_key, "private_key": secret.private_key}],
                    )

    def get_credentials(self) -> PropagationCredentials:
        try:
            propagation_credentials = self._get_credentials_from_control_channel()

            # Needs to be reworked when exploiters accepts sequence of Credentials
            self._aggregate_credentials(propagation_credentials)

            return self._stored_credentials
        except Exception as ex:
            self._stored_credentials = {}
            logger.error(f"Error while attempting to retrieve credentials for propagation: {ex}")

    @request_cache(CREDENTIALS_POLL_PERIOD_SEC)
    def _get_credentials_from_control_channel(self) -> PropagationCredentials:
        return self._control_channel.get_credentials_for_propagation()

    def _aggregate_credentials(self, credentials_to_aggr: Mapping):
        for cred_attr, credentials_values in credentials_to_aggr.items():
            self._set_attribute(cred_attr, credentials_values)

    def _set_attribute(self, attribute_to_be_set: str, credentials_values: Iterable[Any]):
        if not credentials_values:
            return

        if isinstance(credentials_values[0], dict):
            self._stored_credentials.setdefault(attribute_to_be_set, []).extend(credentials_values)
            self._stored_credentials[attribute_to_be_set] = [
                dict(s_c)
                for s_c in set(
                    frozenset(d_c.items()) for d_c in self._stored_credentials[attribute_to_be_set]
                )
            ]
        else:
            self._stored_credentials.setdefault(attribute_to_be_set, set()).update(
                credentials_values
            )
