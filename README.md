# Room Management Module PoC

Proof of concept demonstrating schema-first, forward-compatible architecture for room management systems.

## Objective

Demonstrate that the `Room` entity can maintain a nullable foreign key to a `Reservation` model that is structurally present in the database but has no implemented endpoints. This proves the schema anticipates future booking workflows without requiring future DDL alterations.

Completion criteria:

- Every API response for `Room` includes `current_reservation_id` with value `null`
- The `reservations` table exists with full schema (`id`, `guest_name`, `check_in`, `check_out`, `room_id`)
- The `Reservation` model contains the exact comment: `# Reservation logic is not implemented. This table exists so Room.current_reservation_id has a valid foreign key target when booking endpoints are added in a future phase.`

## Live Demo

This PoC is publicly accessible for validation and stakeholder review:

- **Frontend (Vercel):** https://room-management-module-poc.vercel.app/
- **Backend API (Render):** https://room-management-module-poc.onrender.com/
- **API Documentation (Swagger):** https://room-management-module-poc.onrender.com/docs

### Free Tier Notice

Both deployments use free-tier infrastructure. Please note:

1. **Cold starts**: If the backend has not received traffic in the last 15 minutes, Render may put the service to sleep. The first request can take 30–60 seconds to "wake up" the instance. This is expected behavior and does not indicate an error.

2. **Frontend latency**: Vercel's free tier may also experience brief initialization delays on first load after periods of inactivity.

3. **Rate limits**: Free tiers have request quotas. If you encounter `429 Too Many Requests`, wait a few minutes before retrying.

## Tech Stack

Backend: Python 3.11+, FastAPI 0.111, SQLAlchemy 2.0, Pydantic 2.7+, SQLite
Frontend: React 18, Vite 5, DaisyUI 4, Tailwind CSS

## API Contract

Base path: `/api/v1`
Content-Type: `application/json`

### Rooms

- `GET /rooms` - List all rooms
- `POST /rooms` - Create room (201)
- `GET /rooms/{id}` - Get room by ID (200, 404)
- `PATCH /rooms/{id}` - Update room (200, 404)
- `DELETE /rooms/{id}` - Delete room (204, 404)

### Room Types

- `GET /room-types` - List all room types (200)

### Reservations

No endpoints are implemented. The table exists solely as a structural anchor for future booking workflows.

## Data Model

### Table: rooms

- `id` (PK), `number` (unique), `floor`, `capacity`, `status` (enum)
- `room_type_id` (FK to room_types.id)
- `current_reservation_id` (FK to reservations.id, nullable)

### Table: reservations

- `id` (PK), `guest_name`, `check_in`, `check_out`, `room_id` (FK to rooms.id, nullable)
- Exists in schema only. No CRUD operations.

### Table: room_types

- `id` (PK), `name` (unique), `description` (nullable)

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

API runs at `http://127.0.0.1:8000`. Interactive documentation at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`. API calls are proxied to the backend via Vite configuration.

## Explicit Exclusions

The following are intentionally out of scope to maintain focus on the architectural proof:

- Authentication and login UI
- Dashboard and reporting views
- Reservation endpoints (POST/GET/PATCH/DELETE /reservations)
- Capacity calculation or availability logic
- Pagination, search, or filter controls
- Status filtering controls

## License

MIT

---

## 👤 Maintained By

This project is developed and maintained by **FM ByteShift Software**

**Fernando Magalhães**  
CEO – FM ByteShift Software  
📞 (21) 97250-1546  
✉️ [contact@fmbyteshiftsoftware.com](mailto:contact@fmbyteshiftsoftware.com)  
🌐 [fmbyteshiftsoftware.com](https://fmbyteshiftsoftware.com)  
🏢 CNPJ: 62.145.022/0001-05 (Brazil)
