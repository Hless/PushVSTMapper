''' Parameter model '''

class Parameter():
    ''' Param model '''

    def __init__(self, unique_id, title, param_type):
        self.unique_id = unique_id
        self.title = title
        self.param_type = param_type
        self._param = None

    @classmethod
    def from_dict(cls, data):
        ''' Convert param dictionary to param class  '''

        # Intantiate bank with params
        bank = cls(data['id'], data['title'], data['type'])
        return bank


    def attach_native(self, param):
        ''' Attach native live parameter to this obj '''
        self._param = param
