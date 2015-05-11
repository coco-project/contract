# Specification

## ContainerBackend

The following chapters contain a set of rules/specifications, each and every concrete container backend must fulfill to be 100% compatible with the `ipynbsrv` application.

### Method Input

- Every (non-special) interface method accepts `**kwargs` as its last argument, allowing to pass backend-specific values to the method. There is however no guarantee that this argument is set on the caller side, so strict validation is required inside the method.

### Return Values

- Methods returning container "objects (dictionaries)" must at least include all the `ContainerBackend.FIELD_*` keys in the returned dictionary.
- The value of the `ContainerBackend.FIELD_PK` field must be the unique identifier for the container and will be used to call methods operating on that container.
- The value of the `ContainerBackend.FIELD_STATUS` field must be either one of the `ContainerBackend.STATUS_*` constants or one of its subinterfaces (if any).

### Errors

- Every error raised as a result to a backend call must be wrapped inside the `ContainerBackendError` error type.