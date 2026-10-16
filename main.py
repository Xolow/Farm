money = 100
crop_stage = 0

print("Добро пожаловать на текстовую ферму!")
print("Команды: plant, water, harvest, status, sell, exit")

while True:
    command = input("farm> ")

    if command == "plant":
        if money >= 10:
            money = money - 10
            crop_stage = 1
            print("Культура посажена.")
        else:
            print("Недостаточно денег для посадки.")
    elif command == "water":
        if crop_stage == 0:
            print("Сначала посадите культуру.")
        elif crop_stage < 3:
            crop_stage = crop_stage + 1
            print("Культура полита. Текущая стадия:", crop_stage)
        else:
            print("Культура уже готова к сбору.")
    elif command == "harvest":
        if crop_stage >= 3:
            money = money + 15
            crop_stage = 0
            print("Урожай собран. Получено 15 денег.")
        else:
            print("Культура ещё не готова к сбору.")
    elif command == "status":
        print("Баланс:", money, "Стадия культуры:", crop_stage)
    elif command == "sell":
        print("Текущий баланс:", money)
    elif command == "exit":
        print("До свидания!")
        break
    else:
        print("Неизвестная команда.")
