from typing import Dict
from nilai_py.niltypes import (
    DelegationTokenRequest,
    DelegationTokenResponse,
    DelegationServerConfig,
    DefaultDelegationTokenServerConfig,
    DelegationTokenServerType,
    NilAuthInstance,
    NilAuthPrivateKey,
)

from nilai_py.common import is_expired
from nuc.envelope import NucTokenEnvelope
from nuc.token import Did
from nuc.builder import NucTokenBuilder, Command
from nuc.nilauth import NilauthClient, BlindModule
import datetime


class DelegationTokenServer:
    def __init__(
        self,
        private_key: str,
        config: DelegationServerConfig = DefaultDelegationTokenServerConfig,
        nilauth_instance: NilAuthInstance = NilAuthInstance.SANDBOX,
    ):
        """
        Initialize the delegation token server.

        Args:
            private_key (str): The private key of the server.
            config (DelegationServerConfig): The configuration for the server.
            nilauth_instance (NilAuthInstance): The nilauth instance to use.
        """
        self.config: DelegationServerConfig = config
        self.private_key: NilAuthPrivateKey = NilAuthPrivateKey(
            bytes.fromhex(private_key)
        )
        self.nilauth_instance: NilAuthInstance = nilauth_instance
        self._root_token_envelope: NucTokenEnvelope = None

    @property
    def root_token(self) -> NucTokenEnvelope:
        """
        Get the root token envelope. If the root token is expired, it will be refreshed.
        The root token is used to create delegation tokens.

        Returns:
            NucTokenEnvelope: The root token envelope.
        """
        if self._root_token_envelope is None or is_expired(self._root_token_envelope):
            if self.config.mode == DelegationTokenServerType.DELEGATION_ISSUER:
                raise ValueError(
                    "In DELEGATION_ISSUER mode, the root token cannot be refreshed, it must be provided"
                )
            nilauth_client = NilauthClient(self.nilauth_instance.value)
            root_token_response = nilauth_client.request_token(
                self.private_key, blind_module=BlindModule.NILAI
            )
            self._root_token_envelope = NucTokenEnvelope.parse(root_token_response)
        return self._root_token_envelope

    def update_delegation_token(self, root_token: str):
        """
        Update the root token envelope.

        Args:
            root_token (str): The new root token.
        """
        if self.config.mode != DelegationTokenServerType.DELEGATION_ISSUER:
            raise ValueError(
                "Delegation token can only be updated in DELEGATION_ISSUER mode"
            )
        self._root_token_envelope = NucTokenEnvelope.parse(root_token)

    def get_delegation_request(self) -> DelegationTokenRequest:
        """
        Get the delegation request for the client.

        Returns:
            DelegationTokenRequest: The delegation request.
        """
        delegation_request: DelegationTokenRequest = DelegationTokenRequest(
            public_key=self.private_key.pubkey.serialize().hex()
        )
        return delegation_request

    def create_delegation_token(
        self,
        delegation_token_request: DelegationTokenRequest,
        config_override: DelegationServerConfig = None,
    ) -> DelegationTokenResponse:
        """
        Create a delegation token.

        Args:
            delegation_token_request (DelegationTokenRequest): The delegation token request.
            config_override (DelegationServerConfig): The configuration override.

        Returns:
            DelegationTokenResponse: The delegation token response.
        """
        config = config_override if config_override else self.config

        public_key: bytes = bytes.fromhex(delegation_token_request.public_key)

        meta: Dict[str, str] = {
            "usage_limit": config.token_max_uses,
        }
        if config.prompt_document:
            meta["document_id"] = config.prompt_document.doc_id
            meta["document_owner_did"] = config.prompt_document.owner_did

        delegated_token = (
            NucTokenBuilder.extending(self.root_token)
            .expires_at(
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(seconds=config.expiration_time)
            )
            .audience(Did(public_key))
            .command(Command(["nil", "ai", "generate"]))
            .meta(meta)
            .build(self.private_key)
        )
        return DelegationTokenResponse(delegation_token=delegated_token)
