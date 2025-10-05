# Architecture Documentation

## 1. Database Schema

### User Table
| Column   | Type | Notes |
|----------|------|-------|
| id       | int  | Primary Key |
| username | str  | Unique username |
| password | str  | Hashed password |

### Shipment Table
| Column        | Type | Notes |
|---------------|------|-------|
| id            | int  | Primary Key |
| description   | str  | Shipment details |
| status        | enum | Pending / In Transit / Delivered |
| weight        | float| Weight in kilograms |
| is_express    | bool | Express delivery flag |
| shipping_fee  | float| Calculated based on weight & type |
| created_at    | datetime | Timestamp |
| updated_at    | datetime | Timestamp |

---

## 2. Class / Module Breakdown

| Module / File | Purpose |
|---------------|---------|
| `main.py`     | Initialize FastAPI app and mount routers |
| `app/models/` | SQLAlchemy ORM models (`User`, `Shipment`) |
| `app/schemas/` | Pydantic models for validation |
| `app/routers/auth.py` | Authentication endpoints (register, login, authenticate) |
| `app/routers/shipments.py` | Shipment CRUD endpoints with filters & fee calculation |
| `app/database.py` | Database connection setup |
| `app/config.py` | Environment variable management |
| `app/tests/` | Unit tests for auth and shipments |

**Design Notes:**  
- JWT used for stateless authentication.  
- Shipments are tied to the user who created them.  
- Modular structure allows scalability and maintainability.  
- Business rules enforced, e.g., cannot update delivered shipments.
