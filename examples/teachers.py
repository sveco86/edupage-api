import json

from edupage_api import Edupage

edupage = Edupage()
edupage.login(
    "#EMAIL_ADDRESS#",
    "#PASSWORD#",
    "#SCHOOL_EDUPAGE_SUBDOMAIN#",  # SUBDOMAIN.edupage.org
)

teachers = edupage.get_teachers()


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


json_data = [teacher_to_dict(teacher) for teacher in teachers or []]
print(json.dumps(json_data, ensure_ascii=False, indent=2))
