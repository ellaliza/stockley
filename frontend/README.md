# Stockley Frontend

Vue.js 3 frontend for the Stockley inventory management system.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## 🛠️ Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## 🏗️ Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **Vue Router** - Official routing library
- **Axios** - HTTP client for API calls
- **Iconify** - Icon library

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api.ts          # API client configuration
│   ├── App.vue         # Root component
│   ├── main.ts         # Application entry point
│   ├── types.ts        # TypeScript type definitions
│   ├── assets/         # Static assets
│   ├── components/     # Reusable Vue components
│   └── pages/          # Page-level components
├── public/             # Public static files
├── index.html          # HTML template
├── package.json        # Dependencies and scripts
├── tsconfig.json       # TypeScript configuration
├── vite.config.js      # Vite configuration
└── README.md           # This file
```

## 🔧 Configuration

### API Configuration

The frontend is configured to communicate with the backend API. Update `src/api.ts` if you need to change the base URL:

```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### Development Setup

1. **Prerequisites:**
   - Node.js 20+
   - npm or yarn

2. **Environment Setup:**
   - Ensure the backend is running on `http://localhost:8000`
   - CORS is configured to allow requests from `http://localhost:5173`

## 🎨 Features

- **Responsive Design**: Mobile-first approach with responsive layouts
- **Type Safety**: Full TypeScript support for better development experience
- **Component-Based**: Modular component architecture
- **API Integration**: Axios-based API client with error handling
- **Routing**: Vue Router for single-page application navigation

## 🔄 Development Workflow

1. **Component Development:**
   - Create components in `src/components/`
   - Use Vue 3 Composition API
   - Add TypeScript interfaces in `src/types.ts`

2. **Page Creation:**
   - Add new pages in `src/pages/`
   - Configure routes in the router (future implementation)

3. **API Integration:**
   - Define API calls in `src/api.ts`
   - Handle authentication tokens
   - Implement error handling

## 🚀 Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Follow Vue 3 and TypeScript best practices
2. Use consistent naming conventions
3. Add proper TypeScript types
4. Test components across different screen sizes
5. Ensure API error states are handled gracefully

## 🔧 Troubleshooting

### Common Issues

**CORS Errors:**
- Ensure the backend is running and CORS is configured
- Check that the API base URL is correct

**Type Errors:**
- Run `npm run build` to check for TypeScript errors
- Ensure all imports are properly typed

**Build Issues:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version compatibility
