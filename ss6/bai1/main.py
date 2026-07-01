from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI()

# ======================
# Dữ liệu mẫu
# ======================

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]

# ======================
# Model
# ======================

class Room(BaseModel):
    code: str
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    status: Literal["AVAILABLE", "IN_USE", "MAINTENANCE"]


class RoomBooking(BaseModel):
    room_id: int
    class_name: str = Field(..., min_length=1)
    student_count: int = Field(..., gt=0)
    date: str
    slot: Literal["MORNING", "AFTERNOON", "EVENING"]

# ======================
# CRUD ROOM
# ======================

@app.post("/rooms")
def create_room(room: Room):

    for r in rooms:
        if r["code"].lower() == room.code.lower():
            raise HTTPException(status_code=400, detail="Room code already exists")

    new_room = {
        "id": max(r["id"] for r in rooms) + 1 if rooms else 1,
        **room.model_dump()
    }

    rooms.append(new_room)

    return {
        "message": "Room created successfully",
        "data": new_room
    }


@app.get("/rooms")
def get_rooms(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_capacity: Optional[int] = None
):

    result = rooms

    if keyword:
        result = [
            r for r in result
            if keyword.lower() in r["code"].lower()
            or keyword.lower() in r["name"].lower()
        ]

    if status:
        result = [
            r for r in result
            if r["status"] == status
        ]

    if min_capacity is not None:
        result = [
            r for r in result
            if r["capacity"] >= min_capacity
        ]

    return result


@app.get("/rooms/{room_id}")
def get_room(room_id: int):

    for room in rooms:
        if room["id"] == room_id:
            return room

    raise HTTPException(status_code=404, detail="Room not found")


@app.put("/rooms/{room_id}")
def update_room(room_id: int, updated_room: Room):

    for index, room in enumerate(rooms):

        if room["id"] == room_id:

            for r in rooms:
                if (
                    r["id"] != room_id
                    and r["code"].lower() == updated_room.code.lower()
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Room code already exists"
                    )

            rooms[index] = {
                "id": room_id,
                **updated_room.model_dump()
            }

            return {
                "message": "Room updated successfully",
                "data": rooms[index]
            }

    raise HTTPException(status_code=404, detail="Room not found")


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):

    for index, room in enumerate(rooms):
        if room["id"] == room_id:
            deleted = rooms.pop(index)

            return {
                "message": "Room deleted successfully",
                "data": deleted
            }

    raise HTTPException(status_code=404, detail="Room not found")


# ======================
# ĐẶT PHÒNG
# ======================

@app.post("/room-bookings")
def create_booking(booking: RoomBooking):

    room = None

    for r in rooms:
        if r["id"] == booking.room_id:
            room = r
            break

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    if room["status"] != "AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail="Room is not available"
        )

    if booking.student_count > room["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Student count exceeds room capacity"
        )

    for item in room_bookings:
        if (
            item["room_id"] == booking.room_id
            and item["date"] == booking.date
            and item["slot"] == booking.slot
        ):
            raise HTTPException(
                status_code=400,
                detail="Room already booked"
            )

    new_booking = {
        "id": max(b["id"] for b in room_bookings) + 1 if room_bookings else 1,
        **booking.model_dump()
    }

    room_bookings.append(new_booking)

    return {
        "message": "Booking created successfully",
        "data": new_booking
    }


@app.get("/room-bookings")
def get_bookings():
    return room_bookings