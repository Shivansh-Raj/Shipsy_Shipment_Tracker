# API Documentation

## Base URL
[Click here to access API](https://shipsy-shipment-tracker-1.onrender.com)


## Interactive Docs

Visit `/docs` in your browser to explore Swagger UI for all endpoints.

## Postman Collection

[Click here to access Postman collection](https://web.postman.co/workspace/My-Workspace~81b583b2-ccb1-4e74-8dc5-aeb95fde3af1/collection/36962637-a2ff1eaf-8a91-4e7f-82cc-7592bc4ba691?action=share&source=copy-link&creator=36962637)

---

## Auth Endpoints

| Method | Endpoint | Description |
|--------|---------|------------|
| POST | /auth/register | Register a new user |
| POST | /auth/login | Login and receive JWT token |
| GET  | /auth/authenticate | Checks whether a user is authenticated or not |

---

## Shipment Endpoints

| Method | Endpoint | Description |
|--------|---------|------------|
| POST   | /shipments/ | Create a new shipment |
| GET    | /shipments/ | List shipments (supports pagination, filters, sort) |
| GET    | /shipments/{id} | Get a shipment by ID |
| PUT    | /shipments/{id} | Update shipment details (cannot update delivered shipments) |
| DELETE | /shipments/{id} | Delete a shipment |
