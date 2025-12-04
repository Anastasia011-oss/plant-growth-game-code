class Plant:
    def __init__(self, pid, name, base_time):
        self.id = pid
        self.name = name
        self.base_time = base_time


class Fertilizer:
    def __init__(self, key, name, mult, price):
        self.key = key
        self.name = name
        self.mult = mult
        self.price = price


class PlotModel:
    def __init__(self, index):
        self.index = index
        self.state = "empty"
        self.plant = None
        self.remaining = 0
        self.timer_id = None

    def start_growth(self, plant: Plant, fertilizer: Fertilizer):
        self.state = "growing"
        self.plant = plant
        self.remaining = int(plant.base_time * fertilizer.mult)

    def tick(self, callback):
        if self.remaining <= 0:
            self.state = "ready"
            callback("finish")
            return

        self.remaining -= 1000
        callback("tick")
