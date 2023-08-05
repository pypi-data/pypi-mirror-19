import hmac
from binascii import hexlify
from hashlib import sha1


def create_signed_url(base_url: str, hmac_key: bytes, url: str) -> str:
    """Create a camo signed URL for the specified image URL

    Args:
        base_url: Base URL of the camo installation
        hmac_key: HMAC shared key to be used for signing
        url: URL of the destination image

    Returns:
        str: A full url that can be used to serve the proxied image
    """

    base_url = base_url.rstrip('/')
    signature = hmac.HMAC(hmac_key, url.encode(), digestmod=sha1).hexdigest()
    hex_url = hexlify(url.encode()).decode()

    return ('{base}/{signature}/{hex_url}'
            .format(base=base_url, signature=signature, hex_url=hex_url))
