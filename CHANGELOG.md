# Changelog

All notable changes to Stockley will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with FastAPI backend and Vue.js frontend
- User authentication system with JWT tokens
- User registration and login endpoints
- Password hashing with Argon2
- SQLite database with SQLModel
- CORS configuration for cross-origin requests
- Basic project documentation
- Store management system with create, list, and add member functionality
- Store and user role-based access control (owner/staff roles)
- Custom exception handling for store operations
- Updated database schema for store-member relationships

### Changed
- Refactored user and store models to use direct foreign keys instead of link tables
- Updated authentication endpoints to use dependency injection for current user
- Improved schema definitions with proper Pydantic model configurations

### Planned
- Product inventory tracking
- Stock movement recording
- User roles and permissions
- Dashboard with analytics
- Mobile-responsive frontend

## [0.1.0] - 2024-02-01

### Added
- Project initialization
- Basic FastAPI application structure
- Database models for users, stores, products, and stock movements
- Authentication service with JWT
- API schemas for request/response validation
- Frontend Vue.js setup with TypeScript
- Project documentation (README files, API docs)

### Technical Details
- Backend: FastAPI, SQLModel, SQLite
- Frontend: Vue 3, TypeScript, Vite
- Authentication: JWT with Argon2 password hashing
- Database: SQLite with automatic table creation

---

## Types of Changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Versioning
This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes</content>
<parameter name="filePath">c:\Ella-Liza\personal projects\VUE_FASTAPI\CHANGELOG.md