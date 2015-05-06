class Backend(object):
    '''
    The backend interface defines the representation of an external resource
    like a container or storage backend or any other form of resource
    that exists outside of the application's context.

    Actions performed on instances of a backend should be reflected to its underlaying backend.
    '''
    pass


class BackendError(Exception):
    '''
    Backend errors are meant to be raised instead of letting the backend's
    real exception/error pass up the stack. Every error thrown from the backend
    should be wrapped.
    '''

    def __init__(self, message):
        super(Backend.Error, self).__init__(message)
        self.message = message


class NotFoundError(BackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the resource on which the method should act does not exist.
    '''
    pass


class ContainerBackend(Backend):
    '''
    The container backend is used to abstract container/virtualization backends like
    Docker or VirtualBox.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    '''

    '''
    Checks if the given container exists in the backend.

    :param container: The container to check.
    '''
    def container_exists(self, container, **kwargs):
        raise NotImplementedError

    '''
    Returns true if the container is running.

    :param container: The container to check.
    '''
    def container_is_running(self, container, **kwargs):
        raise NotImplementedError

    '''
    Creates a new container instance.

    :param container: The container to create on the backend.
    '''
    def create_container(self, container, **kwargs):
        raise NotImplementedError

    '''
    Deletes the container.

    :param container: The container to delete.
    '''
    def delete_container(self, container, **kwargs):
        raise NotImplementedError

    '''
    Executes the given command inside the container.

    :param container: The container to execute the command in.
    :param cmd: The command to execute.
    '''
    def exec_in_container(self, container, cmd, **kwargs):
        raise NotImplementedError

    '''
    Returns information about the requested container.

    :param container: The container to get the information of.
    '''
    def get_container(self, container, **kwargs):
        raise NotImplementedError

    '''
    Returns the logging output of the container.

    :param container: The container to get the information of.
    '''
    def get_container_logs(self, container, **kwargs):
        raise NotImplementedError

    '''
    Returns a list of all containers.

    :param only_running: If true, only running containers are returned.
    '''
    def get_containers(self, only_running=False, **kwargs):
        return NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the create_container method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_creation_fields(self):
        return NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the start_container method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_start_fields(self):
        return NotImplementedError

    '''
    Restarts the container.

    If the concret backend has a native restart implementation, this method should
    be overriden, since the default implementation does two simple start/stop calls.

    :param container: The container to restart.
    '''
    def restart_container(self, container, **kwargs):
        self.stop(force=force)
        self.start()

    '''
    Starts the container.

    :param container: The container to start.
    '''
    def start_container(self, container):
        raise NotImplementedError

    '''
    Stops the container.

    :param container: The container to stop.
    '''
    def stop_container(self, container, **kwargs):
        raise NotImplementedError


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


class IllegalContainerStateError(ContainerBackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the container on which the method should act is in an
    illegal state (e.g. exec method and the container is stopped).
    '''
    pass


class CloneableContainerBackend(ContainerBackend):
    '''
    The cloneable container backend extends the regular container backend
    by providing a way to duplicate (clone) existing containers.
    '''

    '''
    Clones the container and returns the newly created one (clone).

    :param container: The container to clone.
    '''
    def clone_container(self, container, **kwargs):
        raise NotImplementedError


class SnapshotableContainerBackend(ContainerBackend):
    '''
    The snapshotable container backend extends the regular container backend
    by providing a way to snapshot/commit an existing container.
    '''

    '''
    Checks if a snapshot with the given name exists for the container.

    :param container: The container to check.
    :param name: The name of the snapshot to check.
    '''
    def container_snapshot_exists(self, container, name, **kwargs):
        raise NotImplemented

    '''
    Creates a snapshop of the container.

    :param container: The container to snapshot.
    :param name: The name of the created snapshot.
    '''
    def create_container_snapshot(self, container, name, **kwargs):
        raise NotImplementedError

    '''
    Deletes the container's snapshot.

    :param container: The container to act on.
    :param snapshot: The snapshot to delete.
    '''
    def delete_container_snapshot(self, container, snapshot, **kwargs):
        raise NotImplementedError

    '''
    Returns information about the container's snapshot.

    :param container: The container to get the snapshots for.
    :param snapshot: The snapshot to get information for.
    '''
    def get_container_snapshot(self, container, snapshot, **kwargs):
        raise NotImplementedError

    '''
    Returns a list of snapshots for the given container.

    :param container: The container to get the snapshots for.
    '''
    def get_container_snapshots(self, container, **kwargs):
        raise NotImplementedError

    '''
    Restores the container's snapshot.

    :param container: The container to restore.
    :param snapshot: The snapshot to restore.
    '''
    def restore_container_snapshot(self, container, snapshot, **kwargs):
        raise NotImplementedError


class ContainerSnapshotNotFoundError(ContainerNotFoundError):
    '''
    Error meant to be raised when an operation can not be performed
    because the snapshot on which the method should act does not exist.
    '''
    pass
