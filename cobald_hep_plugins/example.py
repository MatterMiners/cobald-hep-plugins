from cobald.interfaces import PoolDecorator


class DemandScale(PoolDecorator):
    """
    Example decorator that scales demand
    """

    def __init__(self, target, scale: int = 1):
        if scale <= 0:
            raise ValueError(f"scale must be larger than 0, not {scale}")
        super().__init__(target)
        self.scale = scale

    @property
    def demand(self):
        return self.target.demand / self.scale

    @demand.setter
    def demand(self, value):
        self.target.demand = self.scale * value
