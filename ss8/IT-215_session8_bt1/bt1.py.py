from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI(title="Carrier Management API")

# ==========================
# ENUM
# ==========================

class CarrierStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Shift(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    NIGHT = "NIGHT"


# ==========================
# DATABASE
# ==========================

carriers = [
    {
        "id": 1,
        "code": "GHN",
        "name": "Giao Hang Nhanh",
        "max_weight_capacity": 5000,
        "status": "ACTIVE"
    },
    {
        "id": 2,
        "code": "GHTK",
        "name": "Giao Hang Tiet Kiem",
        "max_weight_capacity": 3000,
        "status": "ACTIVE"
    },
    {
        "id": 3,
        "code": "VTP",
        "name": "Viettel Post",
        "max_weight_capacity": 10000,
        "status": "SUSPENDED"
    }
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]


# ==========================
# SCHEMA
# ==========================

class CarrierCreate(BaseModel):
    code: str
    name: str = Field(..., min_length=3)
    max_weight_capacity: int = Field(..., gt=0)
    status: CarrierStatus


class ShipmentCreate(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(..., gt=0)
    dispatch_date: str
    shift: Shift


# ==========================
# CARRIER API
# ==========================

@app.post("/carriers", status_code=201)
def create_carrier(payload: CarrierCreate):

    for carrier in carriers:
        if carrier["code"].lower() == payload.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Carrier code already exists"
            )

    new_carrier = payload.model_dump()
    new_carrier["id"] = len(carriers) + 1

    carriers.append(new_carrier)

    return {
        "message": "Carrier created successfully",
        "data": new_carrier
    }


@app.get("/carriers")
def get_carriers(
    keyword: str = "",
    status: CarrierStatus | None = None,
    min_weight: int | None = None
):

    result = carriers

    if keyword:
        result = [
            c for c in result
            if keyword.lower() in c["code"].lower()
            or keyword.lower() in c["name"].lower()
        ]

    if status:
        result = [
            c for c in result
            if c["status"] == status
        ]

    if min_weight is not None:
        result = [
            c for c in result
            if c["max_weight_capacity"] >= min_weight
        ]

    return result


@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id: int):

    for carrier in carriers:
        if carrier["id"] == carrier_id:
            return carrier

    raise HTTPException(
        status_code=404,
        detail="Carrier not found"
    )


@app.put("/carriers/{carrier_id}")
def update_carrier(
    carrier_id: int,
    payload: CarrierCreate
):

    for index, carrier in enumerate(carriers):

        if carrier["id"] == carrier_id:

            for item in carriers:
                if (
                    item["code"].lower() == payload.code.lower()
                    and item["id"] != carrier_id
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Carrier code already exists"
                    )

            update_data = payload.model_dump()
            update_data["id"] = carrier_id

            carriers[index] = update_data

            return {
                "message": "Carrier updated successfully",
                "data": update_data
            }

    raise HTTPException(
        status_code=404,
        detail="Carrier not found"
    )


@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):

    for index, carrier in enumerate(carriers):
        if carrier["id"] == carrier_id:
            carriers.pop(index)
            return {
                "message": "Carrier deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Carrier not found"
    )


# ==========================
# SHIPMENT API
# ==========================

@app.post("/shipments", status_code=201)
def create_shipment(payload: ShipmentCreate):

    carrier = None

    for c in carriers:
        if c["id"] == payload.carrier_id:
            carrier = c
            break

    if carrier is None:
        raise HTTPException(
            status_code=404,
            detail="Carrier not found"
        )

    if carrier["status"] != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Carrier is not active"
        )

    if payload.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Shipment exceeds carrier capacity"
        )

    for shipment in shipments:

        if (
            shipment["carrier_id"] == payload.carrier_id
            and shipment["dispatch_date"] == payload.dispatch_date
            and shipment["shift"] == payload.shift
        ):
            raise HTTPException(
                status_code=400,
                detail="Carrier already has shipment in this date and shift"
            )

    new_shipment = payload.model_dump()
    new_shipment["id"] = len(shipments) + 1

    shipments.append(new_shipment)

    return {
        "message": "Shipment created successfully",
        "data": new_shipment
    }


@app.get("/shipments")
def get_shipments():
    return shipments