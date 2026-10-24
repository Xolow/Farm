import random

from farm_data import (
    CROP_NAME,
    HARVEST_BONUS,
    HARVEST_PRICE,
    MAX_STAGE,
    PLANTING_PRICE,
    STARTING_MONEY,
)

random.seed(42)


def show_help():
    print("Команды: plant, water, harvest, status, sell, help, exit")


def plant(money):
    if money >= PLANTING_PRICE:
        money = money - PLANTING_PRICE
        print(CROP_NAME + " посажена.")
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
    crop_stage = 0
    harvest_bonus = 0

    print("Добро пожаловать на текстовую ферму!")
    show_help()

    while True:
        command = input("farm> ").strip().lower()

        if command == "plant":
            previous_money = money
            money, crop_stage = plant(money)
            if money != previous_money:
                event = random_event()
                crop_stage, harvest_bonus = apply_random_event(
                    event, crop_stage, harvest_bonus
                )
        elif command == "water":
            previous_stage = crop_stage
            crop_stage = water(crop_stage)
            if crop_stage != previous_stage:
                event = random_event()
                crop_stage, harvest_bonus = apply_random_event(
                    event, crop_stage, harvest_bonus
                )
        elif command == "harvest":
            previous_stage = crop_stage
            crop_stage, money, harvest_bonus = harvest(
                crop_stage, money, harvest_bonus
            )
            if previous_stage >= MAX_STAGE:
                event = random_event()
                crop_stage, harvest_bonus = apply_random_event(
                    event, crop_stage, harvest_bonus
                )
        elif command == "status":
            print(
                "Баланс:",
                money,
                "Культура:",
                CROP_NAME,
                "Стадия:",
                crop_stage,
                "Бонус урожая:",
                harvest_bonus,
            )
        elif command == "sell":
            print("Текущий баланс:", money)
        elif command == "help":
            show_help()
        elif command == "exit":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    run_farm()
