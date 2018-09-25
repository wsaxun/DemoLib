import threading

_request_store = threading.local()

def get_current():
    return getattr(_request_store,'context',None)

class RequestContext(object):
    def __init__(self,
                 request_id,
                 project_id,
                 user_id=None,
                 is_admin=None,
                 **kwargs):
        self.request_id = request_id
        self.project_id = project_id

        self.user_id = user_id
        self.is_admin = is_admin

        # if not request_id:
        #     request_id = generate_request_id()
        self.request_id = request_id

        if not get_current():
            self.update_store()

    def update_store(self):
        _request_store.context = self

    def to_dict(self):
        """Return a dictionary of context attributes."""

        return {'user_id': self.user_id,
                'request_id': self.request_id,
                'project_id':self.project_id,
                'is_admin':self.is_admin,
                'tenant':self.tenant,
                }

    @property
    def tenant(self):
        return self.project_id
