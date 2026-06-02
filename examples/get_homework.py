from datetime import datetime

from edupage_api import Edupage
from edupage_api.dbi import DbiHelper
from edupage_api.subjects import Subjects
from edupage_api.timeline import EventType

import json

edupage = Edupage()
edupage.login(
    "#EMAIL_ADDRESS#",
    "#PASSWORD#",
    "#SCHOOL_EDUPAGE_SUBDOMAIN#",  # SUBDOMAIN.edupage.org
)

notifications = edupage.get_notifications()

json_data = []

#homework_not_due = 0

homework_types = {
    EventType.HOMEWORK,
    EventType.TESTING,
    EventType.HOMEWORK_TEST,
    EventType.EXAM_ASSIGNMENT,
}

exam_event_types = {
    "exam",
    "bexam",
    "sexam",
    "oexam",
    "rexam",
    "pexam",
}

def is_homework_notification(event):
    if event.event_type in homework_types:
        return True
    if event.event_type == EventType.EVENT:
        if isinstance(event.additional_data, dict) and event.additional_data.get("typ") in exam_event_types:
            return True
    return False


def get_subject_name(event):
    recipient = event.recipient
    if isinstance(recipient, str) and " · " in recipient:
        return recipient.split(" · ", 1)[1].strip()

    if isinstance(event.additional_data, dict):
        subject_id = event.additional_data.get("subjectid") or event.additional_data.get("predmetid")
        if subject_id:
            try:
                subject = Subjects(edupage).get_subject(subject_id)
            except (TypeError, ValueError):
                subject = None
            if subject is not None:
                return subject.name or subject.short
            try:
                return DbiHelper(edupage).fetch_subject_name(int(subject_id))
            except (TypeError, ValueError):
                return None

    return recipient if recipient is not None else ""

homework = [x for x in notifications if is_homework_notification(x)]
#print(homework)
for hw in homework:
    additional_data = hw.additional_data if isinstance(hw.additional_data, dict) else {}

    if additional_data.get("textReply"):
        continue

    due_date = additional_data.get("date")
    hw_title = None
    hw_from = f"{hw.timestamp}"

    def format_homework_text(event):
        if (
            event.event_type == EventType.EVENT
            and isinstance(event.additional_data, dict)
            and event.additional_data.get("typ") in exam_event_types
        ):
            event_name = event.additional_data.get("name") or event.text
            if isinstance(event_name, str):
                event_name = event_name.strip()
                for prefix in ("Udalosť:", "Udalosť:", "Udalosť:"):
                    if event_name.startswith(prefix):
                        event_name = event_name[len(prefix) :].strip()
                        break
                return f"Písomka: {event_name}"
        if event.event_type == EventType.EXAM_ASSIGNMENT:
            assignment_name = (
                event.additional_data.get("name")
                or event.additional_data.get("nazov")
                or event.additional_data.get("title")
                or event.text
            )
            return (assignment_name or "").replace("\n", " ")
        return (event.text or "").replace("\n", " ")

    hw_text = hw_title or format_homework_text(hw)
    text = f"{hw_text}"

    hw_subject = get_subject_name(hw)

    if due_date:
        now = datetime.now()
        #text += f"\nDue to: {due_date}"

        dt_due_date = datetime.strptime(due_date, "%Y-%m-%d")

        if dt_due_date >= now:
            text += ""
        else:
            #homework_not_due += 1
            continue

    # Append homework details to list
    json_data.append({
        "Homework from": hw_from,
        "Text of HW": text,
        "Subject": hw_subject,
        "Due to": due_date
    })

print(json.dumps(json_data))
