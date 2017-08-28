from .arbitrary_closed_profile_def import ArbitraryClosedProfileDef

class ArbitraryProfileDefWithVoids(ArbitraryClosedProfileDef):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'ArbitraryProfileDefWithVoids'
