import six
from datarobot.client import get_client
from datarobot.utils import SetupFieldsMetaclass, encode_utf8_if_py2, from_api


class Blueprint(six.with_metaclass(SetupFieldsMetaclass, object)):
    _client = None
    _fields = frozenset(['id', 'processes', 'model_type',
                         'project_id'])

    def __init__(self, data):
        self.id = None
        self.processes = None
        self.model_type = None
        self.project_id = None

        self._client = get_client()  # pragma:no cover
        self._data = data
        if isinstance(data, dict):
            self._set_up(from_api(data))
        else:
            raise ValueError

    def __repr__(self):
        return encode_utf8_if_py2(u'Blueprint({})'.format(self.model_type))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def _set_up(self, data):
        for k, v in six.iteritems(data):
            if k in self._fields:
                setattr(self, k, v)
