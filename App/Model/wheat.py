from .plant_base import Plant, PlantModel

class WheatModel(PlantModel):
    def __init__(self):
        super().__init__(Plant(1, "Пшеница", 5000))

