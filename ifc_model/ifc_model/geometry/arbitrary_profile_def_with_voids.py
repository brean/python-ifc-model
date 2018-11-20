from .arbitrary_closed_profile_def import ArbitraryClosedProfileDef


class ArbitraryProfileDefWithVoids(ArbitraryClosedProfileDef):
    def __init__(self, representation):
        super().__init__(representation)
        self.type = 'ArbitraryProfileDefWithVoids'
        self.points = None
        self.segments = None
