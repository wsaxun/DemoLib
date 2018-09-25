import uuid
import threading

_request_store = threading.local()

def generate_request_id():
    return 'req-%s' % uuid.uuid4()

def get_current():
    return getattr(_request_store,'context',None)

class RequestContext(object):
    def __init__(self,
                 tenant_id=None,
                 request_id=None,
                 overwrite=True):
        self.tenant_id = tenant_id
        self.request_id = request_id

        if not request_id:
            request_id = generate_request_id()
        self.request_id = request_id

        if overwrite or not get_current():
            self.update_store()

    def update_store(self):
        _request_store.context = self

    def to_dict(self):
        """Return a dictionary of context attributes."""

        return {'tenant': self.tenant_id,
                'request_id': self.request_id
                }

    def get_logging_values(self):
        """Return a dictionary of logging specific context attributes."""
        values = dict()
        values.update(self.to_dict())

        return values
