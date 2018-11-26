# Ubermap Devices patches
# Applies "monkey patches" to methods within Live's Push implementation to support custom parameter mapping
# https://github.com/tomduncalf/ubermap

# Ubermap
from Ubermap import UbermapDevices
from Ubermap.UbermapLibs import log, config
import inspect


def apply_ubermap_patches(is_v1):
    log.info("Applying UbermapDevices patches")

    apply_log_method_patches()
    apply_banking_util_patches()
    apply_device_component_patches(is_v1)
    apply_device_parameter_bank_patches()
    apply_device_parameter_adapater_patches()
    if not is_v1:
        apply_device_visualisation_patches()

# Create singleton UbermapDevices instance
ubermap = UbermapDevices.UbermapDevices()
ubermap_config = config.load('global')

def apply_log_method_patches():
    # Log any method calls made to the object - useful for tracing execution flow
    # Use like: DeviceComponent.__getattribute__ = __getattribute__
    def __getattribute__(self, name):
        returned = object.__getattribute__(self, name)
        if inspect.isfunction(returned) or inspect.ismethod(returned):
            log.info('Called ' + self.__class__.__name__ + '::' + str(returned.__name__))
        return returned

############################################################################################################

def patch_method(obj):
    def decorator(func):
        _orig = None
        try:
            _orig = getattr(obj, func.__name__)
        except AttributeError as e:
            pass


        def wrapper(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
                #log.info(str(result))
            except Exception as e:
                log.error(str(e))

            if result:
                return result
            else:
                #log.info("Result is lacking, running orig fn")
                return _orig(*args, **kwargs) if _orig else None

        setattr(obj, func.__name__, wrapper)

        return func
    return decorator

# BankingUtil
from pushbase import banking_util

def apply_banking_util_patches():

    # device_bank_names - return Ubermap bank names if defined, otherwise use the default
    @patch_method(banking_util)
    def device_bank_names(device, bank_size = 8, definitions = None):
        ubermap_banks = ubermap.get_custom_device_banks(device)
        if ubermap_banks:
            return ubermap_banks
        else:
            ubermap.dump_device(device)
            return False


    # device_bank_count - return Ubermap bank count if defined, otherwise use the default
    @patch_method(banking_util)
    def device_bank_count(device, bank_size = 8, definition = None, definitions = None):
        ubermap_banks = ubermap.get_custom_device_banks(device)
        if ubermap_banks:
            return len(ubermap_banks)

############################################################################################################

# DeviceParameterBank
from pushbase.device_parameter_bank import DeviceParameterBank

def apply_device_parameter_bank_patches():
    # _collect_parameters - this method is called by _update_parameters to determine whether we should
    # notify that parameters have been updated or not, but is hardcoded to use the default bank size
    # (i.e. full banks of 8), so Ubermap banks with <8 parameters cause later banks to break. Instead return
    # the relevant Ubermap bank if defined, otherwise use the default.
    @patch_method(DeviceParameterBank)
    def _collect_parameters(self):
        ubermap_banks = ubermap.get_custom_device_banks(self._device)
        if ubermap_banks:
            bank = ubermap_banks[self._get_index()]
            return bank

############################################################################################################


def apply_device_component_patches(is_v1):
    # _get_provided_parameters - return Ubermap parameter names if defined, otherwise use the default

    # DeviceComponent
    from pushbase.device_component import DeviceComponent
    from pushbase.parameter_provider import ParameterInfo

    if is_v1:
        from Push.parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity
    else:
        from Push2.parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity

    def _get_parameter_info(self, parameter):
        if not parameter:
            return None
        return ParameterInfo(parameter=parameter, name=parameter.custom_name, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter), fine_grain_encoder_sensitivity=fine_grain_parameter_mapping_sensitivity(parameter))

    @patch_method(DeviceComponent)
    def _get_provided_parameters(self):
        ubermap_params = ubermap.get_custom_device_params(self._decorated_device)
        if ubermap_params:
            param_bank = ubermap_params[self._bank.index]
            param_info = map(lambda parameter: _get_parameter_info(self, parameter), param_bank)
            return param_info


def apply_device_visualisation_patches():
    return
    '''
    from Push2.device_component_provider import DEVICE_COMPONENT_MODES, DeviceComponentProvider
    from Push2.device_decorator_factory import DeviceDecoratorFactory
    from Ubermap.UbermapVisualisation import UbermapDeviceDecorator, UbermapDeviceComponent

    @patch_method(DeviceComponentProvider)
    def _set_device(self, device):
        #if device.class_name == "PluginDevice":
            #device.class_name = "Operator"

        #name = device.class_name if device and device.class_name in self._device_component_modes else 'Generic'

        #log.info("DEVICE NAME: " + str(name))
        #d = dir(device)

        log.info("DEVICE")

        r = {}
        for k in dir(device):
            if k.startswith("__"):
                continue
            r[k] = getattr(device,k)


        log.info(r)

        return False

    # Hook device mode and decorator into core functions for plugindevices
    DeviceDecoratorFactory.DECORATOR_CLASSES['PluginDevice'] = UbermapDeviceDecorator

    log.info(str(DeviceDecoratorFactory.DECORATOR_CLASSES))
    DEVICE_COMPONENT_MODES["PluginDevice"] = UbermapDeviceComponent

    '''



############################################################################################################

# DeviceParameterAdapter
from ableton.v2.base import listenable_property
from Push2.model.repr import DeviceParameterAdapter
from math import floor

def apply_device_parameter_adapater_patches():
    def name(self):
        if hasattr(self._adaptee, 'custom_name'):
            return self._adaptee.custom_name
        else:
            return self._adaptee.name

    DeviceParameterAdapter.name = listenable_property(name)

    def valueItems(self):
        if getattr(self._adaptee, 'custom_parameter_values', None):
            return self._adaptee.custom_parameter_values
        else:
            if self._adaptee.is_quantized:
                return self._adaptee.value_items
            return []

    DeviceParameterAdapter.valueItems = listenable_property(valueItems)

    def value_to_start_point_index(value, start_points):
        log.debug("start_points: " + str(start_points) + ", len: " + str(len(start_points)) + ", value: " + str(value))
        for index, start_point in enumerate(start_points):
            log.debug("index: " + str(index) + ", start_point: " + str(start_point) + ", value: " + str(value))
            if value > start_point and (index == len(start_points) - 1 or value < start_points[index + 1]):
                log.debug("Input value: " + str(value) + ", output index: " + str(index) + " with custom start points")
                return index

    def value_to_index(value, parameter_values):
        values_len = len(parameter_values)
        value_index = floor(value * values_len)

        # If the value is 1.00 we don't want an off by one error
        value_index = value_index - 1 if value_index == values_len else value_index

        log.debug("Input value: " + str(value) + ", output index: " + str(value_index))

        return value_index

    def value(self):
        if getattr(self._adaptee, 'custom_parameter_values', None):
            if getattr(self._adaptee, 'custom_parameter_start_points', None):
                return value_to_start_point_index(self._adaptee.value, self._adaptee.custom_parameter_start_points)
            else:
               return value_to_index(self._adaptee.value, self._adaptee.custom_parameter_values)
        else:
            return self._adaptee.value

    DeviceParameterAdapter.value = listenable_property(value)


'''
    self.crop_option = DeviceTriggerOption(name='Crop', callback=partial(call_simpler_function, 'crop'))

    self.loop_option = DeviceOnOffOption(name='Loop', property_host=get_parameter_by_name(self, 'S Loop On'))
    self.filter_slope_option = DeviceSwitchOption(name='Filter Slope', parameter=get_parameter_by_name(self, 'Filter Slope'))

'''
