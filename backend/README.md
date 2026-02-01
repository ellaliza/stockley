# Stockley Backend

FastAPI-based backend for the Stockley inventory management system.

## 🚀 Quick Start

1. **Activate virtual environment:**
   ```bash
   # Windows
   .\Scripts\activate

   # macOS/Linux
   source Scripts/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📋 API Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | User login (OAuth2) | No |
| POST | `/auth/register` | User registration | No |
| GET | `/auth/users/me` | Get current user info | Yes |
| PUT | `/auth/users/me` | Update current user | Yes |
| GET | `/auth/users` | List all users | Yes |

### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API health check | No |

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///stockley.db
```

### CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (development frontend)
- `https://frontend.ellaliza.dev` (production frontend)
- `https://backend.ellaliza.dev` (production backend)

## 🗄️ Database

### Current Schema

#### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    role TEXT DEFAULT 'regular'
);
```

#### Store Members Table
```sql
CREATE TABLE storemember (
    id INTEGER PRIMARY KEY,
    role TEXT NOT NULL,
    user_id INTEGER REFERENCES user(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Stores Table
```sql
CREATE TABLE store (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    location TEXT
);
```

#### Store-Member Links Table
```sql
CREATE TABLE store_to_storemember_link (
    storemember_id INTEGER REFERENCES storemember(id),
    store_id INTEGER REFERENCES store(id),
    PRIMARY KEY (storemember_id, store_id)
);
```

#### Products Table
```sql
CREATE TABLE product (
    productId INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    initial_stock INTEGER NOT NULL,
    current_stock INTEGER NOT NULL,
    minimum_stock_level INTEGER DEFAULT 5,
    reserved_stock INTEGER DEFAULT 0,
    store_id INTEGER REFERENCES store(id)
);
```

#### Stock Movements Table
```sql
CREATE TABLE stockmovement (
    id INTEGER PRIMARY KEY,
    product_id INTEGER REFERENCES product(productId),
    movement_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: Send username/password to `/auth/login` to receive a JWT token
2. **Protected Routes**: Include the token in the `Authorization` header:
   ```
   Authorization: Bearer <your-jwt-token>
   ```
3. **Token Expiration**: Tokens expire after 30 minutes by default

## 📊 Response Formats

### Successful Responses
```json
{
  "message": "Success message",
  "data": { ... }
}
```

### Error Responses
```json
{
  "detail": "Error description",
  "status_code": 400
}
```

## 🧪 Testing

### Manual Testing with curl

**Register a new user:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&email=test@example.com&full_name=Test User&password=securepass123"
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepass123"
```

**Get current user (replace TOKEN with actual token):**
```bash
curl -X GET "http://localhost:8000/auth/users/me" \
  -H "Authorization: Bearer TOKEN"
```

## 📚 API Documentation

When the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API route handlers
│   │   └── auth.py      # Authentication endpoints
│   ├── core/            # Core configuration
│   ├── db/              # Database setup
│   │   └── session.py   # Database session management
│   ├── models/          # SQLModel database models
│   │   ├── auth.py      # Authentication models
│   │   ├── products.py  # Product models
│   │   ├── stores.py    # Store models
│   │   └── users.py     # User models
│   ├── schemas/         # Pydantic request/response schemas
│   │   ├── general.py   # General schemas
│   │   ├── products.py  # Product schemas
│   │   ├── stores.py    # Store schemas
│   │   └── users.py     # User schemas
│   └── services/        # Business logic services
│       └── auth.py      # Authentication services
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔄 Development Workflow

1. **Database Changes**: Update models in `app/models/`
2. **API Changes**: Add routes in `app/api/v1/`
3. **Business Logic**: Implement in `app/services/`
4. **Schemas**: Update in `app/schemas/`

The database tables are automatically created on startup via the `lifespan` event.

## 🚀 Deployment

### Production Considerations

1. **Database**: Switch from SQLite to PostgreSQL/MySQL
2. **Environment Variables**: Set strong `SECRET_KEY`
3. **HTTPS**: Enable SSL/TLS
4. **Rate Limiting**: Implement request rate limiting
5. **Logging**: Add structured logging
6. **Monitoring**: Add health checks and metrics

### Docker Deployment (Future)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Follow the existing code style
2. Add type hints to new functions
3. Update this README for new endpoints
4. Test your changes manually
5. Ensure the API documentation is up to date</content>
<parameter name="filePath">c:\Ella-Liza\personal projects\VUE_FASTAPI\backend\README.md