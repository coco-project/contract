class Algorithm(object):

    """
    Interface for all kind of algorithms used by ipynbsrv.
    """

    pass


class ServerSelectionAlgorithm(Algorithm):

    """
    """

    def choose_server(self, **kwargs):
        """
        """
        raise NotImplementedError
