from .plant_base import Plant, PlantModel

class AppleModel(PlantModel):
    def __init__(self):
        super().__init__(Plant(4, "Яблоня", 7000))