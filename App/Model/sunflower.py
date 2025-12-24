from .plant_base import Plant, PlantModel

class SunflowerModel(PlantModel):
    def __init__(self):
        super().__init__(Plant(6, "Подсолнух", 3000))