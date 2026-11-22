import random

from farm_data import (
    ANIMALS,
    CROP_NAME,
    CROPS,
    CROP_DESCRIPTIONS,
    HARVEST_BONUS,
    HARVEST_PRICE,
    MAX_STAGE,
    PLANTING_PRICE,
    STARTING_MONEY,
)
from storage import load_farm, save_farm

random.seed(42)


def show_help():
    print("Команды: plant, water, harvest, describe, status, sell, save, load, help, exit")
    print("Для plant, water и harvest можно указать культуру, например: plant морковь")


def ready_crops(stages):
    """Вернуть культуры, достигшие стадии сбора."""
    all_crops = list(stages)
    return [crop for crop in all_crops if stages[crop] >= MAX_STAGE]


def growing_crops(stages):
    """Вернуть посаженные культуры, которые ещё не созрели."""
    candidates = [c if 0 < s < MAX_STAGE else None for c, s in stages.items()]
    return [c for c in candidates if c is not None]


def hungry_animals(animals):
    return [animal["name"] for animal in animals if animal["hungry"]]


def bed_reports(stages):
    return [
        f"{crop.capitalize()}: стадия {stage} "
        f"({'готова к сбору' if stage >= MAX_STAGE else 'растёт' if stage > 0 else 'не посажена'})"
        for crop, stage in stages.items()
    ]


def add_ready(ready, c):
    """Добавить культуру в множество готовых."""
    ready.add(c)
    return ready


def describe(crop):
    """Вернуть описание культуры или сообщение о неизвестном названии."""
    return CROP_DESCRIPTIONS.get(crop.lower(), f"Неизвестная культура: {crop}.")


def crops_upper(crops):
    return [c.upper() for c in crops]


def plant(money, crop=CROP_NAME):
    if money >= PLANTING_PRICE:
        money = money - PLANTING_PRICE
        print(crop.capitalize() + " посажена.")
        return money, 1
    print("Недостаточно денег для посадки.")
    return money, 0


def water(stage):
    if stage == 0:
        print("Сначала посадите культуру.")
    elif stage < MAX_STAGE:
        stage = stage + 1
        print("Культура полита. Текущая стадия:", stage)
    else:
        print("Культура уже готова к сбору.")
    return stage


def harvest(stage, money, bonus=0):
    if stage >= MAX_STAGE:
        earnings = HARVEST_PRICE + bonus
        money = money + earnings
        stage = 0
        bonus = 0
        print("Урожай собран. Получено", earnings, "монет.")
    else:
        print("Культура ещё не готова к сбору.")
    return stage, money, bonus


def random_event():
    event = random.randint(1, 4)
    if event == 4:
        return 0
    return event


def apply_random_event(event, stage, bonus):
    if event == 1:
        print("Случайное событие: пошёл дождь.")
        if stage > 0 and stage < MAX_STAGE:
            stage = stage + 1
            print("Дождь полил культуру. Текущая стадия:", stage)
    elif event == 2:
        print("Случайное событие: появились вредители.")
        if stage > 0:
            stage = stage - 1
            if stage == 0:
                print("Вредители уничтожили культуру.")
            else:
                print("Культура повреждена. Текущая стадия:", stage)
    elif event == 3:
        bonus = bonus + HARVEST_BONUS
        print("Случайное событие: удачный урожай! Бонус к следующему сбору:", bonus)
    return stage, bonus


def run_farm():
    money = STARTING_MONEY
    crops = CROPS.copy()
    stages = {crop: 0 for crop in crops}
    ready = set()
    harvest_bonus = 0
    animals = [animal.copy() for animal in ANIMALS]
    inventory = []

    print("Добро пожаловать на текстовую ферму!")
    print("Доступные культуры:", ", ".join(c.capitalize() for c in crops))
    show_help()

    while True:
        parts = input("farm> ").strip().lower().split(maxsplit=1)
        command = parts[0] if parts else ""
        crop = parts[1] if len(parts) > 1 else CROP_NAME.lower()

        if command in ("plant", "water", "harvest", "describe") and crop not in stages:
            if command != "describe" and crop in CROPS:
                print("Для этой культуры нет грядки.")
            else:
                print(describe(crop))
            continue

        if command == "plant":
            if stages[crop] > 0:
                print("Культура уже посажена.")
                continue
            previous_money = money
            money, stages[crop] = plant(money, crop)
            if money != previous_money:
                event = random_event()
                stages[crop], harvest_bonus = apply_random_event(
                    event, stages[crop], harvest_bonus
                )
        elif command == "water":
            previous_stage = stages[crop]
            stages[crop] = water(stages[crop])
            if stages[crop] != previous_stage:
                event = random_event()
                stages[crop], harvest_bonus = apply_random_event(
                    event, stages[crop], harvest_bonus
                )
        elif command == "harvest":
            previous_stage = stages[crop]
            stages[crop], money, harvest_bonus = harvest(
                stages[crop], money, harvest_bonus
            )
            if previous_stage >= MAX_STAGE:
                event = random_event()
                stages[crop], harvest_bonus = apply_random_event(
                    event, stages[crop], harvest_bonus
                )
        elif command == "describe":
            print(describe(crop))
        elif command == "status":
            print("Баланс:", money, "Бонус урожая:", harvest_bonus)
            for report in bed_reports(stages):
                print(report)
            print("Готовы к сбору:", ", ".join(c.capitalize() for c in crops if c in ready) or "нет")
            print("Растут:", ", ".join(c.capitalize() for c in growing_crops(stages)) or "нет")
            print("Животные:", ", ".join(a["name"].capitalize() for a in animals) or "нет")
            print("Нужно покормить:", ", ".join(a.capitalize() for a in hungry_animals(animals)) or "нет")
            print("Инвентарь:", ", ".join(inventory) or "пуст")
        elif command == "save":
            state = {
                "money": money,
                "beds": [{"crop": name, "stage": stages[name]} for name in crops],
                "animals": animals,
                "inventory": inventory,
                "harvest_bonus": harvest_bonus,
            }
            try:
                save_farm(state)
                print("Ферма сохранена в farm_save.json.")
            except (OSError, ValueError) as error:
                print("Не удалось сохранить ферму:", error)
        elif command == "load":
            try:
                state = load_farm()
                loaded_stages = {bed["crop"]: bed["stage"] for bed in state["beds"]}
                money = state["money"]
                stages = loaded_stages
                crops = list(stages)
                animals = state["animals"]
                inventory = state["inventory"]
                harvest_bonus = state.get("harvest_bonus", 0)
                print("Ферма загружена из farm_save.json.")
            except (OSError, ValueError, UnicodeError) as error:
                print("Не удалось загрузить ферму:", error)
        elif command == "sell":
            print("Текущий баланс:", money)
        elif command == "help":
            show_help()
        elif command == "exit":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")

        # События могут как ускорить рост, так и повредить готовую культуру.
        ready.clear()
        for name in ready_crops(stages):
            add_ready(ready, name)


if __name__ == "__main__":
    run_farm()
