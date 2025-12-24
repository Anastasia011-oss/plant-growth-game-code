class Plant:
    def __init__(self, pid, name, base_time, images=None):
        self.id = pid
        self.name = name
        self.base_time = base_time
        self.images = images or {}


class PlantModel:
    def __init__(self, plant: Plant):
        self.state = "empty"
        self.remaining = 0
        self.plant = plant

    def start_growth(self, fertilizer):
        self.state = "growing"
        self.remaining = int(self.plant.base_time * fertilizer.mult)

    def tick(self, callback):
        if self.remaining <= 0:
            self.state = "ready"
            callback("finish")
            return
        self.remaining -= 1000
        callback("tick")
