import pytest

from main import bed_reports, growing_crops, hungry_animals, ready_crops


@pytest.mark.parametrize("stages, ready, growing", [
    ({}, [], []),
    ({"лук": 0, "морковь": 1, "томат": 2, "пшеница": 3, "тыква": 4},
     ["пшеница", "тыква"], ["морковь", "томат"]),
    ({"лук": 0}, [], []),
    ({"пшеница": 3}, ["пшеница"], []),
])
def test_crop_stages(stages, ready, growing):
    actual_ready = list(ready_crops(stages))
    actual_growing = list(growing_crops(stages))
    assert actual_ready == ready
    assert actual_growing == growing
    assert set(actual_ready).isdisjoint(actual_growing)


@pytest.mark.parametrize("animals, expected", [
    ([], []),
    ([{"name": "корова", "hungry": False}], []),
    ([{"name": "корова", "hungry": True}, {"name": "овца", "hungry": False},
      {"name": "курица", "hungry": True}], ["корова", "курица"]),
])
def test_hungry_animals(animals, expected):
    assert list(hungry_animals(animals)) == expected


def test_bed_reports_include_every_name_and_stage():
    stages = {"пшеница": 0, "морковь": 2, "томат": 3}
    reports = list(bed_reports(stages))
    assert len(reports) == len(stages)
    for report, (name, stage) in zip(reports, stages.items()):
        assert isinstance(report, str)
        assert name.lower() in report.lower()
        assert str(stage) in report
    assert list(bed_reports({})) == []
