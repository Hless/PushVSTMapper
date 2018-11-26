from Push2.device_component import DeviceComponentWithTrackColorViewData, make_vector, ButtonRange
from Push2.visualisation_settings import VisualisationGuides
from ableton.v2.base import liveobj_valid
from pushbase.decoration import LiveObjectDecorator
from Push2.device_component_provider import DeviceComponentProvider, DEVICE_COMPONENT_MODES
from ableton.v2.base import const, EventObject, listenable_property, listens, liveobj_valid
from pushbase.internal_parameter import EnumWrappingParameter
from Ubermap.UbermapLibs import log, config
from collections import namedtuple

from Push2.operator import OperatorDeviceComponent, OperatorDeviceDecorator

import re
def _object_as_dict(obj):
    if obj:
        return obj.__dict__
    else:
        return {}


BankConfiguration = namedtuple('BankConfiguration', [
 'name_function', 'button_range'])

'''
def apply_check_function_patch():
    OperatorDeviceComponent.ENVELOPE_PREFIXES = [
     'Ae', 'Be', 'Ce', 'De', 'Fe', 'Le', 'Pe']
    _orig = OperatorDeviceComponent._envelope_visualisation_data
    def _envelope_visualisation_data(self):


        config = self._bank_configuration.get(self._bank.index, BankConfiguration(const(''), ButtonRange(0, 0)))
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed
                             ]
        shown_features = set(['AttackLine', 'DecayLine', 'SustainLine', 'ReleaseLine'])
        for parameter_info in self.parameters:
            extend_with_envelope_features_for_parameter(shown_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

        log.info(shown_features)
        focused_features = set()
        for parameter_info in touched_parameters:
            extend_with_envelope_features_for_parameter(focused_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

        return {'EnvelopeName': config.name_function(),
           'EnvelopeLeft': VisualisationGuides.light_left_x(config.button_range.left_index),
           'EnvelopeRight': VisualisationGuides.light_right_x(config.button_range.right_index),
           'EnvelopeShow': make_vector(list(shown_features)),
           'EnvelopeFocus': make_vector(list(focused_features)),
           'FilterVisible': self._should_show_filter_visualisation(),
           'FilterLeft': VisualisationGuides.light_left_x(1),
           'FilterRight': VisualisationGuides.light_right_x(3),
           'FilterFocus': self._is_filter_parameter_touched()}

    OperatorDeviceComponent._envelope_visualisation_data = _envelope_visualisation_data
'''

# def apply_check_function_patch():

ENVELOPE_FEATURES_FOR_PARAMETER = {'Attack': set(['AttackLine', 'AttackNode', 'DecayLine']),
   'Decay': set(['DecayLine', 'DecayNode', 'SustainLine']),
   'Sustain': set(['DecayLine', 'DecayNode', 'SustainLine', 'SustainNode', 'ReleaseLine']),
   'Release': set(['ReleaseLine', 'ReleaseNode']),
   'Init': set(['InitNode', 'AttackLine']),
   'Initial': set(['InitNode', 'AttackLine']),
   'Peak': set(['AttackLine', 'AttackNode', 'DecayLine']),
   'End': set(['ReleaseLine', 'ReleaseNode']),
   'Final': set(['ReleaseLine', 'ReleaseNode']),
   'A Slope': set(['AttackLine']),
   'D Slope': set(['DecayLine']),
   'R Slope': set(['ReleaseLine']),
   'Fade In': set(['FadeInLine', 'FadeInNode', 'SustainLine']),
   'Fade Out': set(['FadeOutLine', 'FadeOutNode'])}

def normalize_envelope_parameter_name(parameter_name, envelope_prefixes):
    find_envelope_prefix = re.compile(('^({}) ').format(('|').join(envelope_prefixes)))
    return re.sub(find_envelope_prefix, '', parameter_name)


def extend_with_envelope_features_for_parameter(features, parameter, envelope_prefixes):
    if liveobj_valid(parameter):
        normalized_name = normalize_envelope_parameter_name(parameter.name, envelope_prefixes)
        try:
            features |= ENVELOPE_FEATURES_FOR_PARAMETER[normalized_name]
        except KeyError:
            pass

class NotifyingList(EventObject):
    __events__ = (u'index', )

    def __init__(self, available_values, default_value=None, *a, **k):
        super(NotifyingList, self).__init__(*a, **k)
        self._index = default_value if default_value is not None else 0
        self._available_values = available_values
        return

    @property
    def available_values(self):
        return self._available_values

    def _get_index(self):
        return self._index

    def _set_index(self, value):
        if value < 0 or value >= len(self.available_values):
            raise IndexError
        self._index = value
        self.notify_index()

    index = property(_get_index, _set_index)


# This won't import properly for some obscure reason, probably only exists in >=10.0.2
ENVELOPE_FEATURES_FOR_PARAMETER = {'Attack': set(['AttackLine', 'AttackNode', 'DecayLine']),
   'Decay': set(['DecayLine', 'DecayNode', 'SustainLine']),
   'Sustain': set(['DecayLine', 'DecayNode', 'SustainLine', 'SustainNode', 'ReleaseLine']),
   'Release': set(['ReleaseLine', 'ReleaseNode']),
   'Init': set(['InitNode', 'AttackLine']),
   'Initial': set(['InitNode', 'AttackLine']),
   'Peak': set(['AttackLine', 'AttackNode', 'DecayLine']),
   'End': set(['ReleaseLine', 'ReleaseNode']),
   'Final': set(['ReleaseLine', 'ReleaseNode']),
   'A Slope': set(['AttackLine']),
   'D Slope': set(['DecayLine']),
   'R Slope': set(['ReleaseLine']),
   'Fade In': set(['FadeInLine', 'FadeInNode', 'SustainLine']),
   'Fade Out': set(['FadeOutLine', 'FadeOutNode'])}

class EnvelopeType(int):
    pass


EnvelopeType.env1 = EnvelopeType(0)
EnvelopeType.env2 = EnvelopeType(1)
EnvelopeType.env3 = EnvelopeType(2)
EnvelopeType.env4 = EnvelopeType(3)


class UbermapDeviceDecorator(OperatorDeviceDecorator):

   def __init__(self, *a, **k):
       self.available_env_values = ['Env 1', 'Env 2']
       self._envelope_types_provider = NotifyingList(available_values=self.available_env_values, default_value=EnvelopeType.env1)

       self.envelope = EnumWrappingParameter(name='Env. Type', parent=self, values_host=self._envelope_types_provider, index_property_host=self._envelope_types_provider, values_property='available_values', index_property='index', value_type=EnvelopeType)
       log.info("YES THE DECORATOR IS WOKRING")
       super(UbermapDeviceDecorator, self).__init__(*a, **k)

       self.__on_envelope_type_changed.subject = self.envelope



   @property
   def parameters(self):
       return tuple(self._live_object.parameters) + (
       self.envelope,)

   @property
   def options(self):
       return tuple()

   @listenable_property
   def envelope_type_index(self):
     return self._envelope_types_provider.index

   @listens('value')
   def __on_envelope_type_changed(self):
     self.notify_envelope_type_index()

   @property
   def selected_envelope(self):
       return self.available_env_values[self._envelope_types_provider.index]



# TODO: Inject this as a custom device for everything except base devices
class UbermapDeviceComponent(OperatorDeviceComponent):
    FILTER_PARAMETER_NAMES = [
     'Filter Type', 'Filter Freq', 'Filter Res']
    FILTER_BANK = 0
    ENVELOPE_PREFIXES = [
     'Ae', 'Be', 'Ce', 'De', 'Fe', 'Le', 'Pe']

    def __init__(self, *a, **k):
        super(UbermapDeviceComponent, self).__init__(*a, **k)
        self._bank_configuration = {
           2: BankConfiguration(const('Envelope.'), ButtonRange(2, 5))}

    def _parameter_touched(self, parameter):
        #if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            #self._decorated_device.zoom.touch_object(parameter)
        self._update_visualisation_view_data(self._visualisation_data())

    def _parameter_released(self, parameter):
        #if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            #self._decorated_device.zoom.release_object(parameter)
        self._update_visualisation_view_data(self._visualisation_data())

    def parameters_changed(self):
        self._update_visualisation_view_data(self._visualisation_data())

    def _set_bank_index(self, bank):
        super(UbermapDeviceComponent, self)._set_bank_index(bank)

        self._update_visualisation_view_data(self._visualisation_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()


    def _visualisation_data(self):
        data = self._envelope_visualisation_data()
        data.update(self._filter_visualisation_data())
        return data


    def _set_decorated_device(self, decorated_device):
        super(UbermapDeviceComponent, self)._set_decorated_device(decorated_device)
        self.__on_selected_envelope_type_changed.subject = decorated_device

    @property
    def selected_envelope_type(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.envelope_type_index
        return 0

    @property
    def selected_envelope_name(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.selected_envelope
        return "None"

    @listens('envelope_type_index')
    def __on_selected_envelope_type_changed(self):
        self._update_visualisation_view_data(self._visualisation_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @property
    def _shrink_parameters(self):
        if self._envelope_visible:
            left_button = 1
            right_button = left_button + 3
            return [ index >= left_button and index <= right_button for index in range(8)
                   ]
        if self._filter_visible:
            return [ index >= 1 and index <= 3 for index in range(8) ]
        return [
         False] * 8

    @property
    def _visualisation_visible(self):
        log.info("Visualisation visible  " + str(self._envelope_visible or self._filter_visible))

        return self._envelope_visible or self._filter_visible

    @property
    def _envelope_visible(self):
        log.info("Envelope visible " + str(self._bank != None and self._bank.index == 1))
        return self._bank != None and self._bank.index == 1

    @property
    def _filter_visible(self):
        return self._bank != None and self._bank.index == 0

    def _is_filter_parameter_touched(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed
                             ]
        return any([ parameter.parameter.name in self.FILTER_PARAMETER_NAMES for parameter in touched_parameters if liveobj_valid(parameter.parameter)
                       ])

    def _initial_visualisation_view_data(self):
        view_data = super(UbermapDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._visualisation_data())

        return view_data


    def _envelope_visualisation_data(self):
        # config = self._bank_configuration.get(self._bank.index, BankConfiguration(const(''), ButtonRange(0, 0)))
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed
                             ]
        shown_features = set(['AttackLine', 'DecayLine', 'SustainLine', 'ReleaseLine'])
        for parameter_info in self.parameters:
            extend_with_envelope_features_for_parameter(shown_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

        log.info(shown_features)
        focused_features = set()
        for parameter_info in touched_parameters:
            extend_with_envelope_features_for_parameter(focused_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

        return {'EnvelopeName': "Env1",
           'EnvelopeLeft': VisualisationGuides.light_left_x(1),
           'EnvelopeRight': VisualisationGuides.light_right_x(4),
           'EnvelopeVisible': self._envelope_visible,
           'EnvelopeShow': make_vector(list(shown_features)),
           'EnvelopeFocus': make_vector(list(focused_features))}


    def _filter_visualisation_data(self):
        left_column = 1
        right_column = left_column + 3
        return {'FilterVisible': self._filter_visible,
           'FilterLeft': VisualisationGuides.light_left_x(left_column),
           'FilterRight': VisualisationGuides.light_right_x(right_column),
           'FilterFocus': any([ button.is_pressed for index, button in enumerate(self.parameter_touch_buttons) if index >= left_column and index <= right_column
                        ])}
