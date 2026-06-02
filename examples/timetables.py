import datetime
import json

from edupage_api import Edupage

edupage = Edupage()
edupage.login(
    "#EMAIL_ADDRESS#",
    "#PASSWORD#",
    "#SCHOOL_EDUPAGE_SUBDOMAIN#",  # SUBDOMAIN.edupage.org
)

student_name = "#STUDENT_NAME#"  # e.g. "Alžbeta Výborná"

def names(items):
    if not items:
        return []
    return [item.name for item in items if item is not None]


def lesson_to_dict(lesson):
    return {
        "period": lesson.period,
        "start": lesson.start_time.strftime("%H:%M") if lesson.start_time else None,
        "end": lesson.end_time.strftime("%H:%M") if lesson.end_time else None,
        "duration": lesson.duration,
        "subject": lesson.subject.name if lesson.subject else None,
        "teachers": names(lesson.teachers),
        "classrooms": names(lesson.classrooms),
        "classes": names(lesson.classes),
        "groups": lesson.groups or [],
        "curriculum": lesson.curriculum,
        "is_cancelled": lesson.is_cancelled,
        "is_event": lesson.is_event,
    }


date = datetime.date.today()
students = edupage.get_students() or []
student = next((student for student in students if student.name == student_name), None)

if student is None:
    available_students = [student.name for student in students]
    raise RuntimeError(
        f"Student {student_name!r} was not found. Available students: {available_students}"
    )

timetable = edupage.get_timetable(student, date)

json_data = [lesson_to_dict(lesson) for lesson in timetable]
print(json.dumps(json_data, ensure_ascii=False))
