''' Bank model for returning a bank with parameters '''

from .parameter import Parameter

class Bank():
    ''' Bank model for returning a bank with parameters '''
    def __init__(self, id, name, parameters=None):
        self.id = id
        self.name = name
        self.parameters = parameters if parameters is not None else []


    @classmethod
    def from_dict(cls, data):
        ''' Convert bank dictionary to Bank class '''
        params = [Parameter.from_dict(param) for param in data['parameters']]

        # Intantiate bank with params
        bank = cls(data['name'], params)
        return bank

    def hydrated_params(self, params):
        return
