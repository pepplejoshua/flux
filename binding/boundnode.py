from abc import ABC, abstractmethod

# this is a typed syntax node to support type checking
class BoundNode(ABC):
    @abstractmethod
    # this returns the bound individual node type
    def nodetype(_):
        # _ because self if not used
        pass