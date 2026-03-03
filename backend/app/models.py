"""SQLAlchemy models for Count Room, Cage, Vault, Tables."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from app.database import Base
import enum


class CountSessionStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class DrawerStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class CageTransactionType(str, enum.Enum):
    chip_redemption = "chip_redemption"
    tito_redemption = "tito_redemption"
    marker = "marker"
    cash_in = "cash_in"
    fill_received = "fill_received"


class VaultTransactionType(str, enum.Enum):
    fill = "fill"              # chips to table
    credit = "credit"          # chips from table
    deposit = "deposit"       # cash from count room
    withdrawal = "withdrawal"
    armored_car = "armored_car"
    cage_replenishment = "cage_replenishment"


class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DropBox(Base):
    __tablename__ = "drop_boxes"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    machine_id = Column(String(100), nullable=False)  # slot or table identifier
    barcode = Column(String(100), unique=True, nullable=False)
    bank = Column(String(50), nullable=True)
    expected_cents = Column(BigInteger, nullable=True)  # from slot meter
    created_at = Column(DateTime, default=datetime.utcnow)


class SoftCountSession(Base):
    __tablename__ = "soft_count_sessions"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    status = Column(String(20), default=CountSessionStatus.open.value)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)


class CountResult(Base):
    __tablename__ = "count_results"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("soft_count_sessions.id"), nullable=False)
    drop_box_id = Column(Integer, ForeignKey("drop_boxes.id"), nullable=False)
    counted_cents = Column(BigInteger, nullable=False)
    expected_cents = Column(BigInteger, nullable=True)
    variance_cents = Column(BigInteger, nullable=True)  # counted - expected
    denomination_breakdown = Column(JSON, nullable=True)  # e.g. {"100": 50, "20": 10}
    created_at = Column(DateTime, default=datetime.utcnow)


class Cashier(Base):
    __tablename__ = "cashiers"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    name = Column(String(255), nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False)
    pin_hash = Column(String(255), nullable=True)  # demo: optional
    created_at = Column(DateTime, default=datetime.utcnow)


class Drawer(Base):
    __tablename__ = "drawers"
    id = Column(Integer, primary_key=True, index=True)
    cashier_id = Column(Integer, ForeignKey("cashiers.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    opening_cents = Column(BigInteger, nullable=False)
    closing_cents = Column(BigInteger, nullable=True)
    expected_cents = Column(BigInteger, nullable=True)  # computed from transactions
    status = Column(String(20), default=DrawerStatus.open.value)
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)


class CageTransaction(Base):
    __tablename__ = "cage_transactions"
    id = Column(Integer, primary_key=True, index=True)
    drawer_id = Column(Integer, ForeignKey("drawers.id"), nullable=False)
    type = Column(String(50), nullable=False)  # chip_redemption, tito_redemption, marker, etc.
    amount_cents = Column(BigInteger, nullable=False)  # positive = cash out to player, negative = cash in
    reference_id = Column(String(100), nullable=True)  # e.g. ticket token
    created_at = Column(DateTime, default=datetime.utcnow)


class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    name = Column(String(100), nullable=False)
    game_type = Column(String(50), nullable=False)  # blackjack, roulette, craps
    bank = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VaultTransaction(Base):
    __tablename__ = "vault_transactions"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    type = Column(String(50), nullable=False)
    amount_cents = Column(BigInteger, nullable=False)  # + deposit/credit, - fill/withdrawal/armored_car
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    drawer_id = Column(Integer, ForeignKey("drawers.id"), nullable=True)
    reference_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TableInventory(Base):
    __tablename__ = "table_inventories"
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    date = Column(String(10), nullable=False)  # YYYY-MM-DD
    shift = Column(String(20), nullable=True)  # day, swing, graveyard
    opening_cents = Column(BigInteger, nullable=False)
    closing_cents = Column(BigInteger, nullable=False)
    fills_cents = Column(BigInteger, default=0)
    credits_cents = Column(BigInteger, default=0)
    drop_cents = Column(BigInteger, default=0)
    win_loss_cents = Column(BigInteger, nullable=False)  # positive = win
    created_at = Column(DateTime, default=datetime.utcnow)
