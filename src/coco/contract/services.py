class Service(object):

    """
    The interface defines a service in the sense of 'a resource that can be used for only a handful of jobs'.
    """

    pass


class EncryptionService(Service):

    """
    The encryption service defines the API an implementation has to fullfil to be a compliant coco encryption service.

    These services are used whenever (sensitive) data have to be transfered between different actors
    and the connection cannot be considered secure.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    """

    def decrypt(self, text, key, **kwargs):
        """
        Decrypt the input cipher text with the given key.

        :param text: The cipher text to decrypt.
        :param key: The key to decrypt the message with.
        """
        raise NotImplementedError

    def encrypt(self, text, key, **kwargs):
        """
        Encrypt the input text with the given key.

        :param text: The text to encrypt.
        :param key: The key to encrypt the text with.
        """
        raise NotImplementedError


class IntegrityService(Service):

    """
    Base class for integrity service implementations.

    The integrity services are used whenever the integrity of a resource (message, status etc.)
    needs to be ensured.
    """

    def sign(self, text, key, **kwargs):
        """
        Sign the input text with the provided key.

        :param text: The text to sign.
        :param key: The key to sign the text with.
        """
        raise NotImplementedError

    def verify(self, text, signature, key, **kwargs):
        """
        Verify the signature of the input text using the provided key.

        :param text: The text to verify the signature of.
        :param signature: The signature to verify for the text.
        :param key: The key to verify the signature with.
        """
        raise NotImplementedError
