import unittest
from App.DTO.plot_dto import PlotDTO
from App.Model.plot_entity import PlotEntity
from App.Mapper.PlotMapper import PlotMapper

class TestPlotMapper(unittest.TestCase):
    def test_to_dto_and_from_dto(self):
        entity = PlotEntity(index=1, state="growing", plant_id=5, remaining=3000, fertilizer_count=2)

        dto = PlotMapper.to_dto(entity)
        self.assertIsInstance(dto, PlotDTO)
        self.assertEqual(dto.index, entity.index)
        self.assertEqual(dto.state, entity.state)
        self.assertEqual(dto.plant_id, entity.plant_id)
        self.assertEqual(dto.remaining, entity.remaining)
        self.assertEqual(dto.fertilizer_count, entity.fertilizer_count)

        # Преобразуем обратно в сущность
        new_entity = PlotMapper.from_dto(dto)
        self.assertIsInstance(new_entity, PlotEntity)
        self.assertEqual(new_entity.index, entity.index)
        self.assertEqual(new_entity.state, entity.state)
        self.assertEqual(new_entity.plant_id, entity.plant_id)
        self.assertEqual(new_entity.remaining, entity.remaining)
        self.assertEqual(new_entity.fertilizer_count, entity.fertilizer_count)


if __name__ == "__main__":
    unittest.main()
