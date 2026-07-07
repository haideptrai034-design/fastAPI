from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
import re

app = FastAPI(title="IT Assets Management")

# =========================
# ENUM
# =========================

class AssetStatus(str, Enum):
    READY = "READY"
    ALLOCATED = "ALLOCATED"
    REPAIRING = "REPAIRING"
    SCRAPPED = "SCRAPPED"


# =========================
# DATABASE
# =========================

assets = [
    {
        "id": 1,
        "serial_number": "SN-MAC-01",
        "model": "MacBook Pro M3",
        "stock_available": 5,
        "status": "READY"
    },
    {
        "id": 2,
        "serial_number": "SN-DELL-02",
        "model": "Dell UltraSharp 27",
        "stock_available": 10,
        "status": "READY"
    },
    {
        "id": 3,
        "serial_number": "SN-THINK-03",
        "model": "ThinkPad X1 Carbon",
        "stock_available": 0,
        "status": "REPAIRING"
    }
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

# =========================
# SCHEMA
# =========================

class AssetCreate(BaseModel):
    serial_number: str
    model: str = Field(..., min_length=2, max_length=255)
    stock_available: int = Field(..., ge=0)
    status: AssetStatus


class AllocationCreate(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(..., gt=0)
    start_date: str
    duration_months: int = Field(..., ge=1, le=12)


EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'


# =========================
# ASSETS API
# =========================

@app.post("/assets", status_code=201)
def create_asset(payload: AssetCreate):

    for asset in assets:
        if asset["serial_number"].lower() == payload.serial_number.lower():
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    new_asset = payload.model_dump()
    new_asset["id"] = len(assets) + 1

    assets.append(new_asset)

    return {
        "message": "Asset created successfully",
        "data": new_asset
    }


@app.get("/assets")
def get_assets(
    keyword: str = "",
    status: AssetStatus | None = None,
    min_stock: int | None = None
):

    result = assets

    if keyword:
        pattern = re.compile(keyword, re.IGNORECASE)
        result = [
            asset for asset in result
            if pattern.search(asset["serial_number"])
            or pattern.search(asset["model"])
        ]

    if status:
        result = [
            asset for asset in result
            if asset["status"] == status
        ]

    if min_stock is not None:
        result = [
            asset for asset in result
            if asset["stock_available"] >= min_stock
        ]

    return result


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):

    for asset in assets:
        if asset["id"] == asset_id:
            return asset

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, payload: AssetCreate):

    for index, asset in enumerate(assets):

        if asset["id"] == asset_id:

            for item in assets:
                if (
                    item["serial_number"].lower() == payload.serial_number.lower()
                    and item["id"] != asset_id
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Serial number already exists"
                    )

            update_data = payload.model_dump()
            update_data["id"] = asset_id

            assets[index] = update_data

            return {
                "message": "Asset updated successfully",
                "data": update_data
            }

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):

    for index, asset in enumerate(assets):
        if asset["id"] == asset_id:
            assets.pop(index)
            return {
                "message": "Asset deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


# =========================
# ALLOCATIONS API
# =========================

@app.post("/allocations", status_code=201)
def create_allocation(payload: AllocationCreate):

    asset = None

    for item in assets:
        if item["id"] == payload.asset_id:
            asset = item
            break

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if asset["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail="Asset is not ready"
        )

    if payload.allocated_quantity > asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    if not re.fullmatch(EMAIL_REGEX, payload.employee_email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    new_allocation = payload.model_dump()
    new_allocation["id"] = len(allocations) + 1

    allocations.append(new_allocation)

    # Trừ tồn kho
    asset["stock_available"] -= payload.allocated_quantity

    # Nếu hết hàng thì chuyển trạng thái
    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    return {
        "message": "Allocation created successfully",
        "data": new_allocation
    }


@app.get("/allocations")
def get_allocations():
    return allocations