from fastapi import FastAPI, Request
from pydantic import BaseModel
from database import Database

app = FastAPI()
db = Database()
db.create_tables()

from pydantic import Field

class MeetingRequest(BaseModel):
    date: str = ("YYYY-MM-DD")
    start_time: int
    end_time: int


@app.post("/request_meeting")
async def request_meeting(meeting_request: MeetingRequest):
    date = meeting_request.date
    start_time = meeting_request.start_time
    end_time = meeting_request.end_time

    if end_time <= start_time or end_time > 24:
        return "Meeting request rejected due to invalid meeting timing."

    if db.check_schedule_conflict(date, start_time, end_time):
        return "Meeting request rejected due to overlapping "

    db.add_meeting(date, start_time, end_time)
    return "Meeting request accepted, Thank You !"

