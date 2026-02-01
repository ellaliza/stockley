# Stockley - Inventory Management System

A modern, web-based inventory management application built with FastAPI and Vue.js. Stockley allows users to manage multiple stores/warehouses, track inventory items, monitor stock levels, and handle stock movements in a realistic multi-user environment.

## 🚀 Features

- **User Management**: Secure user registration and authentication with JWT tokens
- **Multi-Store Support**: Users can create and manage multiple stores/warehouses
- **Inventory Tracking**: Comprehensive product management with stock levels and movements
- **Stock Monitoring**: Real-time tracking of stock levels, minimum thresholds, and reservations
- **Role-Based Access**: Platform-wide roles (admin/regular) and store-specific roles (owner/staff)
- **RESTful API**: Well-documented API endpoints for all operations
- **Modern Frontend**: Responsive Vue.js interface with TypeScript support

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with SQLModel (SQLAlchemy + Pydantic)
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Authentication**: JWT tokens with Argon2 password hashing
- **CORS**: Configured for cross-origin requests

### Frontend (Vue.js)
- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **Language**: TypeScript
- **HTTP Client**: Axios
- **Icons**: Iconify

## 📋 Prerequisites

- Python 3.8+
- Node.js 20+
- npm or yarn

## 🛠️ Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   # On Windows
   .\Scripts\activate
   # On macOS/Linux
   source Scripts/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## 📖 API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

### Key Endpoints

#### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/users/me` - Get current user info
- `PUT /auth/users/me` - Update current user

#### Stores (Planned)
- `GET /stores/` - List user's stores
- `POST /stores/` - Create new store
- `GET /stores/{id}` - Get store details

#### Products (Planned)
- `GET /products/` - List products
- `POST /products/` - Add new product
- `PUT /products/{id}` - Update product
- `POST /products/{id}/movement` - Record stock movement

## 🗄️ Database Schema

The application uses the following main entities:

- **Users**: Platform users with authentication
- **Stores**: Warehouses or stores managed by users
- **StoreMembers**: Junction table for user-store relationships with roles
- **Products**: Inventory items belonging to stores
- **StockMovements**: Records of stock changes (in/out/reservations)

## 🔧 Development

### Project Structure

```
stockley/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Core functionality
│   │   ├── db/              # Database configuration
│   │   ├── models/          # SQLModel database models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── requirements.txt     # Python dependencies
│   └── README.md           # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── pages/          # Page components
│   │   ├── api.ts          # API client
│   │   └── types.ts        # TypeScript types
│   ├── package.json        # Node dependencies
│   └── README.md           # Frontend documentation
└── README.md               # Main project documentation
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///stockley.db
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [x] User authentication system
- [ ] Store management
- [ ] Product inventory
- [ ] Stock movement tracking
- [ ] Dashboard with analytics
- [ ] User roles and permissions
- [ ] API rate limiting
- [ ] Email notifications
- [ ] Mobile-responsive design

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Stockley** - Built with ❤️ for learning and portfolio purposes.</content>
<parameter name="filePath">c:\Ella-Liza\personal projects\VUE_FASTAPI\README.md