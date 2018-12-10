''' File to replace original __init__.py from the Push2 directory '''

from __future__ import absolute_import, print_function, unicode_literals

def get_capabilities():
    ''' Stub '''
    from ableton.v2.control_surface import capabilities as caps # pylint: disable=import-error
    return {
        caps.CONTROLLER_ID_KEY: caps.controller_id(
            vendor_id=10626,
            product_ids=[6503],
            model_name=u'Ableton Push 2'),
        caps.PORTS_KEY: [
            caps.inport(props=[caps.HIDDEN, caps.NOTES_CC, caps.SCRIPT]),
            caps.inport(props=[]),
            caps.outport(props=[caps.HIDDEN, caps.NOTES_CC, caps.SYNC, caps.SCRIPT]),
            caps.outport(props=[])
        ],
        caps.TYPE_KEY: u'push2',
        caps.AUTO_LOAD_KEY: True
    }


def create_instance(c_instance):
    ''' Apply patches '''
    from .push2 import Push2 # pylint: disable=import-error
    from .push2_model import Root, Sender # pylint: disable=import-error
    root = Root(sender=Sender(
        message_sink=c_instance.send_model_update,
        process_connected=c_instance.process_connected))

    from pushtool import patcher # pylint: disable=import-error
    patcher.apply_patches()

    return Push2(c_instance=c_instance, model=root)
