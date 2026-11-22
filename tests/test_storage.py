import json

import pytest

from storage import load_farm, save_farm


@pytest.mark.parametrize("state", [
    {"money": 0, "beds": [], "animals": [], "inventory": []},
    {"money": 0, "beds": [], "animals": [], "inventory": [], "harvest_bonus": 0},
    {
        "money": 125,
        "beds": [{"crop": "пшеница", "stage": 3}, {"crop": "морковь", "stage": 1}],
        "animals": [{"name": "корова", "hungry": True}, {"name": "овца", "hungry": False}],
        "inventory": ["пшеница", "морковь"],
        "harvest_bonus": 10,
    },
])
def test_save_and_load_round_trip(tmp_path, state):
    path = tmp_path / "farm.json"
    save_farm(state, path)
    assert json.loads(path.read_text(encoding="utf-8")) == state
    assert load_farm(path) == state


def test_default_save_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    state = {"money": 0, "beds": [], "animals": [], "inventory": [], "harvest_bonus": 0}
    save_farm(state)
    assert (tmp_path / "farm_save.json").exists()
    assert load_farm() == state


@pytest.mark.parametrize("bonus", [None, "10", -1, True])
def test_invalid_optional_harvest_bonus_raises(tmp_path, bonus):
    state = {"money": 100, "beds": [], "animals": [], "inventory": [], "harvest_bonus": bonus}
    path = tmp_path / "farm.json"
    path.write_text(json.dumps(state), encoding="utf-8")
    with pytest.raises(ValueError):
        load_farm(path)
    with pytest.raises(ValueError):
        save_farm(state, tmp_path / "out.json")


@pytest.mark.parametrize("stage", [0, 1, 2, 3])
def test_save_and_load_each_bed_stage(tmp_path, stage):
    state = {
        "money": 100,
        "beds": [{"crop": "пшеница", "stage": stage}],
        "animals": [],
        "inventory": [],
    }
    path = tmp_path / "farm.json"
    save_farm(state, path)
    assert load_farm(path) == state


@pytest.mark.parametrize("content", ["", "{", '{"money": 1,}'])
def test_invalid_json_raises(tmp_path, content):
    path = tmp_path / "farm.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_farm(path)


@pytest.mark.parametrize("state", [
    [],
    {},
    {"money": "100", "beds": [], "animals": [], "inventory": [], "harvest_bonus": 0},
    {"money": 100, "beds": [{"crop": "пшеница", "stage": "3"}], "animals": [], "inventory": [], "harvest_bonus": 0},
    {"money": 100, "beds": [], "animals": [{"name": "корова", "hungry": "да"}], "inventory": [], "harvest_bonus": 0},
    {"money": 100, "beds": [], "animals": [], "inventory": [42], "harvest_bonus": 0},
])
def test_invalid_structure_raises(tmp_path, state):
    path = tmp_path / "farm.json"
    path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError):
        load_farm(path)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_farm(tmp_path / "missing.json")
