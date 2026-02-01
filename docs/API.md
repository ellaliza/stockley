# Stockley API Documentation

## Overview

Stockley provides a RESTful API for inventory management. The API is built with FastAPI and uses JSON for request/response formats.

**Base URL:** `http://localhost:8000` (development)

**Authentication:** JWT Bearer tokens

## Authentication

### Login

Authenticate a user and receive a JWT access token.

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user&password=password
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (401):**
```json
{
  "detail": "Incorrect username or password"
}
```

### Register

Create a new user account.

```http
POST /auth/register
Content-Type: application/x-www-form-urlencoded

username=newuser&email=user@example.com&full_name=New User&password=securepass123
```

**Response (200):**
```json
{
  "id": 1,
  "username": "newuser",
  "full_name": "New User",
  "email": "user@example.com",
  "created_at": "2024-02-01T10:00:00Z"
}
```

**Response (400):**
```json
{
  "detail": "Username already registered"
}
```

### Get Current User

Retrieve information about the authenticated user.

```http
GET /auth/users/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "user",
  "full_name": "User Name",
  "email": "user@example.com",
  "created_at": "2024-02-01T10:00:00Z",
  "role": "regular"
}
```

### Update Current User

Update the authenticated user's information.

```http
PUT /auth/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "full_name": "Updated Name",
  "password": "newpassword123"
}
```

**Response (200):**
```json
{
  "id": 1,
  "username": "user",
  "full_name": "Updated Name",
  "email": "newemail@example.com",
  "created_at": "2024-02-01T10:00:00Z"
}
```

### List Users

Get a list of all users (requires authentication).

```http
GET /auth/users?skip=0&limit=100
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "username": "user1",
    "full_name": "User One",
    "email": "user1@example.com",
    "created_at": "2024-02-01T10:00:00Z"
  },
  {
    "id": 2,
    "username": "user2",
    "full_name": "User Two",
    "email": "user2@example.com",
    "created_at": "2024-02-01T10:00:00Z"
  }
]
```

## Health Check

### Root Endpoint

Check if the API is running.

```http
GET /
```

**Response (200):**
```json
{
  "message": "Welcome to Stockley!"
}
```

## Error Responses

### Common Error Format

```json
{
  "detail": "Error description message"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request (validation errors, duplicate data)
- `401` - Unauthorized (invalid/missing authentication)
- `404` - Not Found
- `422` - Unprocessable Entity (validation errors)
- `500` - Internal Server Error

## Data Models

### User

```typescript
interface User {
  id: number;
  username: string;
  full_name: string;
  email: string;
  created_at: string; // ISO 8601 datetime
  role: "admin" | "regular";
}
```

### UserCreate

```typescript
interface UserCreate {
  username: string;
  email: string;
  full_name: string;
  password: string;
}
```

### Token

```typescript
interface Token {
  token: string;
  token_type: string;
}
```

## Rate Limiting

Currently, there are no rate limits implemented. This will be added in future versions.

## Versioning

The API uses URL path versioning:
- Current version: `v1`
- All endpoints are prefixed with `/auth` for authentication routes

## SDKs and Libraries

### JavaScript/TypeScript

```javascript
// Axios example
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000'
});

// Login
const login = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await api.post('/auth/login', formData);
  const token = response.data.token;

  // Set authorization header for future requests
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

  return token;
};

// Get current user
const getCurrentUser = async () => {
  const response = await api.get('/auth/users/me');
  return response.data;
};
```

### Python

```python
import requests

class StockleyAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username, password):
        data = {
            "username": username,
            "password": password
        }
        response = self.session.post(f"{self.base_url}/auth/login", data=data)
        response.raise_for_status()
        token = response.json()["token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token

    def get_current_user(self):
        response = self.session.get(f"{self.base_url}/auth/users/me")
        response.raise_for_status()
        return response.json()
```

## Testing

### Using curl

```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -d "username=testuser&password=testpass"

# Register
curl -X POST "http://localhost:8000/auth/register" \
  -d "username=newuser&email=new@example.com&full_name=New User&password=pass123"

# Get current user (replace TOKEN)
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/auth/users/me"
```

### Using Python requests

```python
import requests

# Login
response = requests.post("http://localhost:8000/auth/login",
                        data={"username": "test", "password": "pass"})
token = response.json()["token"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
user = requests.get("http://localhost:8000/auth/users/me", headers=headers)
print(user.json())
```

## Future Endpoints

The following endpoints are planned for future releases:

### Stores
- `GET /stores/` - List user's stores
- `POST /stores/` - Create store
- `GET /stores/{id}` - Get store details
- `PUT /stores/{id}` - Update store
- `DELETE /stores/{id}` - Delete store

### Products
- `GET /products/` - List products
- `POST /products/` - Add product
- `GET /products/{id}` - Get product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Stock Movements
- `POST /products/{id}/movement` - Record stock movement
- `GET /products/{id}/movements` - Get movement history

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for API changes and updates.

## Support

For API support or questions:
- Check the [GitHub Issues](https://github.com/yourusername/stockley/issues)
- Review the [Backend README](../backend/README.md)
- Visit the interactive API docs at `/docs` when the server is running</content>
<parameter name="filePath">c:\Ella-Liza\personal projects\VUE_FASTAPI\docs\API.md