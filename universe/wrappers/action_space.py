import warnings
import gym
from universe import error, spaces

def atari_vnc(up=False, down=False, left=False, right=False, z=False):
    return [spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right),
            spaces.KeyEvent.by_name('down', down=down),
            spaces.KeyEvent.by_name('z', down=z)]

def slither_vnc(space=False, left=False, right=False):
    return [spaces.KeyEvent.by_name('space', down=space),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right)]

def racing_vnc(up=False, left=False, right=False):
    return [spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right)]

def platform_vnc(up=False, left=False, right=False, space=False):
    return [spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right),
            spaces.KeyEvent.by_name('space', down=space)]

def gym_core_action_space(gym_core_id):
    spec = gym.spec(gym_core_id)

    if spec.id == 'CartPole-v0':
        return spaces.Hardcoded([[spaces.KeyEvent.by_name('left', down=True)],
                                 [spaces.KeyEvent.by_name('left', down=False)]])
    elif spec._entry_point.startswith('gym.envs.atari:'):
        actions = []
        env = spec.make()
        for action in env.unwrapped.get_action_meanings():
            z = 'FIRE' in action
            left = 'LEFT' in action
            right = 'RIGHT' in action
            up = 'UP' in action
            down = 'DOWN' in action
            translated = atari_vnc(up=up, down=down, left=left, right=right, z=z)
            actions.append(translated)
        return spaces.Hardcoded(actions)
    else:
        raise error.Error('Unsupported env type: {}'.format(spec.id))

class SafeActionSpace(object):
    def __init__(self, env):
        # We unfortunately can't maintain backwards compatability here because it would cause an import cycle.
        warnings.warn(('wrapper.SafeActionSpace is moved to '
                      'wrapper.experimental.action_space.SafeActionSpace as of 2017-01-07. '
                      'Using legacy wrapper.SafeActionSpace is now a NOOP'), DeprecationWarning)
