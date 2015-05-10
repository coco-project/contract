class Service(object):
    '''
    The interface defines a service in the sense of 'a resource that can be used for only a handful of jobs'.
    '''
    pass


class ContainerHostSelectionService(Service):
    '''
    The container host selection service interface defines the method signature for the algorithm
    that will choose the docker host for a new container in a multihost environment

    TODO: change interface to something more flexible (i.e. list of dicts with additional information)

    :param count: numberof Servers available
    '''
    @staticmethod
    def get_server(self, count):
        raise NotImplementedError


class ServiceError(Exception):
    '''
    Base exception class for errors raised by service implementations.
    '''
    pass


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


class IntegrityValidationError(IntegrityServiceError):
    '''
    Error to be raised when an integrity (e.g. the return value of a sign() call)
    cannot be verified or the integrity check fails.
    '''
    pass
