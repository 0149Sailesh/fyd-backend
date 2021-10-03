import jwt
import json
import base64

from app.config import keys, api_keys


# https://docs.setu.co/data/account-aggregator/request-signing#request-signing
def makeDetachedJWS(payload):
    """Creates a JWS payload for the given payload which can be used
    attached as the HTTP Header 'x-jws-signature'

    Args:
        payload (any): payload which u want the signature to contain

    Returns:
        string: the jws signature for the given payload
    """
    encoded = jwt.encode(payload, keys.PRIVATE_KEY, algorithm="RS256")
    splittedJWS = encoded.split(".")
    splittedJWS[1] = ""
    return ".".join(splittedJWS)

def createAuthHeadersForAPI(payload):
    return {
        "x-jws-signature": makeDetachedJWS(payload),
        "client_api_key": api_keys.CLIENT_API_KEY,
    }

def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace(b"=", b"")


def validateDetachedJWS(payload, signature):
    splittedJWS = signature.split(".")
    splittedJWS[1] = base64url_encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    splittedJWS[1] = splittedJWS[1].decode("utf-8")
    sig = ".".join(splittedJWS)
    try:
        jwt.decode(sig, keys.PUBLIC_KEY, algorithms=["RS256"])
        return True
    except Exception as e:
        print(e)
        return False
