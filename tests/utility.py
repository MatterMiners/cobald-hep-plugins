from cobald.interfaces import Pool


class MockPool(Pool):
    __slots__ = ("supply", "demand", "utilisation", "allocation")

    def __init__(self, *, supply=0, demand=0, utilisation=1.0, allocation=1.0):
        self.supply = supply
        self.demand = demand
        self.utilisation = utilisation
        self.allocation = allocation
