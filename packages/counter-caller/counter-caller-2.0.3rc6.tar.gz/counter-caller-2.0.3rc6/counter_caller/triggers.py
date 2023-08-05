from collections import namedtuple

Trigger = namedtuple('Trigger', ['id', 'label', 'shortcut'])

def build_triggers(definitions):
    """
    Convert a series of trigger definitions into trigger objects.

    id:         Can be most anything, but must be unique
    label:      A label to describe the trigger - keep it short
    shortcut:   String that matches the mousetrap.js spec (or an array of same)
    """

    for definition in definitions:
        if type(definition) is str:
            trigger = Trigger(definition, definition, definition)
        elif type(definition) is dict:
            trigger = Trigger(str(definition['id']), str(definition['label']), str(definition['shortcut']))
        else:
            raise RuntimeError('Trigger must be of type str or dict, not %s' % type(definition))

        yield trigger

def triggers_as_dict(definitions):
    triggers = build_triggers(definitions)

    return [ dict(trigger._asdict()) for trigger in triggers ]
