import main


def test_ready_crops():
    stages = {"пшеница": 3, "морковь": 2, "томат": 4, "лук": 0}
    original = stages.copy()

    assert main.ready_crops(stages) == ["пшеница", "томат"]
    assert stages == original
    assert main.ready_crops({}) == []
    assert main.ready_crops({"лук": 2}) == []


def test_add_ready():
    ready = {"пшеница"}

    result = main.add_ready(ready, "морковь")
    assert result is ready
    assert ready == {"пшеница", "морковь"}
    assert main.add_ready(ready, "морковь") is ready
    assert ready == {"пшеница", "морковь"}


def test_describe():
    for crop in ("пшеница", "Морковь", ""):
        description = main.describe(crop)
        assert isinstance(description, str)
        assert crop.lower() in description.lower()


def test_crops_upper():
    crops = ["пшеница", "Морковь", "томат", "пшеница"]
    original = crops.copy()

    assert main.crops_upper(crops) == ["ПШЕНИЦА", "МОРКОВЬ", "ТОМАТ", "ПШЕНИЦА"]
    assert crops == original
    assert main.crops_upper([]) == []


def test_run_farm_harvest(monkeypatch, capsys):
    commands = iter(["plant", "water", "water", "status", "harvest", "status", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(commands))
    monkeypatch.setattr(main, "random_event", lambda: 0)

    main.run_farm()

    output = capsys.readouterr().out
    lines = output.splitlines()
    statuses = [line for line in lines if "Пшеница: стадия" in line]
    assert len(statuses) == 2
    assert "стадия 3 (готова к сбору)" in statuses[0]
    assert "стадия 0 (не посажена)" in statuses[1]
    ready_lines = [line for line in lines if "Готовы к сбору:" in line]
    assert len(ready_lines) == 2
    assert "Пшеница" in ready_lines[0]
    assert "Пшеница" not in ready_lines[1]
    assert "Урожай собран" in output


def test_multiple_crops_and_events(monkeypatch, capsys):
    commands = iter([
        "plant", "water", "water", "plant морковь", "water морковь",
        "status", "water морковь", "status", "harvest", "status", "exit",
    ])
    # Вредители повреждают готовую морковь после полива; пшеница не меняется.
    events = iter([0, 0, 0, 0, 0, 2, 0])
    monkeypatch.setattr("builtins.input", lambda prompt: next(commands))
    monkeypatch.setattr(main, "random_event", lambda: next(events))

    main.run_farm()

    output = capsys.readouterr().out
    ready = [line for line in output.splitlines() if line.startswith("Готовы к сбору:")]
    assert ready == ["Готовы к сбору: Пшеница", "Готовы к сбору: Пшеница", "Готовы к сбору: нет"]
    assert output.count("Морковь: стадия 2 (растёт)") == 3
    assert "появились вредители" in output


def test_invalid_and_repeated_planting(monkeypatch, capsys):
    commands = iter(["plant неизвестная", "describe морковь", "plant", "plant", "status", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(commands))
    monkeypatch.setattr(main, "random_event", lambda: 0)

    main.run_farm()

    output = capsys.readouterr().out
    assert "Неизвестная культура: неизвестная" in output
    assert "Морковь — овощная культура." in output
    assert "Культура уже посажена" in output
    assert "Баланс: 90" in output
    assert "Пшеница: стадия 1" in output
