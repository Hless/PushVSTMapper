''' Device model, responsible for parsing and hydrating parameter configs '''

from pushtool.common.files import save_as_json, load_from_json
from pushtool.common.config import FILE_PARAMS, FILE_BANKS
from .bank import Bank

def diff_raw_parameters(new, old):
    ''' Diff new and old paramaters '''
    return len(new) is not len(old)


class DeviceConfig:
    ''' Proxy model for config '''
    banks = []

class Device:
    ''' Device model class implementation '''

    def __init__(self, device):
        self._device = device
        self.display_name = device.class_display_name
        self.chain = device.canonical_parent
        self.config = self._load_config()
        self.raw_params = self._load_raw_parameters()

    def refresh(self):
        ''' Refresh config '''
        self.config = self._load_config()

    def dump(self):
        ''' Dump config '''
        self._dump_raw_parameters()

    @property
    def bank_count(self):
        ''' Return number of banks for this device '''
        return len(self.config.banks)


    def bank_names(self):
        ''' Return all banks names as list'''
        return [bank.name for bank in self.config.banks]

    def name_for_bank(self, number=0):
        ''' Return name for bank at given index '''
        bank = self._load_bank(number)
        if bank is None:
            return "Bank {}".format(number + 1)
        return bank.name

    def parameters_for_bank(self, number=0):
        ''' Return parameters for bank at given index '''
        bank = self._load_bank(number)
        if bank is None:
            return []

        return bank.mapped_params(self._device.parameters[1:])


    def _load_bank(self, number=0):
        ''' Load bank with given number or return none '''
        if number > len(self.config.banks) - 1:
            return None

        return self.config.banks[number]

    def _load_config(self):
        ''' Load device config from json file '''
        obj = load_from_json(self.display_name, FILE_BANKS)
        config = obj if isinstance(obj, list) else {}
        banks = []
        for bank in config['banks']:
            bank.append(Bank.from_dict(bank))

        return DeviceConfig(banks=banks)

    def _load_raw_parameters(self):
        ''' Load raw parameters from the parameter json file '''
        raw = load_from_json(self.display_name, FILE_PARAMS)
        return raw if isinstance(raw, list) else []

    def _dump_raw_parameters(self):
        '''
        Dump parameters to available file after merging them
        with the current available params
        '''
        new = [param.original_name for param in self._device.parameters[1:]]
        if diff_raw_parameters(new, self.raw_params):
            save_as_json(self.display_name, FILE_PARAMS, self.raw_params)
