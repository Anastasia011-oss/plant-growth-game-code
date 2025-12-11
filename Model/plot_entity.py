class PlotEntity:
    def __init__(self, index, state="empty", plant_id=None, remaining=0, fertilizer_count=0):
        self.index = index
        self.state = state
        self.plant_id = plant_id
        self.remaining = remaining
        self.fertilizer_count = fertilizer_count
