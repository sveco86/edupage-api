import json
from datetime import date, timedelta

from edupage_api import Edupage

edupage = Edupage()
edupage.login(
    "#EMAIL_ADDRESS#",
    "#PASSWORD#",
    "#SCHOOL_EDUPAGE_SUBDOMAIN#",  # SUBDOMAIN.edupage.org
)


substitution_date = date.today() + timedelta(days=1)


def format_date(value):
    return value.strftime("%Y-%m-%d") if value else None


def format_enum(value):
    return value.value if value else None


def teacher_to_dict(teacher):
    return {
        "person_id": teacher.person_id,
        "name": teacher.name,
        "gender": format_enum(teacher.gender),
        "in_school_since": format_date(teacher.in_school_since),
        "account_type": format_enum(teacher.account_type),
        "classroom_name": teacher.classroom_name,
        "teacher_to": format_date(teacher.teacher_to),
    }


def change_to_dict(change):
    return {
        "class": change.change_class,
        "lesson": change.lesson_n,
        "title": change.title,
        "action": format_enum(change.action),
    }


missing_teachers = edupage.get_missing_teachers(substitution_date) or []
timetable_changes = edupage.get_timetable_changes(substitution_date) or []

json_data = {
    "date": substitution_date.strftime("%Y-%m-%d"),
    "missing_teachers": [teacher_to_dict(teacher) for teacher in missing_teachers],
    "timetable_changes": [change_to_dict(change) for change in timetable_changes],
}

print(json.dumps(json_data, ensure_ascii=False, indent=2))
