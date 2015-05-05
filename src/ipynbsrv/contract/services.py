class Service(object):
    '''
    The interface defines a service in the sense of 'a resource that can be used for only a handful of jobs'.
    '''
    pass


class EncryptionService(Service):
    '''
    The encryption service interfaces defines the public API a concrete implementation has to fullfil
    to be a compliant ipynbsrv encryption service.

    These services are used whenever (sensitive) data have to be transfered between different actors
    and the connection cannot be considered secure.
    '''

    '''
    Decrypts the input cipher text with the given key.

    :param text: The cipher text to decrypt.
    :param key: The key to decrypt the message with.
    '''
    def decrypt(self, text, key):
        raise NotImplementedError

    '''
    Encrypts the input text with the given key.

    :param text: The text to encrypt.
    :param key: The key to encrypt the text with.
    '''
    def encrypt(self, text, key):
        raise NotImplementedError


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
    def sign(self, text, key):
        raise NotImplementedError

    '''
    Verifies the signature of the input text using the provided key.

    :param text: The text to verify the signature of.
    :param signature: The signature to verify for the text.
    :param key: The key to verify the signature with.
    '''
    def verify(self, text, signature, key):
        raise NotImplementedError
