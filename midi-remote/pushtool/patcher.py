'''
Patcher is responsible for monkey patching Ableton Remote methods
'''

from .common.logger import LOGGER
from .common.memoize import cached

from .common.decorators import patch_method
from .models.device import Device



def apply_patches():
    LOGGER.info("Applying PushTool patches")
    apply_banking_util_patches()
    apply_device_parameter_bank_patches()
    apply_device_component_patches()

    '''
    apply_device_component_patches(is_v1)
    apply_device_parameter_bank_patches()
    apply_device_parameter_adapater_patches()
    if not is_v1:
        apply_device_visualisation_patches()
    '''

@cached('display_name', namespace="devices")
def _memoized_loader(device, display_name):
    return Device(device)

def load_device(device):
    if device.class_name == "PluginDevice":
        return _memoized_loader(device, device.class_display_name)
    return False

def apply_banking_util_patches():
    ''' Apply bank util patches '''

    LOGGER.info("Applying BankUtil patches")
    from ableton.v2.control_surface import banking_util # pylint: disable=import-error


    @patch_method(banking_util, log_original=True)
    def device_bank_names(device, bank_size=8, definitions=None):
        ''' Find bank names, otherwise return default imlementation '''
        wrapped = load_device(device)
        if not wrapped:
            return False

        return wrapped.bank_names

    # device_bank_count - return Ubermap bank count if defined, otherwise use the default
    @patch_method(banking_util, log_original=True)
    def device_bank_count(device, bank_size=8, definition=None, definitions=None):
        ''' Find bank count, otherwise return default imlementation '''
        wrapped = load_device(device)
        if not wrapped:
            return False

        return wrapped.bank_count


def apply_device_parameter_bank_patches():
    '''
    _collect_parameters - this method is called by _update_parameters to determine whether we should
    notify that parameters have been updated or not, but is hardcoded to use the default bank size
    (i.e. full banks of 8), so Ubermap banks with <8 parameters cause later banks to break. Instead
    return the relevant Ubermap bank if defined, otherwise use the default.
    '''

    from ableton.v2.control_surface.device_parameter_bank import DeviceParameterBank  # pylint: disable=import-error

    @patch_method(DeviceParameterBank, log_original=True)
    def _collect_parameters(self):
        return False


def apply_device_component_patches():
    '''
    _get_provided_parameters - return Pushtool parameter names if defined, otherwise use the default
    '''

    # DeviceComponent
    from ableton.v2.control_surface.components import DeviceComponent # pylint: disable=import-error
    # from pushbase.parameter_provider import ParameterInfo
    # from Push2.parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity


    # def _get_parameter_info(self, parameter):
        # if not parameter:
            # return None
        # return ParameterInfo(parameter=parameter, name=parameter.custom_name, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter), fine_grain_encoder_sensitivity=fine_grain_parameter_mapping_sensitivity(parameter))

    @patch_method(DeviceComponent, log_original=True)
    def _get_provided_parameters(self):
        wrapped = load_device(self.decorate_device)
        if not wrapped:
            return False
        return False
