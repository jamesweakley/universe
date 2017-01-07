import logging

from universe.wrappers import action_space

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SafeActionSpace(action_space.SafeActionSpace):
    # This will be the new location for SafeActionSpace, however the logic must currently remain in
    # wrappers.SafeActionSpace in order to maintain backwards compatibility.
    def _deprecation_warning(self):
        pass
