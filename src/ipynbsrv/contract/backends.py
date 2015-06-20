import os


class Backend(object):
    '''
    The backend interface defines the representation of an external resource
    like a container or storage backend or any other form of resource
    that exists outside of the application's context.

    Actions performed on instances of a backend should be reflected to its underlaying backend.

    All methods creating a resource must return the primary key for that resource as 'pk' and all methods
    returning resources or a list of them must include that 'pk' field as well.
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
    Key to be used in returns as unique identifier for the container.
    '''
    FIELD_PK = 'pk'

    '''
    Key to be used for the value storing the status (see below) of the container..
    '''
    FIELD_STATUS = 'status'

    '''
    String to be used in the 'status' field for a running container.
    '''
    STATUS_RUNNING = 'running'

    '''
    String to be used in the 'status' field for a stopped container.
    '''
    STATUS_STOPPED = 'stopped'

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
        raise NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the create_container method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_container_creation_fields(self):
        raise NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the start_container method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_container_start_fields(self):
        raise NotImplementedError

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
    def container_snapshot_exists(self, container, snapshot, **kwargs):
        raise NotImplementedError

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
    String to be used in the 'status' field for a stopped container.
    '''
    STATUS_SUSPENDED = 'suspended'

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


class StorageBackend(Backend):
    '''
    The storage backend component is used for users' home directories, publications
    and shared folders. It therefor abstracts basic operations on the filesystem like
    creating directories, setting owners etc.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    All implementations are required to accept the 'base_dir' argument in its constructor.
    '''

    '''
    Initializes a new storage backend instance that will work within 'base_dir'.

    :param base_dir: The base directory within which should be worked.
    '''
    def __init__(self, base_dir):
        if not os.path.exists(base_dir):
            raise DirectoryNotFoundError("Base directory does not exist.")

        self.base_dir = base_dir

    '''
    Checks if the directory with the given name exists.

    :param dir_name: The name of the directory to check.
    '''
    def dir_exists(self, dir_name, **kwargs):
        raise NotImplementedError

    '''
    Returns the group identifier of the group owning the directory.

    :param dir_name: The directory to get the group for.
    '''
    def get_dir_group(self, dir_name, **kwargs):
        raise NotImplementedError

    '''
    Returns the direcories access modes.

    :param dir_name: The directory to get the mode for.
    '''
    def get_dir_mode(self, dir_name, **kwargs):
        raise NotImplementedError

    '''
    Returns the user identifier of the user owning the directory.

    :param dir_name: The directory to get the owner for.
    '''
    def get_dir_owner(self, dir_name, **kwargs):
        raise NotImplementedError

    '''
    Returns the absolute/full path for the directory.

    :param dir_name: The directory to get the path for.
    '''
    def get_full_dir_path(self, dir_name, **kwargs):
        raise NotImplementedError

    '''
    Creates a directory with the given name.

    :param dir_name: The name of the directory to create.
    '''
    def mk_dir(self, dir_name, **kwargs):
        raise NotImplementedError

    '''
    Deletes the directory from the storage backend.

    :param dir_name: The name of the directory to delete.
    '''
    def rm_dir(self, dir_name, **kwargs):
        raise NotImplementedError

    '''
    Sets the directory's primary group.

    :param dir_name: The directory to set the group on.
    :param group: The group to set as primary group.
    '''
    def set_dir_group(self, dir_name, group, **kwargs):
        raise NotImplementedError

    '''
    Sets the directory's access mode.

    :param dir_name: The directory to set the group on.
    :param mode: The access mode to set.
    '''
    def set_dir_mode(self, dir_name, mode, **kwargs):
        raise NotImplementedError

    '''
    Sets the directory's owner.

    :param dir_name: The directory to set the group on.
    :param owner: The user to set as an owner.
    '''
    def set_dir_owner(self, dir_name, owner, **kwargs):
        raise NotImplementedError


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


class GroupBackend(Backend):
    '''
    The Group backend is used to abstract group management backends like LDAP

    All methods accept kwargs so individual data can be passed to conrete implementations.
    '''

    '''
    Key to be used in returns as unique identifier for the group.
    '''
    FIELD_GROUP_PK = 'pk'

    def add_user_to_group(self, user, group, **kwargs):
        raise NotImplementedError

    def create_group(self, specification, **kwargs):
        raise NotImplementedError

    def delete_group(self, group, **kwargs):
        raise NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the create_group method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_group_creation_fields(self):
        raise NotImplementedError

    def get_users_by_group(self, group, **kwargs):
        raise NotImplementedError

    def remove_user_from_group(self, user, group, **kwargs):
        raise NotImplementedError

    def rename_group(self, group, new_name, **kwargs):
        raise NotImplementedError


class UserBackend(Backend):
    '''
    The User backend is used to abstract user management backends like LDAP

    All methods accept kwargs so individual data can be passed to conrete implementations.
    '''

    '''
    Key to be used in returns as unique identifier for the user.
    '''
    FIELD_USER_PK = 'pk'

    def create_user(self, specification, **kwargs):
        raise NotImplementedError

    def delete_user(self, user, **kwargs):
        raise NotImplementedError

    '''
    Returns a list of field names the backend expects the input objects
    to the create_user method to have at least.

    The list should contain tuples in the form: (name, type)
    '''
    def get_required_user_creation_fields(self):
        raise NotImplementedError

    def get_user(self, pk, **kwargs):
        raise NotImplementedError

    def get_users(self, **kwargs):
        raise NotImplementedError

    def rename_user(self, user, new_name, **kwargs):
        raise NotImplementedError

    def set_user_password(self, user, password, **kwargs):
        raise NotImplementedError

    def user_exists(self, user):
        try:
            self.get_user(user)
            return True
        except UserNotFoundError:
            return False


class UserGroupBackendError(BackendError):
    '''
    Backend error type for users/groups backends.
    '''
    pass


class GroupNotFoundError(NotFoundError, UserGroupBackendError):
    '''
    Error meant to be raised when a group does not exist.
    '''


class UserNotFoundError(NotFoundError, UserGroupBackendError):
    '''
    Error meant to be raised when a user does not exist.
    '''
    pass


class AuthenticationBackend(object):
    '''
    https://docs.djangoproject.com/en/1.4/topics/auth/#writing-an-authentication-backend
    '''
    def authenticate(self, username=None, password=None):
        raise NotImplementedError

    def get_user(self, user_id):
        raise NotImplementedError
