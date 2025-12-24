import json
from pathlib import Path
import os


class ResourceService:
    resources_dir = Path(__file__).parent.parent / "Resources"
    resources_file = resources_dir / "game_resources.json"

    @staticmethod
    def create_resources_file():
        data = {
            "plants": {
                "1": {
                    "name": "Пшеница",
                    "grow_time": 5000,
                    "sell_price": 15,
                    "images": {
                        "stage1": "Images/little_wheat.png",
                        "stage2": "Images/medium_wheat.png",
                        "ready": "Images/the_wheat_is_ripe.png"
                    }
                },
                "2": {
                    "name": "Виноград",
                    "grow_time": 4000,
                    "sell_price": 30,
                    "images": {
                        "stage1": "Images/little_grapes.png",
                        "stage2": "Images/medium_grapes.png",
                        "ready": "Images/the_grapes_is_ripe.png"
                    }
                },
                "3": {
                    "name": "Ананас",
                    "grow_time": 9000,
                    "sell_price": 60,
                    "images": {
                        "stage1": "Images/little_pineapple.png",
                        "stage2": "Images/medium_pineapple.png",
                        "ready": "Images/the_pineapple_is_ripe.png"
                    }
                },
                "4": {
                    "name": "Яблоня",
                    "grow_time": 6000,
                    "sell_price": 50,
                    "images": {
                        "stage1": "Images/little_apple_tree.png",
                        "stage2": "Images/medium_apple_tree.png",
                        "ready": "Images/the_apple_tree_is_ripe.png"
                    }
                },
                "5": {
                    "name": "Дыня",
                    "grow_time": 7000,
                    "sell_price": 70,
                    "images": {
                        "stage1": "Images/little_melon.png",
                        "stage2": "Images/medium_melon.png",
                        "ready": "Images/the_melon_is_ripe.png"
                    }
                },
                "6": {
                    "name": "Подсолнух",
                    "grow_time": 3000,
                    "sell_price": 40,
                    "images": {
                        "stage1": "Images/little_sunflower.png",
                        "stage2": "Images/medium_sunflower.png",
                        "ready": "Images/the_sunflower_is_ripe.png"
                    }
                },
                "7": {
                    "name": "Банан",
                    "grow_time": 5000,
                    "sell_price": 35,
                    "images": {
                        "stage1": "Images/little_banana.png",
                        "stage2": "Images/medium_banana.png",
                        "ready": "Images/the_banana_is_ripe.png"
                    }
                },
                "8": {
                    "name": "Перец",
                    "grow_time": 4500,
                    "sell_price": 28,
                    "images": {
                        "stage1": "Images/little_pepper.png",
                        "stage2": "Images/medium_pepper.png",
                        "ready": "Images/the_pepper_is_ripe.png"
                    }
                },
                "9": {
                    "name": "Слива",
                    "grow_time": 4800,
                    "sell_price": 30,
                    "images": {
                        "stage1": "Images/little_plum.png",
                        "stage2": "Images/medium_plum.png",
                        "ready": "Images/the_plum_is_ripe.png"
                    }
                }
            },

            "fertilizers": {
                "none": {"name": "Без удобрения", "multiplier": 1.0, "price": 0},
                "fast": {"name": "Обычное удобрение", "multiplier": 0.8, "price": 10},
                "super": {"name": "Суперудобрение", "multiplier": 0.6, "price": 20}
            },

            "plots": {
                "count": 4
            },

            "player": {
                "starting_balance": 50
            },

            "missions": [
                {
                    "id": 1,
                    "description": "Посадить 3 растения",
                    "type": "plant",
                    "target": 3,
                    "reward": 50
                },
                {
                    "id": 2,
                    "description": "Собрать 5 урожаев",
                    "type": "harvest",
                    "target": 5,
                    "reward": 100
                },
                {
                    "id": 3,
                    "description": "Продать урожай 1 раз",
                    "type": "sell",
                    "target": 1,
                    "reward": 70
                },
                {
                    "id": 4,
                    "description": "Купить 1 удобрение",
                    "type": "fertilizer",
                    "target": 1,
                    "reward": 30
                },
                {
                    "id": 5,
                    "description": "Купить 1 грядку",
                    "type": "plot",
                    "target": 1,
                    "reward": 150
                }
            ]
        }

        os.makedirs(ResourceService.resources_dir, exist_ok=True)

        if not ResourceService.resources_file.exists():
            with open(ResourceService.resources_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Файл game_resources.json успешно создан в {ResourceService.resources_dir}")

    @staticmethod
    def load_resources():
        if not ResourceService.resources_file.exists():
            raise FileNotFoundError(f"Файл {ResourceService.resources_file} не найден!")
        with open(ResourceService.resources_file, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_plant(plant_id: int):
        resources = ResourceService.load_resources()
        return resources["plants"].get(str(plant_id))

    @staticmethod
    def get_fertilizer(key: str):
        resources = ResourceService.load_resources()
        return resources["fertilizers"].get(key)

    @staticmethod
    def get_plot_count():
        resources = ResourceService.load_resources()
        return resources["plots"]["count"]

    @staticmethod
    def get_starting_balance():
        resources = ResourceService.load_resources()
        return resources["player"]["starting_balance"]

    @staticmethod
    def get_missions():
        resources = ResourceService.load_resources()
        return resources.get("missions", [])


if __name__ == "__main__":
    ResourceService.create_resources_file()
    print("Растение 1:", ResourceService.get_plant(1))
    print("Удобрение fast:", ResourceService.get_fertilizer("fast"))
    print("Количество грядок:", ResourceService.get_plot_count())
    print("Стартовый баланс:", ResourceService.get_starting_balance())
    print("Миссии:", ResourceService.get_missions())
