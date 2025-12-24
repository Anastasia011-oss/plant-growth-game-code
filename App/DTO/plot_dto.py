class PlotDTO:
    def __init__(self, index, state, plant_id, remaining, fertilizer_count=0):
        self.index = index
        self.state = state
        self.plant_id = plant_id
        self.remaining = remaining
        self.fertilizer_count = fertilizer_count