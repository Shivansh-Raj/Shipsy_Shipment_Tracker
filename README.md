# Shipment Tracker API Documentation

Welcome to the documentation for the Shipment Tracker API.  
This directory contains:

- `architecture.md` – Database schema, modules, and technical breakdown
- `api.md` – API endpoints, usage, and Postman collection link

## Base URL
[Click here to access API](https://shipsy-shipment-tracker-1.onrender.com)


## Interactive Docs

Visit `/docs` in your browser to explore Swagger UI for all endpoints.

## Postman Collection

[Click here to access Postman collection](https://web.postman.co/workspace/My-Workspace~81b583b2-ccb1-4e74-8dc5-aeb95fde3af1/collection/36962637-a2ff1eaf-8a91-4e7f-82cc-7592bc4ba691?action=share&source=copy-link&creator=36962637)


## How to Use

### 1. Register 
- **Register** → `POST /auth/register` with:
  ```json
  { "username": "testuser", "password": "1234" }

### 2. How to get access_token
- **login** → `POST /auth/login` with:
  ```json
  { "username": "testuser", "password": "1234" }
- **copy your access token**
  
## Authorization

### Swagger UI
1. [Click here](https://shipsy-shipment-tracker-1.onrender.com/docs).
2. Click the **Authorize** button at the top-right.
3. Enter your token in the format:
```python
<your_access_token>
