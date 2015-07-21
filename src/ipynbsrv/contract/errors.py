class Error(Exception):

    """
    Base error for all ipynbsrv exceptions.

    Only when throwing an instance of this error one can be sure it
    will get caught by the application. All other exceptions might
    be unhandled leading to crashes.
    """

    pass


class BackendError(Error):

    """
    Base error for all backend exceptions.

    Backend errors are meant to be raised instead of letting the backend's
    real exception/error pass up the stack. Every error thrown from the backend
    should be wrapped.
    """

    pass


class ConnectionError(BackendError):

    """
    Generic backend error meant to be thrown then a connection to the backend cannot be established.
    """

    pass


class NotFoundError(BackendError):

    """
    Generic (backend record) not found error.

    Error meant to be raised when an operation can not be performed
    because the resource on which the method should act does not exist.
    """

    pass


class ContainerBackendError(BackendError):

    """
    Backend error type for container backends.
    """

    pass


class ContainerNotFoundError(NotFoundError, ContainerBackendError):

    """
    Error meant to be raised when a container does not exist.

    A reason for such a failure could be that the container on which a method should act, does not exist.
    """

    pass


class IllegalContainerStateError(ContainerBackendError):

    """
    Error for problems due to a container's state.

    Error meant to be raised when an operation can not be performed
    because the container on which the method should act is in an
    illegal state (e.g. exec method and the container is stopped).
    """

    pass


class ContainerImageNotFoundError(NotFoundError, ContainerBackendError):

    """
    Error meant to be raised when an image (container template) does not exist.
    """

    pass


class ContainerSnapshotNotFoundError(ContainerBackendError):

    """
    Error for non-existing container snapshots.

    Meant to be raised when an operation can not be performed
    because the snapshot on which the method should act does not exist.
    """

    pass


class GroupBackendError(BackendError):

    """
    Backend error type for user backends.
    """

    pass


class GroupNotFoundError(NotFoundError, GroupBackendError):

    """
    Error meant to be raised when a group does not exist.
    """

    pass


class StorageBackendError(BackendError):

    """
    Backend error type for storage backends.
    """

    pass


class DirectoryNotFoundError(NotFoundError, StorageBackendError):

    """
    Error to be raised when the directory on which an operation should be performed does not exist.
    """

    pass


class UserBackendError(BackendError):

    """
    Backend error type for user backends.
    """

    pass


class AuthenticationError(UserBackendError):

    """
    Error meant to be raised when there is a problem while authenticating.
    """

    pass


class ReadOnlyError(UserBackendError):

    """
    Error indicating that a user cannot be updated because the backend is read-only.
    """

    pass


class UserNotFoundError(NotFoundError, UserBackendError):

    """
    Error meant to be raised when a user does not exist.
    """

    pass


class ServiceError(Exception):

    """
    Base exception class for errors raised by service implementations.
    """

    pass


class EncryptionServiceError(ServiceError):

    """
    Service error type for encryption services.
    """

    pass


class IntegrityServiceError(ServiceError):

    """
    Service error type for integrity services.
    """

    pass


class IntegrityValidationError(IntegrityServiceError):

    """
    Error to be raised when an integrity cannot be verified or the integrity check fails.
    """

    pass
