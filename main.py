import random

from farm_data import (
    CROP_NAME,
    CROPS,
    CROP_DESCRIPTIONS,
    HARVEST_BONUS,
    HARVEST_PRICE,
    MAX_STAGE,
    PLANTING_PRICE,
    STARTING_MONEY,
)

random.seed(42)


def show_help():
    print("Команды: plant, water, harvest, describe, status, sell, help, exit")
    print("Для plant, water и harvest можно указать культуру, например: plant морковь")


def ready_crops(stages):
    """Вернуть культуры, достигшие стадии сбора."""
    return [c for c, s in stages.items() if s >= MAX_STAGE]


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

    print("Добро пожаловать на текстовую ферму!")
    print("Доступные культуры:", ", ".join(c.capitalize() for c in crops))
    show_help()

    while True:
        parts = input("farm> ").strip().lower().split(maxsplit=1)
        command = parts[0] if parts else ""
        crop = parts[1] if len(parts) > 1 else CROP_NAME.lower()

        if command in ("plant", "water", "harvest", "describe") and crop not in stages:
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
            for name in crops:
                state = ("готова к сбору" if name in ready else
                         "не посажена" if stages[name] == 0 else "растёт")
                print(f"{name.capitalize()}: стадия {stages[name]} ({state})")
            print("Готовы к сбору:", ", ".join(c.capitalize() for c in crops if c in ready) or "нет")
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
