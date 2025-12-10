import json
import os

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
        }
    },
    "fertilizers": {
        "none": {"name": "Без удобрения", "multiplier": 1.0, "price": 0},
        "fast": {"name": "Обычное удобрение", "multiplier": 0.8, "price": 10},
        "super": {"name": "Суперудобрение", "multiplier": 0.6, "price": 20}
    },
    "plots": {"count": 4},
    "player": {"starting_balance": 50}
}

def create_json_file():
    resources_dir = os.path.join(os.path.dirname(__file__), "..", "Resources")
    os.makedirs(resources_dir, exist_ok=True)
    file_path = os.path.join(resources_dir, "game_resources.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Файл game_resources.json успешно создан в {resources_dir}!")


# Функция для загрузки ресурсов из JSON
def load_resources(file_name="game_resources.json"):
    resources_dir = os.path.join(os.path.dirname(__file__), "..", "Resources")
    file_path = os.path.join(resources_dir, file_name)
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден!")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Создание JSON при запуске напрямую
if __name__ == "__main__":
    create_json_file()
