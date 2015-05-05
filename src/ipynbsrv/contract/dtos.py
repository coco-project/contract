class DTO(object):
    '''
    Data transfer objects (DTO) are used to carry objects between hosts/subsystems
    in a model independant way. They are for example used in ipynbsrv to have a unified
    format for messages send between different hosts (e.g. master API to host API).
    '''
    pass

    '''
    Checks if the DTO is valid as per the class' definition.
    '''
    def is_valid(self):
        raise NotImplementedError

    '''
    Validates the DTO (like is_valid) but raises errors when the validation fails.
    '''
    def validate(self):
        raise NotImplementedError


class ValidationError(Exception):
    '''
    Validation errors should be raised by DTOs if their validate method is called
    and the instance does not satisfy the validation rules.
    '''

    def __init__(self, message):
        super(ValidationError, self).__init__(message)
        self.message = message


class MissingFieldError(ValidationError):
    '''
    '''
    pass


class ContainerImageDTO(DTO):
    '''
    '''

    '''
    Initializes a new container image model with the values from the input dictionary.
    '''
    def __init__(self, values):
        # self.id = values.get('id')
        self.name = values.get('name')
        self.tag = values.get('tag')

    '''
    Returns the full identifier of this image.
    '''
    def get_full_identifier(self):
        return "%s:%s" % (self.name, self.tag)

    def is_valid(self):
        return self.name is not None and self.tag is not None

    def validate(self):
        # if not self.id:
        #     raise MissingFieldError("Container image ID not set")
        if not self.name:
            raise MissingFieldError("Container image name not set")
        if not self.tag:
            raise MissingFieldError("Container image tag name not set")


class ContainerDTO(DTO):
    '''
    '''

    '''
    Initializes a new container transfer model with the values from the input dictionary.
    '''
    def __init__(self, values):
        self.id = values.get('id')

    def is_valid(self):
        return self.id is not None

    def validate(self):
        if not self.id:
            raise MissingFieldError("Container ID not set")


class CreatableContainerDTO(DTO):
    '''
    The creatable container DTO extends the regular container DTO with
    fields (required) for the creation of a new container.
    '''

    def __init__(self, values):
        self.command = values.get('command')
        self.env = values.get('env')
        self.image = values.get('image')
        self.name = values.get('name')
        self.ports = values.get('ports')
        self.volumes = values.get('volumes')

    def is_valid(self):
        return self.command is not None and self.image is not None \
            and isinstance(self.image, ContainerImageDTO) and self.image.is_valid() \
            and self.name is not None

    def validate(self):
        if not self.image:
            raise MissingFieldError("Container image not set")
        if not isinstance(self.image, ContainerImageDTO):
            raise ValidationError("Container image not valid")
        self.image.validate()
        if not self.name:
            raise MissingFieldError("Container name not set")
