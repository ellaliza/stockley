# Contributing to Stockley

Thank you for your interest in contributing to Stockley! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 20+
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/stockley.git
   cd stockley
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   # Create virtual environment
   python -m venv venv
   # Activate
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate   # Windows
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **Start Development:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

## 📋 Development Workflow

### 1. Choose an Issue
- Check the [Issues](https://github.com/yourusername/stockley/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Ensure your code works with both backend and frontend

### 4. Test Your Changes
- **Backend:** Run the API and test endpoints manually
- **Frontend:** Test UI components and API integration
- **Database:** Verify database operations work correctly

### 5. Commit Changes
```bash
git add .
git commit -m "feat: add user profile page

- Add profile component
- Integrate with user API
- Add form validation"
```

#### Commit Message Format
We follow [Conventional Commits](https://conventionalcommits.org/):
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code restructuring
- `test:` for testing
- `chore:` for maintenance

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub.

## 🏗️ Architecture Guidelines

### Backend (FastAPI)

#### File Structure
```
backend/app/
├── api/v1/          # API endpoints
├── models/          # Database models
├── schemas/         # Pydantic schemas
├── services/        # Business logic
└── db/             # Database configuration
```

#### Code Style
- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use SQLModel for database models
- Use Pydantic for API schemas
- Add docstrings to all functions and classes

#### Example
```python
from fastapi import APIRouter, Depends
from app.db.session import SessionDep
from app.schemas.users import UserCreate, UserRead
from app.services.auth import create_user

router = APIRouter()

@router.post("/users/", response_model=UserRead)
async def create_new_user(
    user: UserCreate,
    session: SessionDep
) -> UserRead:
    """Create a new user account."""
    return create_user(session, user)
```

### Frontend (Vue.js)

#### File Structure
```
frontend/src/
├── components/      # Reusable components
├── pages/          # Page components
├── api.ts          # API client
└── types.ts        # TypeScript types
```

#### Code Style
- Use Vue 3 Composition API
- Use TypeScript for type safety
- Follow Vue.js style guide
- Use kebab-case for component files
- Use PascalCase for component names

#### Example
```typescript
// types.ts
export interface User {
  id: number;
  username: string;
  email: string;
}

// api.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
});

// components/UserProfile.vue
<template>
  <div class="user-profile">
    <h2>{{ user.username }}</h2>
    <p>{{ user.email }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { User } from '@/types';

const props = defineProps<{
  user: User;
}>();
</script>
```

## 🧪 Testing

### Backend Testing
- Test API endpoints manually using Swagger UI (`/docs`)
- Test with different user roles
- Verify error handling
- Check database state after operations

### Frontend Testing
- Test component rendering
- Test API integration
- Test form validation
- Test responsive design

## 📚 Documentation

### API Documentation
- Update endpoint documentation in code docstrings
- Add new endpoints to the backend README
- Update API examples in documentation

### Code Documentation
- Add docstrings to all new functions
- Update type hints
- Comment complex business logic

## 🔒 Security Considerations

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user inputs
- Implement proper authentication checks
- Follow OWASP guidelines

## 📝 Pull Request Process

1. **Title:** Use descriptive, conventional commit style
2. **Description:** Explain what changes and why
3. **Screenshots:** Include UI changes screenshots
4. **Testing:** Describe how you tested the changes
5. **Checklist:**
   - [ ] Code follows style guidelines
   - [ ] Tests pass
   - ] Documentation updated
   - [ ] No breaking changes
   - [ ] Security considerations addressed

## 🎯 Code Review

### What to Look For
- Code quality and style
- Security vulnerabilities
- Performance implications
- Test coverage
- Documentation completeness

### Review Checklist
- [ ] Code is readable and well-documented
- [ ] Follows project conventions
- [ ] Includes appropriate tests
- [ ] No security issues
- [ ] Performance is acceptable
- [ ] Documentation is updated

## 📞 Getting Help

- **Issues:** Use GitHub Issues for bugs and feature requests
- **Discussions:** Use GitHub Discussions for questions
- **Code of Conduct:** Be respectful and inclusive

## 🙏 Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- GitHub repository contributors list
- Project documentation

Thank you for contributing to Stockley! 🎉</content>
<parameter name="filePath">c:\Ella-Liza\personal projects\VUE_FASTAPI\CONTRIBUTING.md