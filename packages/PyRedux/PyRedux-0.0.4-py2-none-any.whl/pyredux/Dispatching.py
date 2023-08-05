from __future__ import absolute_import, unicode_literals
from collections import namedtuple

import functools
from singledispatch import singledispatch

from pyredux import Actions

ActionA = Actions.create_action_type("ActionABCD")


class WrongCallingSpecForAReducer(Exception):
    pass


def default_reducer(func):
    _func = singledispatch(func)

    def _determine_action_type_from_arguments(*args, **kwargs):
        if not len(args) + len(kwargs.keys()) != 2:
            raise WrongCallingSpecForAReducer(
                "2 [Named-]Arguments have to be provided for a reducer! "
                "Found: %d positional args and %d named kwargs" % (len(args), len(kwargs.keys()))
            )
        if len(args) != 2 and (kwargs.get("action", None) is None and kwargs.get("state", None) is None):
            raise WrongCallingSpecForAReducer(
                "Named arguments have to be <action, state> found: %s" % str(kwargs.keys())
            )
        if len(args) == 2:
            return args, {}
        elif len(args) == 0:
            return (kwargs.pop("action"), kwargs["state"]), {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_args, new_kwargs = _determine_action_type_from_arguments(*args, **kwargs)

        action_type = new_args[0]
        if action_type in _func.registry:
            return _func.registry[action_type](*args, **kwargs)
        return _func(*new_args, **new_kwargs)

    wrapper.register = _func.register
    wrapper.dispatch = _func.dispatch
    wrapper.registry = _func.registry
    return wrapper


@default_reducer
def default_reducer_for_any_type(state={}, action=None):
    print("default reducer for action: %s" % str(action))


@default_reducer_for_any_type.register(ActionA)
def _(action, state):
    print("ActionA - Dispatcher: %s" % str(action))


if __name__ == '__main__':
    default_reducer_for_any_type("asdf")
    default_reducer_for_any_type(ActionA("adsf"), {1: "state"})
