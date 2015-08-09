from ipynbsrv.contract.errors import DirectoryNotFoundError
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
    Status for the backend if everything is working.
    """
    BACKEND_STATUS_OK = 0

    """
    Status for the backend if it is stopped (i.e. the backend is a daemon).
    """
    BACKEND_STATUS_STOPPED = 1

    """
    Status for the backend if it doesn't work due to an error.
    """
    BACKEND_STATUS_ERROR = 2

    """
    Key to be used in the return of `create_container` for the created container
    if an image has been created for the clone.
    """
    CONTAINER_KEY_CLONE_CONTAINER = 'container'

    """
    Key to be used in the return of `create_container` for the created image (if any).
    """
    CONTAINER_KEY_CLONE_IMAGE = 'image'

    """
    Key to be used for the value storing the status (see below) of the container.
    """
    CONTAINER_KEY_STATUS = 'status'

    """
    String to be used in the 'status' field for a running container.
    """
    CONTAINER_STATUS_RUNNING = 'running'

    """
    String to be used in the 'status' field for a stopped container.
    """
    CONTAINER_STATUS_STOPPED = 'stopped'

    """
    Key to be used in returns as unique identifier for the resource.
    """
    KEY_PK = 'pk'

    """
    Key to be used for the value storing the address of the port mapping.
    """
    PORT_MAPPING_KEY_ADDRESS = 'address'

    """
    Key to be used for the value storing the external port of the port mapping.
    """
    PORT_MAPPING_KEY_EXTERNAL = 'external'

    """
    Key to be used for the value storing the internal port of the port mapping.
    """
    PORT_MAPPING_KEY_INTERNAL = 'internal'

    """
    Key to be used for the value storing the volume/bind mount source location.
    """
    VOLUME_KEY_SOURCE = 'source'

    """
    Key to be used for the value storing the volume/bind mount target location.
    """
    VOLUME_KEY_TARGET = 'target'

    def container_exists(self, container, **kwargs):
        """
        Check if the given container exists in the backend.

        :param container: The container to check.

        :return bool `True` if the container exists, `False` otherwise.
        """
        raise NotImplementedError

    def container_image_exists(self, image):
        """
        Check if the image exists on the backend.

        :param image: The image to check for.

        :return bool `True` if the image exists, `False` otherwise.
        """
        raise NotImplementedError

    def container_is_running(self, container, **kwargs):
        """
        Return true if the container is running.

        :param container: The container to check.

        :return bool `True` if the container is running, `False` otherwise.
        """
        raise NotImplementedError

    def create_container(self, username, uid, name, ports, volumes,
                         cmd=None, base_url=None, image=None, clone_of=None, **kwargs):
        """
        Create a new container instance.

        Either `image` or `clone_of` will be set.
        If `clone_of` is set, the new container needds to be based on that one.
        If the backend does not support native cloning and an image is created for that purpose,
        the returned value needs to be modified so it returns a `dict` with the fields
        `ContainerBackend.CONTAINER_KEY_CLONE_CONTAINER` and `ContainerBackend.CONTAINER_KEY_CLONE_IMAGE` where
        each of this fields has the value of `get_container` resp. `get_container_image`.

        :param username: The username of the container owner.
        :param uid: The user ID of the container owner.
        :param name: The name of the to be created container.
        :param ports: The ports that need to be available from the outside.
        :param volumes: The volumes to mount inside the container.
        :param cmd: An optional command to execute inside the container.
        :param base_url: If the container/image has a public exposed port, this is the base url the
                         exposed service should listen on. It's something in the form of
                         /ct/<encoded-IP-and-port>. This is required because the container is accessd
                         via a reverse proxy.
        :param image: The bootstrap image/template to use.
        :param clone_of: The optional PK of the container the to be created one is a clone of.

        :return The created container, as it would be returned with `get_container`.
        """
        raise NotImplementedError

    def create_container_image(self, container, name, **kwargs):  # TODO: arguments
        """
        Create a new image based on `container` with name `name`.

        :param container: The container acting as a base for the image.
        :param name: The name of the image to create.

        :return The created image, as it would be returned with `get_container_image`.
        """
        raise NotImplementedError

    def delete_container(self, container, **kwargs):
        """
        Delete the container.

        :param container: The container to delete.
        """
        raise NotImplementedError

    def delete_container_image(self, image, **kwargs):
        """
        Delete the container image.

        :param image: The image to delete.
        """
        raise NotImplementedError

    def exec_in_container(self, container, cmd, **kwargs):
        """
        Execute the given command inside the container.

        :param container: The container to execute the command in.
        :param cmd: The command to execute.

        :return str The output returned by the command.
        """
        raise NotImplementedError

    def get_container(self, container, **kwargs):
        """
        Get information about the requested container.

        :param container: The container to get the information of.

        :return dict A dict describing the container.
                     At least all the `ContainerBackend.KEY_*` and `ContainerBackend.CONTAINER_KEY_*` field
                     must be in this dict.
        """
        raise NotImplementedError

    def get_container_image(self, image, **kwargs):
        """
        Get information about the requested image.

        :param image: The image to get.

        :return dict A dict describing the image.
                     At least all the `ContainerBackend.KEY_*` and `ContainerBackend.CONTAINER_KEY_*` field
                     must be in this dict.
        """
        raise NotImplementedError

    def get_container_images(self, **kwargs):
        """
        Get a list of available container images.

        :return list A list of all images (each entry as with `get_image`).
        """
        raise NotImplementedError

    def get_container_logs(self, container, **kwargs):
        """
        Get the logging output of the container.

        :param container: The container to get the information of.

        :return list The list of log messages for this container.
        """
        raise NotImplementedError

    def get_containers(self, only_running=False, **kwargs):
        """
        Get a list of all containers.

        :param only_running: If true, only running containers are returned.

        :return list A list of all containers (each entry as with `get_container`).
        """
        raise NotImplementedError

    def get_status(self):
        """
        Get the status of the container backend.

        The returned value must be one of the BACKEND_STATUS_* fields.
        If determinating the status fails, no exception should be thrown - never.

        :return ContainerBackend.STATUS_* The container backend's status.
        """
        raise NotImplementedError

    def restart_container(self, container, **kwargs):
        """
        Restart the container.

        If the concret backend has a native restart implementation, this method should
        be overriden, since the default implementation does two simple start/stop calls.

        :param container: The container to restart.
        """
        self.stop_container(container)
        self.start_container(container)

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


class SnapshotableContainerBackend(ContainerBackend):

    """
    Extended ContainerBackend providing snapshot functionality.

    The snapshotable container backend extends the regular container backend
    by providing a way to snapshot/commit an existing container.
    """

    def container_snapshot_exists(self, snapshot, **kwargs):
        """
        Check if a snapshot with the given name exists for the container.

        :param snapshot: The snapshot to check.

        :return bool `True` if the snapshot exists, `False` otherwise.
        """
        raise NotImplementedError

    def create_container_snapshot(self, container, name, **kwargs):
        """
        Create a snapshop of the container.

        The `name` is passed in as entered by the user.
        Concreate backends need to ensure uniqueness is garanteed for: (`container`, `name`).

        :param container: The container to snapshot.
        :param name: The name of the to be created snapshot.

        :return dict The container snapshot (as it would be returned with `get_container_snapshot`).
        """
        raise NotImplementedError

    def delete_container_snapshot(self, snapshot, **kwargs):
        """
        Delete the container's snapshot.

        :param snapshot: The snapshot to delete.
        """
        raise NotImplementedError

    def get_container_snapshot(self, snapshot, **kwargs):
        """
        Get information about the container's snapshot.

        :param snapshot: The snapshot to get information for.

        :return dict A dict describing the container snapshot.
                     At least all the `ContainerBackend.KEY_*` fields must be in this dict.
        """
        raise NotImplementedError

    def get_container_snapshots(self, **kwargs):
        """
        Get a list of containers' snapshots.

        :return list A list of all containers' snapshots (each entry as with `get_container_snapshot`).
        """
        raise NotImplementedError

    def get_containers_snapshots(self, container, **kwargs):
        """
        Get a list of the container's snapshots.

        :return list A list of the container's snapshots (each entry as with `get_container_snapshot`).
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
    CONTAINER_STATUS_SUSPENDED = 'suspended'

    def container_is_suspended(self, container, **kwargs):
        """
        Check if the container is suspended.

        :param container: The container to check.

        :return bool `True` if the container is suspended, `False` otherwise.
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

        :param container: The container to suspend.
        """
        raise NotImplementedError


class GroupBackend(Backend):

    """
    The GroupBackend is used to abstract group management backends like LDAP.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    """

    """
    Key to be used in returns for the unique ID belonging to the group.

    Most of the time, this might be the same as FIELD_GROUP_PK.
    """
    FIELD_ID = 'id'

    """
    Key to be used in returns as unique identifier for the group.
    """
    FIELD_PK = 'pk'

    def add_group_member(self, group, user, **kwargs):
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

    def create_group(self, gid, name, **kwargs):
        """
        Create a new group on the backend.

        :param gid: The group's ID.
        :param name: The group's name.
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

    def get_group(self, group, **kwargs):
        """
        Get information about a specific group.

        :param group: The group to get the information for.
        """
        raise NotImplementedError

    def get_group_members(self, group, **kwargs):
        """
        Get a list of all members within the given group.

        :param group: The group to get the members of.
        """
        raise NotImplementedError

    def get_groups(self, **kwargs):
        """
        Get a list of all groups.
        """
        raise NotImplementedError

    def group_exists(self, group, **kwargs):
        """
        Check if the group exists.

        :param group: The group to check existance of.
        """
        raise NotImplementedError

    def is_group_member(self, group, user, **kwargs):
        """
        Check if the user is a member of the given group.

        :param group: The group to check membership of.
        :param user: The user to check.
        """
        raise NotImplementedError

    def remove_group_member(self, group, user, **kwargs):
        """
        TODO: write doc.
        """
        raise NotImplementedError

    def remove_user_from_all_groups(self, user, **kwargs):
        """
        Remove the user from all groups he belongs to.

        :param user: The user for which all memberships should be removed.
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

    def get_dir_gid(self, dir_name, **kwargs):
        """
        Get the group identifier (numeric) of the group owning the directory.

        :param dir_name: The directory to get the group for.
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

    def get_dir_uid(self, dir_name, **kwargs):
        """
        Get the user identifier (numeric) of the user owning the directory.

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

    def rm_dir(self, dir_name, recursive=False, **kwargs):
        """
        Delete the directory from the storage backend.

        :param dir_name: The name of the directory to delete.
        :param recursive: Either to delete recursive or not.
        """
        raise NotImplementedError

    def set_dir_gid(self, dir_name, gid, **kwargs):
        """
        Set the directory's primary group by numeric ID.

        :param dir_name: The directory to set the group on.
        :param gid: The numeric group ID.
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

    def set_dir_uid(self, dir_name, uid, **kwargs):
        """
        Set the directory's owner by numeric ID.

        :param dir_name: The directory to set the group on.
        :param uid: The user's numeric ID.
        """
        raise NotImplementedError


class UserBackend(Backend):

    """
    The UserBackend is used to abstract user management backends like LDAP.

    All methods accept kwargs so individual data can be passed to conrete implementations.
    """

    """
    Key to be used in returns for the unique ID belonging to the user.

    Most of the time, this might be the same as FIELD_USER_PK.
    """
    FIELD_ID = 'id'

    """
    Key to be used in returns as unique identifier for the user.
    """
    FIELD_PK = 'pk'

    def auth_user(self, user, password, **kwargs):
        """
        Validate that the given user exists and the password is correct.

        If the user does not exist, an `ipynbsrv.contract.errors.UserNotFoundError` should be raised.
        If the authentication failed, an an `ipynbsrv.contract.errors.AuthenticationError` should be raised.
        If the authentication went well, the user should be returned.

        :param user: The user to validate.
        :param password: The user's password.
        """
        raise NotImplementedError

    def connect(self, credentials, **kwargs):
        """
        Establish the connection to the user backend with the given credentials.

        :param credentials: The login credentials for the backend.
        """
        raise NotImplementedError

    def create_user(self, uid, username, password, gid, home_directory, **kwargs):
        """
        Create a new user on the backend.

        The user details are taken from `specification` which must include at least
        the fields returned by the get_required_user_creation_fields.

        :param uid: The user's ID.
        :param username: The username identifying the user.
        :param password: The user's login password.
        :param gid: The user's primary group's ID.
        :param home_directory: The user's home directory path.
        """
        raise NotImplementedError

    def delete_user(self, user, **kwargs):
        """
        Delete the user from the backend.

        :param user: The user to delete.
        """
        raise NotImplementedError

    def disconnect(self, **kwargs):
        """
        Disconnect from the user backend server.
        """
        raise NotImplementedError

    def get_user(self, user, **kwargs):
        """
        Get information about a specific user.

        :param user: The user to get the information for.
        """
        raise NotImplementedError

    def get_users(self, **kwargs):
        """
        Get a list of all users the backend stores.
        """
        raise NotImplementedError

    def set_user_password(self, user, password, **kwargs):
        """
        Set/update the user's password stored in the backend.

        :param user: The user for which the credentials should be updated.
        :param credential: The new password.
        """
        raise NotImplementedError

    def user_exists(self, user):
        """
        Check if the user exists.

        :param user: The user to check existance of.
        """
        raise NotImplementedError
