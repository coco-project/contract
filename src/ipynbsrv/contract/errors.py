class BackendError(Exception):
    '''
    Backend errors are meant to be raised instead of letting the backend's
    real exception/error pass up the stack. Every error thrown from the backend
    should be wrapped.
    '''
    pass


class NotFoundError(BackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the resource on which the method should act does not exist.
    '''
    pass


class ContainerBackendError(BackendError):
    '''
    Backend error type for container backends.
    '''
    pass


class ContainerNotFoundError(NotFoundError, ContainerBackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the container on which the method should act does not exist.
    '''
    pass


class IllegalContainerSpecificationError(ContainerBackendError):
    '''
    Error meant to be thrown by methods that fail to execute due to
    a bad (container) specification as per the various get_required_*_fields methods.
    '''
    pass


class IllegalContainerStateError(ContainerBackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the container on which the method should act is in an
    illegal state (e.g. exec method and the container is stopped).
    '''
    pass


class ContainerImageNotFoundError(NotFoundError, ContainerBackendError):
    '''
    Error meant to be raised when an image (container template) does not exist.
    '''
    pass


class ContainerSnapshotNotFoundError(ContainerBackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the snapshot on which the method should act does not exist.
    '''
    pass


class GroupBackendError(BackendError):
    '''
    Backend error type for user backends.
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GroupNotFoundError(NotFoundError, GroupBackendError):
    '''
    Error meant to be raised when a group does not exist.
    '''
    def __init__(self, group):
        self.group = group

    def __str__(self):
        return 'Group not found: {0}'.format(repr(self.group))


class StorageBackendError(BackendError):
    '''
    Backend error type for storage backends.
    '''
    pass


class DirectoryNotFoundError(NotFoundError, StorageBackendError):
    '''
    Storage backend error to be raised when the directory on which an operation
    should be performed does not exist.
    '''
    pass


class UserBackendError(BackendError):
    '''
    Backend error type for user backends.
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserNotFoundError(NotFoundError, UserBackendError):
    '''
    Error meant to be raised when a user does not exist.
    '''
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return 'User not found: {0}'.format(repr(self.user))
