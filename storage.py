"""Сохранение и загрузка состояния фермы в формате JSON."""

import json


def _validate_state(state):
    """Проверить структуру состояния; при ошибке вызвать ValueError."""
    def check_fields(value, fields):
        if type(value) is not dict or set(value) != fields:
            raise ValueError("Неверный набор полей состояния фермы")

    def nonnegative_integer(value):
        return type(value) is int and value >= 0

    required_fields = {"money", "beds", "animals", "inventory"}
    if type(state) is not dict or not required_fields <= set(state) or set(state) - required_fields - {"harvest_bonus"}:
        raise ValueError("Неверный набор полей состояния фермы")
    if not nonnegative_integer(state["money"]):
        raise ValueError("Деньги должны быть неотрицательным целым числом")
    if "harvest_bonus" in state and not nonnegative_integer(state["harvest_bonus"]):
        raise ValueError("Бонус должен быть неотрицательным целым числом")
    if any(type(state[key]) is not list for key in ("beds", "animals", "inventory")):
        raise ValueError("Грядки, животные и инвентарь должны быть списками")

    crops = set()
    for bed in state["beds"]:
        check_fields(bed, {"crop", "stage"})
        if type(bed["crop"]) is not str or type(bed["stage"]) is not int or not 0 <= bed["stage"] <= 3:
            raise ValueError("Неверные данные грядки")
        crop = bed["crop"].casefold()
        if crop in crops:
            raise ValueError("Культуры на грядках не должны повторяться")
        crops.add(crop)

    for animal in state["animals"]:
        check_fields(animal, {"name", "hungry"})
        if type(animal["name"]) is not str or type(animal["hungry"]) is not bool:
            raise ValueError("Неверные данные животного")
    if any(type(item) is not str for item in state["inventory"]):
        raise ValueError("Инвентарь должен содержать строки")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Повторяющееся поле JSON: " + key)
        result[key] = value
    return result


def save_farm(state, path="farm_save.json"):
    """Проверить и записать состояние фермы в UTF-8 JSON."""
    _validate_state(state)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)


def load_farm(path="farm_save.json"):
    """Прочитать и проверить состояние фермы из UTF-8 JSON."""
    with open(path, encoding="utf-8") as file:
        state = json.load(file, object_pairs_hook=_unique_object)
    _validate_state(state)
    return state
