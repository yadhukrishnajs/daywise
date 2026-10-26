import pytest
from datetime import date
from project import get_greeting, parse_future_date, get_sorted_upcoming_tasks


def test_get_greeting():
    assert get_greeting(8) == "Good morning! ☀️"
    assert get_greeting(14) == "Good afternoon! 🌤"
    assert get_greeting(20) == "Good evening! 🌙"
    with pytest.raises(ValueError):
        get_greeting(25)
    with pytest.raises(ValueError):
        get_greeting(-1)


def test_parse_future_date():
    fixed_today = date(2026, 10, 24)
    assert parse_future_date("24-10-2026", today=fixed_today) == "2026-10-24"
    assert parse_future_date("31-12-2026", today=fixed_today) == "2026-12-31"



    with pytest.raises(ValueError):
        parse_future_date("20-10-2026", today=fixed_today)

    with pytest.raises(ValueError):
        parse_future_date("2026-10-31", today=fixed_today)


def test_get_sorted_upcoming_tasks():
    sample_tasks = [
        {"description": "Study Python", "type": "daily", "completed": False},
        {"description": "Submit Project", "type": "future", "date": "2026-11-15", "completed": False},
        {"description": "Doctor Appointment", "type": "future", "date": "2026-10-28", "completed": True},
    ]
    sorted_result = get_sorted_upcoming_tasks(sample_tasks)
    assert len(sorted_result) == 2
    assert sorted_result[0]["description"] == "Doctor Appointment"
    assert sorted_result[1]["description"] == "Submit Project"
