from snecs import RegisteredComponent
from snecs.typedefs import EntityID


class WantsToMelee(RegisteredComponent):
    def __init__(self, target: EntityID) -> None:
        self.target = target
