from .plant_base import Plant, PlantModel

class PineappleModel(PlantModel):
    def __init__(self):
        super().__init__(Plant(3, "Ананас", 9000))