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
    pass


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

    Implementations are free to either use the specification argument or kwargs
    for input arguments.
    Required fields should however be included in the specification.

    :param specification: The specification of the to be created container.
    '''
    def create_container(self, specification, **kwargs):
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
    def get_required_container_creation_fields(self):
        return NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the start_container method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_container_start_fields(self):
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

    Implementations are free to either use the specification argument or kwargs
    for input arguments.
    Required fields should however be included in the specification.

    :param container: The container to snapshot.
    :param specification: The specification of the to be created snapshot.
    '''
    def create_container_snapshot(self, container, specification, **kwargs):
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
    Returns a list of field names the backend expects the input objects
    to the create_container_snapshot method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_snapshot_creation_fields(self):
        raise NotImplementedError

    '''
    Restores the container's snapshot.

    :param container: The container to restore.
    :param snapshot: The snapshot to restore.
    '''
    def restore_container_snapshot(self, container, snapshot, **kwargs):
        raise NotImplementedError


class ContainerSnapshotNotFoundError(ContainerBackendError):
    '''
    Error meant to be raised when an operation can not be performed
    because the snapshot on which the method should act does not exist.
    '''
    pass


class SuspendableContainerBackend(ContainerBackend):
    '''
    The suspendable container backend adds suspend/resume capabilities to
    the regular container backend. Other than start/stop, these two operations
    to not really stop a container but actually freeze it.
    '''

    '''
    Checks if the container is suspended.

    :param container: The container to check.
    '''
    def container_is_suspended(self, container, **kwargs):
        raise NotImplementedError

    '''
    Resumes a suspended container.

    :param container: The container to resume.
    '''
    def resume_container(self, container, **kwargs):
        raise NotImplementedError

    '''
    Suspends a running container.

    :param container: The container to resume.
    '''
    def suspend_container(self, container, **kwargs):
        raise NotImplementedError


class ImageBasedContainerBackend(ContainerBackend):
    '''
    The image based container backend interface can be implemented by container backends
    to signalize that they are image/template based.
    '''

    '''
    Creates a new image from the specification.

    :param specification: The specification for the new image.
    '''
    def create_image(self, specification, **kwargs):
        raise NotImplementedError

    '''
    Deletes the container image.

    :param image: The image to delete.
    '''
    def delete_image(self, image, **kwargs):
        raise NotImplementedError

    '''
    Returns information about the requested image.

    :param image: The image to get.
    '''
    def get_image(self, image, **kwargs):
        raise NotImplementedError

    '''
    Returns a list of available container images.
    '''
    def get_images(self, **kwargs):
        raise NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the create_image method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_image_creation_fields(self):
        raise NotImplementedError

    '''
    Checks if the image exists on the backend.

    :param image: The image to check for.
    '''
    def image_exists(self, image):
        raise NotImplementedError


class ContainerImageNotFoundError(NotFoundError, ContainerBackendError):
    '''
    Error meant to be raised when an image (container template) does not exist.
    '''
    pass
