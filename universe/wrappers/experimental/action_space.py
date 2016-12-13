import logging

from universe import spaces
from universe import vectorized
from universe.wrappers.action_space import gym_core_action_space, slither_vnc, racing_vnc, platform_vnc

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SafeActionSpace(vectorized.Wrapper):
    '''
    Recall that every universe environment receives a list of VNC events as action.
    There exist many environments for which the set of relevant action is much smaller
    and is known.   For example, Atari environments have a modest number of keys,
    so this wrapper, when applied to an Atari environment will reduce its action space.
    Doing so is very convenient for research, since today's RL algorithms rely on random
    exploration, which is hurt by small action spaces.  As our algorithms get better
    and we switch to using the raw VNC commands, this wrapper will become less important.
    '''
    def __init__(self, env):
        super(SafeActionSpace, self).__init__(env)

        if self.spec.tags.get('runtime') == 'gym-core':
            self.action_space = gym_core_action_space(self.spec._kwargs['gym_core_id'])
        elif self.spec is None:
            pass
        elif self.spec.id in ['internet.SlitherIO-v0',
                              'internet.SlitherIOErmiyaEskandaryBot-v0',
                              'internet.SlitherIOEasy-v0']:
            self.action_space = spaces.Hardcoded([slither_vnc(left=True),
                                                  slither_vnc(right=True),
                                                  slither_vnc(space=True),
                                                  slither_vnc(left=True, space=True),
                                                  slither_vnc(right=True, space=True)])
        elif self.spec.id in ['flashgames.DuskDrive-v0']:
            # TODO: be more systematic
            self.action_space = spaces.Hardcoded([racing_vnc(up=True),
                                                  racing_vnc(left=True),
                                                  racing_vnc(right=True)])
        elif self.spec.id in ['flashgames.RedBeard-v0']:
            self.action_space = spaces.Hardcoded([platform_vnc(up=True),
                                                  platform_vnc(left=True),
                                                  platform_vnc(right=True),
                                                  platform_vnc(space=True)])
