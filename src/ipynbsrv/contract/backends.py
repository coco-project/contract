from ipynbsrv.contract.errors import DirectoryNotFoundError, UserNotFoundError
import os


class Backend(object):

    """
    Parent class for all pluggable ipynbsrv backend components.

    The backend interface defines the representation of an external resource
    like a container or storage backend or any other form of resource
    that exists outside of the application's context.

    Actions performed on instances of a backend should be reflected to its underlaying backend.

    All methods creating a resource must return the primary key for that resource as 'pk' and all methods
    returning resources or a list of them must include that 'pk' field as well.
    """

    pass


class ContainerBackend(Backend):

    """
    The container backend is used to abstract container/virtualization backends like Docker or VirtualBox.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    """

    """
    Key to be used in returns as unique identifier for the container.
    """
    FIELD_PK = 'pk'

    """
    Key to be used for the value storing the status (see below) of the container..
    """
    FIELD_STATUS = 'status'

    """
    String to be used in the 'status' field for a running container.
    """
    STATUS_RUNNING = 'running'

    """
    String to be used in the 'status' field for a stopped container.
    """
    STATUS_STOPPED = 'stopped'

    def container_exists(self, container, **kwargs):
        """
        Check if the given container exists in the backend.

        :param container: The container to check.
        """
        raise NotImplementedError

    def container_is_running(self, container, **kwargs):
        """
        Return true if the container is running.

        :param container: The container to check.
        """
        raise NotImplementedError

    def create_container(self, specification, **kwargs):
        """
        Create a new container instance.

        Implementations are free to either use the specification argument or kwargs
        for input arguments.
        Required fields should however be included in the specification.

        :param specification: The specification of the to be created container.
        """
        raise NotImplementedError

    def delete_container(self, container, **kwargs):
        """
        Delete the container.

        :param container: The container to delete.
        """
        raise NotImplementedError

    def exec_in_container(self, container, cmd, **kwargs):
        """
        Execute the given command inside the container.

        :param container: The container to execute the command in.
        :param cmd: The command to execute.
        """
        raise NotImplementedError

    def get_container(self, container, **kwargs):
        """
        Get information about the requested container.

        :param container: The container to get the information of.
        """
        raise NotImplementedError

    def get_container_logs(self, container, **kwargs):
        """
        Get the logging output of the container.

        :param container: The container to get the information of.
        """
        raise NotImplementedError

    def get_containers(self, only_running=False, **kwargs):
        """
        Get a list of all containers.

        :param only_running: If true, only running containers are returned.
        """
        raise NotImplementedError

    def get_required_container_cretion_fields(self):
        """
        Get a list of fields the backend expects the input objects to the create_container method to have at least.

        The list should contain tuples in the form: (name, type)
        """
        raise NotImplementedError

    def get_required_container_start_fields(self):
        """
        Get a list of fields the backend expects the input objects to the start_container method to have at least.

        The list should contain tuples in the form: (name, type)
        """
        raise NotImplementedError

    def restart_container(self, container, **kwargs):
        """
        Restart the container.

        If the concret backend has a native restart implementation, this method should
        be overriden, since the default implementation does two simple start/stop calls.

        :param container: The container to restart.
        """
        self.stop(force=kwargs.get('force', False))
        self.start()

    def start_container(self, container):
        """
        Start the container.

        :param container: The container to start.
        """
        raise NotImplementedError

    def stop_container(self, container, **kwargs):
        """
        Stop the container.

        :param container: The container to stop.
        """
        raise NotImplementedError


class CloneableContainerBackend(ContainerBackend):

    """
    Extended ContainerBackend providing cloning functionality.

    The cloneable container backend extends the regular container backend
    by providing a way to duplicate (clone) existing containers.
    """

    def clone_container(self, container, **kwargs):
        """
        Clone the container and returns the newly created one (clone).

        :param container: The container to clone.
        """
        raise NotImplementedError


class ImageBasedContainerBackend(ContainerBackend):

    """
    Extended ContainerBackend providing image-based containers.

    The image based container backend interface can be implemented by container backends
    to signalize that they are image/template based.
    """

    def create_image(self, specification, **kwargs):
        """
        Create a new image from the specification.

        :param specification: The specification for the new image.
        """
        raise NotImplementedError

    def delete_image(self, image, **kwargs):
        """
        Delete the container image.

        :param image: The image to delete.
        """
        raise NotImplementedError

    def get_image(self, image, **kwargs):
        """
        Get information about the requested image.

        :param image: The image to get.
        """
        raise NotImplementedError

    def get_images(self, **kwargs):
        """
        Get a list of available container images.
        """
        raise NotImplementedError

    def get_required_image_creation_fields(self):
        """
        Get a list of fields the backend expects the input objects to the create_image method to have at least.

        The list should contain tuples in the form: (name, type)
        """
        raise NotImplementedError

    def image_exists(self, image):
        """
        Check if the image exists on the backend.

        :param image: The image to check for.
        """
        raise NotImplementedError


class SnapshotableContainerBackend(ContainerBackend):

    """
    Extended ContainerBackend providing snapshot functionality.

    The snapshotable container backend extends the regular container backend
    by providing a way to snapshot/commit an existing container.
    """

    def container_snapshot_exists(self, container, snapshot, **kwargs):
        """
        Check if a snapshot with the given name exists for the container.

        :param container: The container to check.
        :param name: The name of the snapshot to check.
        """
        raise NotImplementedError

    def create_container_snapshot(self, container, specification, **kwargs):
        """
        Create a snapshop of the container.

        Implementations are free to either use the specification argument or kwargs
        for input arguments.
        Required fields should however be included in the specification.

        :param container: The container to snapshot.
        :param specification: The specification of the to be created snapshot.
        """
        raise NotImplementedError

    def delete_container_snapshot(self, container, snapshot, **kwargs):
        """
        Delete the container's snapshot.

        :param container: The container to act on.
        :param snapshot: The snapshot to delete.
        """
        raise NotImplementedError

    def get_container_snapshot(self, container, snapshot, **kwargs):
        """
        Get information about the container's snapshot.

        :param container: The container to get the snapshots for.
        :param snapshot: The snapshot to get information for.
        """
        raise NotImplementedError

    def get_container_snapshots(self, container, **kwargs):
        """
        Get a list of snapshots for the given container.

        :param container: The container to get the snapshots for.
        """
        raise NotImplementedError

    def get_required_snapshot_creation_fields(self):
        """
        Get a list of fields the backend expects the input objects to the create_container_snapshot method to have at least.

        The list should contain tuples in the form: (name, type)
        """
        raise NotImplementedError

    def restore_container_snapshot(self, container, snapshot, **kwargs):
        """
        Restore the container's snapshot.

        :param container: The container to restore.
        :param snapshot: The snapshot to restore.
        """
        raise NotImplementedError


class SuspendableContainerBackend(ContainerBackend):

    """
    Extended ContainerBackend providing suspend/resume functionality.

    The suspendable container backend adds suspend/resume capabilities to
    the regular container backend. Other than start/stop, these two operations
    to not really stop a container but actually freeze it.
    """

    """
    String to be used in the 'status' field for a stopped container.
    """
    STATUS_SUSPENDED = 'suspended'

    def container_is_suspended(self, container, **kwargs):
        """
        Check if the container is suspended.

        :param container: The container to check.
        """
        raise NotImplementedError

    def resume_container(self, container, **kwargs):
        """
        Resume a suspended container.

        :param container: The container to resume.
        """
        raise NotImplementedError

    def suspend_container(self, container, **kwargs):
        """
        Suspend a running container.

        :param container: The container to resume.
        """
        raise NotImplementedError


class GroupBackend(Backend):

    """
    The GroupBackend is used to abstract group management backends like LDAP.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    """

    """
    Key to be used in returns as unique identifier for the group.
    """
    FIELD_GROUP_PK = 'pk'

    def add_user_to_group(self, user, group, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def connect(self, credentials, **kwargs):
        """
        Establish the connection to the group backend with the given credentials.

        :param credentials: The login credentials for the backend.
        """
        raise NotImplementedError

    def create_group(self, specification, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def delete_group(self, group, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def disconnect(self, **kwargs):
        """
        Disconnect from the group backend server.
        """
        raise NotImplementedError

    def get_required_group_creation_fields(self):
        """
        Get a list of fields the backend expects the input objects to the create_group method to have at least.

        The list should contain tuples in the form: (name, type)
        """
        raise NotImplementedError

    def get_users_by_group(self, group, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def remove_user_from_group(self, user, group, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def rename_group(self, group, new_name, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError


class StorageBackend(Backend):

    """
    The storage backend component is used for users' home directories, publications and shared folders.

    It therefor abstracts basic operations on the filesystem like creating directories, setting owners etc.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    All implementations are required to accept the 'base_dir' argument in its constructor.
    """

    def __init__(self, base_dir):
        """
        Initialize a new storage backend instance that will work within 'base_dir'.

        :param base_dir: The base directory within which should be worked.
        """
        if not os.path.exists(base_dir):
            raise DirectoryNotFoundError("Base directory does not exist.")

        self.base_dir = base_dir

    def dir_exists(self, dir_name, **kwargs):
        """
        Check if the directory with the given name exists.

        :param dir_name: The name of the directory to check.
        """
        raise NotImplementedError

    def get_dir_group(self, dir_name, **kwargs):
        """
        Get the group identifier of the group owning the directory.

        :param dir_name: The directory to get the group for.
        """
        raise NotImplementedError

    def get_dir_mode(self, dir_name, **kwargs):
        """
        Get the direcories access modes.

        :param dir_name: The directory to get the mode for.
        """
        raise NotImplementedError

    def get_dir_owner(self, dir_name, **kwargs):
        """
        Get the user identifier of the user owning the directory.

        :param dir_name: The directory to get the owner for.
        """
        raise NotImplementedError

    def get_full_dir_path(self, dir_name, **kwargs):
        """
        Get the absolute/full path for the directory.

        :param dir_name: The directory to get the path for.
        """
        raise NotImplementedError

    def mk_dir(self, dir_name, **kwargs):
        """
        Create a directory with the given name.

        :param dir_name: The name of the directory to create.
        """
        raise NotImplementedError

    def rm_dir(self, dir_name, **kwargs):
        """
        Delete the directory from the storage backend.

        :param dir_name: The name of the directory to delete.
        """
        raise NotImplementedError

    def set_dir_group(self, dir_name, group, **kwargs):
        """
        Set the directory's primary group.

        :param dir_name: The directory to set the group on.
        :param group: The group to set as primary group.
        """
        raise NotImplementedError

    def set_dir_mode(self, dir_name, mode, **kwargs):
        """
        Set the directory's access mode.

        :param dir_name: The directory to set the group on.
        :param mode: The access mode to set.
        """
        raise NotImplementedError

    def set_dir_owner(self, dir_name, owner, **kwargs):
        """
        Set the directory's owner.

        :param dir_name: The directory to set the group on.
        :param owner: The user to set as an owner.
        """
        raise NotImplementedError


class UserBackend(Backend):

    """
    The UserBackend is used to abstract user management backends like LDAP.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    """

    """
    Key to be used in returns as unique identifier for the user.
    """
    FIELD_USER_PK = 'pk'

    def connect(self, credentials, **kwargs):
        """
        Establish the connection to the user backend with the given credentials.

        :param credentials: The login credentials for the backend.
        """
        raise NotImplementedError

    def create_user(self, specification, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def delete_user(self, user, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def disconnect(self, **kwargs):
        """
        Disconnect from the user backend server.
        """
        raise NotImplementedError

    def get_required_user_creation_fields(self):
        """
        Get a list of fields the backend expects the input objects to the create_user method to have at least.

        The list should contain tuples in the form: (name, type)
        """
        raise NotImplementedError

    def get_user(self, user, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def get_users(self, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def rename_user(self, user, new_name, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def set_user_password(self, user, password, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def user_exists(self, user):
        """
        TODO: write doc.
        """
        try:
            self.get_user(user)
            return True
        except UserNotFoundError:
            return False

    def validate_login(self, user, credentials, **kwargs):
        """
        Validate that the given user exists and the credentials (e.g. password) are correct.

        :param user: The user to validate.
        :param credentials: The credentials identifiying the user.
        """
        raise NotImplementedError
