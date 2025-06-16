import datetime
from nuc.envelope import NucTokenEnvelope
from nuc.token import NucToken


def is_expired(token_envelope: NucTokenEnvelope) -> bool:
    """
    Check if a token envelope is expired.

    Args:
        token_envelope (NucTokenEnvelope): The token envelope to check.

    Returns:
        bool: True if the token envelope is expired, False otherwise.
    """
    token: NucToken = token_envelope.token.token
    if token.expires_at is None:
        return False
    return token.expires_at < datetime.datetime.now(datetime.timezone.utc)
