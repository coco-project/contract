'''
Data transfer objects (DTO) are used to carry objects between hosts/subsystems
in a model independant way. They are for example used in ipynbsrv to have a unified
format for messages send between different hosts (e.g. master API to host API).

Senders and receivers need to take care of validation themselve!
'''
class DTO(object):
    pass


class ContainerDTO(DTO):
    '''
    Initializes a new container transfer model with the values from the input dictionary.
    '''
    def __init__(self, values):
        self.id = values['id']
        self.name = values['name']
        self.image = values['image']
        # optional fields
        self.cmd = values['cmd']
        self.env = values['env']
        self.ports = values['ports']
        self.volumes = values['volumes']
