
from guide_search.esearch import Esearch

from guide_search.exceptions import (
    BadRequestError,            # 400
    ResourceNotFoundError,      # 404
    ConflictError,              # 409
    PreconditionError,          # 412
    ServerError,                # 500
    ServiceUnreachableError,    # 503
    UnknownError,               # unexpected http response
    CommitError,
    JSONDecodeError,
    ValidationError)

__version__ = '0.0.5'
__author__ = 'John Pickerill <john.pickerill@landregistry.gov.uk>'
__all__ = ['Esearch', 'ResourceNotFoundError']
