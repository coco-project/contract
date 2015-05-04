'''
The backend interface defines the representation of an external resource
like a container or storage backend or any other form of resource
that exists outside of the application's context.

Actions performed on instances of a backend should be reflected to its underlaying backend.
'''
class Backend(object):
    pass


'''
The container backend is used to abstract container/virtualization backends like
Docker or VirtualBox.
'''
class ContainerBackend(Backend):
    '''
    Returns the status of the container.

    :param container: The container to get the status of.
    '''
    def container_status(self, container):
        raise NotImplementedError

    '''
    Returns true if the container is running.

    :param container: The container to check.
    '''
    def container_is_running(self, container):
        raise NotImplementedError

    '''
    '''
    def create_container(self, container):
        raise NotImplementedError

    '''
    Deletes the container.

    :param container: The container to delete.
    :param force: If true, tries to delete the container in any case (e.g. also if it is running).
    '''
    def delete_container(self, container, force=False):
        raise NotImplementedError

    '''
    Restarts the container.

    If the concret backend has a native restart implementation, this method should
    be overriden, since the default implementation does two simple start/stop calls.

    :param container: The container to restart.
    '''
    def restart_container(self, container):
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
    :param force: If true, tries to stop the container in any case (e.g. kills it after a given timeout).
    '''
    def stop_container(self, container, force=False):
        raise NotImplementedError


'''
The cloneable container backend extends the regular container backend
by providing a way to duplicate (clone) existing containers.
'''
class CloneableContainerBackend(ContainerBackend):
    '''
    Clones the container and returns the newly created one (clone).

    :param container: The container to clone.
    '''
    def clone_container(self, container):
        raise NotImplementedError


'''
The commitable container backend extends the regular container backend
by providing a way to commit (snapshot) an existing container.
'''
class CommitableContainerBackend(ContainerBackend):
    '''
    Creates a snapshop of the container by committing it.

    :param container: The container to commit.
    '''
    def commit_container(self, container):
        raise NotImplementedError
