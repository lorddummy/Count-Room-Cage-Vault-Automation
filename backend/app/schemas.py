"""Pydantic schemas for API request/response."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ----- Property -----
class PropertyBase(BaseModel):
    name: str
    code: str


class PropertyCreate(PropertyBase):
    pass


class PropertyResponse(PropertyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Drop Box -----
class DropBoxBase(BaseModel):
    machine_id: str
    barcode: str
    bank: Optional[str] = None
    expected_cents: Optional[int] = None


class DropBoxCreate(DropBoxBase):
    property_id: int


class DropBoxResponse(DropBoxBase):
    id: int
    property_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Soft Count Session -----
class SoftCountSessionCreate(BaseModel):
    property_id: int
    notes: Optional[str] = None


class SoftCountSessionResponse(BaseModel):
    id: int
    property_id: int
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# ----- Count Result -----
class CountResultCreate(BaseModel):
    session_id: int
    drop_box_id: int
    counted_cents: int
    expected_cents: Optional[int] = None
    denomination_breakdown: Optional[Dict[str, int]] = None


class CountResultResponse(BaseModel):
    id: int
    session_id: int
    drop_box_id: int
    counted_cents: int
    expected_cents: Optional[int] = None
    variance_cents: Optional[int] = None
    denomination_breakdown: Optional[Dict[str, int]] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Cashier -----
class CashierBase(BaseModel):
    name: str
    employee_id: str


class CashierCreate(CashierBase):
    property_id: int


class CashierResponse(CashierBase):
    id: int
    property_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Drawer -----
class DrawerCreate(BaseModel):
    cashier_id: int
    property_id: int
    opening_cents: int


class DrawerClose(BaseModel):
    closing_cents: int


class DrawerResponse(BaseModel):
    id: int
    cashier_id: int
    property_id: int
    opening_cents: int
    closing_cents: Optional[int] = None
    expected_cents: Optional[int] = None
    status: str
    opened_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----- Cage Transaction -----
class CageTransactionCreate(BaseModel):
    drawer_id: int
    type: str = Field(..., pattern="^(chip_redemption|tito_redemption|marker|cash_in|fill_received)$")
    amount_cents: int
    reference_id: Optional[str] = None


class CageTransactionResponse(BaseModel):
    id: int
    drawer_id: int
    type: str
    amount_cents: int
    reference_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Vault Transaction -----
class VaultTransactionCreate(BaseModel):
    property_id: int
    type: str = Field(
        ...,
        pattern="^(fill|credit|deposit|withdrawal|armored_car|cage_replenishment)$"
    )
    amount_cents: int
    table_id: Optional[int] = None
    drawer_id: Optional[int] = None
    reference_id: Optional[str] = None


class VaultTransactionResponse(BaseModel):
    id: int
    property_id: int
    type: str
    amount_cents: int
    table_id: Optional[int] = None
    drawer_id: Optional[int] = None
    reference_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Table -----
class TableBase(BaseModel):
    name: str
    game_type: str
    bank: Optional[str] = None


class TableCreate(TableBase):
    property_id: int


class TableResponse(TableBase):
    id: int
    property_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Table Inventory -----
class TableInventoryCreate(BaseModel):
    table_id: int
    date: str
    shift: Optional[str] = None
    opening_cents: int
    closing_cents: int
    fills_cents: int = 0
    credits_cents: int = 0
    drop_cents: int = 0


class TableInventoryResponse(BaseModel):
    id: int
    table_id: int
    date: str
    shift: Optional[str] = None
    opening_cents: int
    closing_cents: int
    fills_cents: int
    credits_cents: int
    drop_cents: int
    win_loss_cents: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----- Compliance Reports -----
class DailySlotDropReport(BaseModel):
    property_id: int
    date: str
    total_drop_cents: int
    total_variance_cents: int
    machines: List[Dict[str, Any]]
    generated_at: datetime


class DailyTableReport(BaseModel):
    property_id: int
    date: str
    tables: List[Dict[str, Any]]
    total_win_cents: int
    generated_at: datetime
