# Changelog

All notable changes to Stockley will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Product management endpoints: create, list, get single product, bulk create
- Stock operations: `stock-out` (sell) and `stock-in` (restock) endpoints with authorization
- `ProductBulkCreate` schema for batch product creation
- `ProductReadWithStockMovement` schema for products with stock history
- `StockMovement` and `StockMovementTypes` (IN, OUT, RESERVE) for audit trail
- Comprehensive docstrings and inline comments for product schemas, services, and endpoints
- Updated API documentation with product endpoints and data models
- Product authorization checks to ensure store membership
- Field aliases (camelCase JSON, snake_case Python) for all product schemas

### Changed
- **Fixed**: `bulk-create` endpoint now correctly checks authorization against `product_list.store_id` (was referencing undefined `product.store_id`)
- **Fixed**: `restock_product` endpoint now correctly increments stock (was incorrectly decrementing)
- **Enhanced**: Added `current_user` parameter to stock operation endpoints (`stock-out`, `stock-in`) for authorization
- Improved `ProductUpdate` schema documentation regarding optional fields and `exclude_unset` usage
- Added type hints and docstrings to service functions for better developer clarity
- Product service functions now include notes about audit trail integration

### Planned
- Dashboard with analytics and low-stock alerts
- Stock movement history API and filtering
- User roles and permissions (admin, manager, staff)
- Mobile-responsive frontend
- Email notifications for low stock events
- Product inventory tracking
- Stock movement recording
- User roles and permissions
- Dashboard with analytics
- Mobile-responsive frontend

## [0.1.0] - 2026-02-01

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