class Service(object):
    '''
    The interface defines a service in the sense of 'a resource that can be used for only a handful of jobs'.
    '''
    pass


class ServiceError(Exception):
    '''
    Base exception class for errors raised by service implementations.
    '''

    def __init__(self, message):
        super(ServiceError, self).__init__(message)
        self.message = message


class EncryptionService(Service):
    '''
    The encryption service interfaces defines the public API a concrete implementation has to fullfil
    to be a compliant ipynbsrv encryption service.

    These services are used whenever (sensitive) data have to be transfered between different actors
    and the connection cannot be considered secure.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    '''

    '''
    Decrypts the input cipher text with the given key.

    :param text: The cipher text to decrypt.
    :param key: The key to decrypt the message with.
    '''
    def decrypt(self, text, key, **kwargs):
        raise NotImplementedError

    '''
    Encrypts the input text with the given key.

    :param text: The text to encrypt.
    :param key: The key to encrypt the text with.
    '''
    def encrypt(self, text, key, **kwargs):
        raise NotImplementedError


class EncryptionServiceError(ServiceError):
    '''
    Service error type for encryption services.
    '''
    pass


class IntegrityService(Service):
    '''
    The integrity services are used whenever the integrity of a resource (message, status etc.) needs to
    be ensured.
    '''

    '''
    Signs the input text with the provided key.

    :param text: The text to sign.
    :param key: The key to sign the text with.
    '''
    def sign(self, text, key, **kwargs):
        raise NotImplementedError

    '''
    Verifies the signature of the input text using the provided key.

    :param text: The text to verify the signature of.
    :param signature: The signature to verify for the text.
    :param key: The key to verify the signature with.
    '''
    def verify(self, text, signature, key, **kwargs):
        raise NotImplementedError


class IntegrityServiceError(ServiceError):
    '''
    Service error type for integrity services.
    '''
    pass
