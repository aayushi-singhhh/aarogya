# Aarogya Unified Health Platform

A comprehensive healthcare management system combining a modern React frontend with a powerful Flask backend.

## Project Structure

```
unified-aarogya/
├── frontend/          # React.js frontend application
│   ├── src/
│   │   ├── components/
│   │   └── sections/
│   ├── public/
│   └── package.json
├── backend/           # Flask backend API and hospital portal
│   ├── models/        # Database models (User, Patient, Doctor, etc.)
│   ├── templates/     # HTML templates for web portal
│   ├── app.py         # Main Flask application
│   └── portal_system.py # CLI system
└── package.json       # Root package.json for unified commands
```

## Features

### Frontend (React)
- Modern, responsive healthcare website
- Interactive components with Framer Motion animations
- Parallax backgrounds and smooth scrolling
- Hospital portal integration button

### Backend (Flask)
- Role-based authentication (Patient, Doctor, Admin)
- Appointment booking and management
- Medical records system
- Dashboard for all user types
- RESTful API endpoints

### User Roles
1. **Patients**: Book appointments, view medical history, manage profile
2. **Doctors**: Manage schedule, view patients, add diagnoses
3. **Hospital Admin**: Oversee operations, manage staff, view analytics

## Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python 3.9+
- pip (Python package manager)

### Installation

1. **Clone and setup the project:**
```bash
cd unified-aarogya
npm run install:all
```

2. **Setup Python virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install flask
```

3. **Start both frontend and backend:**
```bash
npm run dev
```

This will start:
- React frontend on http://localhost:5174
- Flask backend on http://localhost:5001

### Manual Start (Alternative)

**Frontend only:**
```bash
npm run frontend:dev
```

**Backend only:**
```bash
npm run backend:dev
```

## Demo Login Credentials

After starting the backend, visit http://localhost:5001/demo_data to initialize demo data.

- **Patient**: alice@email.com / pat123
- **Doctor**: sarah@hospital.com / doc123  
- **Admin**: admin@hospital.com / admin123

## Development

### Frontend Development
- Built with React + Vite
- Uses Tailwind CSS for styling
- Framer Motion for animations
- Components are modular and reusable

### Backend Development
- Flask web framework
- Object-oriented design with proper inheritance
- Session-based authentication
- Bootstrap-styled templates

### API Endpoints
- `GET /` - Home page
- `POST /login` - User authentication
- `GET /patient/dashboard` - Patient dashboard
- `GET /doctor/dashboard` - Doctor dashboard
- `GET /admin/dashboard` - Admin dashboard
- `POST /patient/book_appointment` - Book appointment
- `GET /demo_data` - Initialize demo data

## Project Integration

The frontend and backend are integrated through:
1. **Hospital Portal Button**: Located in the main Aarogya website, opens the Flask portal
2. **Cross-Origin Resource Sharing (CORS)**: Allows frontend-backend communication
3. **Unified Development**: Both services start with a single command
4. **Shared Assets**: Common styling and branding across both applications

## File Organization

### Frontend Key Files
- `src/components/AarogyaContent.jsx` - Main landing page component
- `src/components/HospitalPortalButton.jsx` - Portal integration button
- `src/components/FlipWords.jsx` - Animated text component
- `src/components/parallaxBackground.jsx` - Background effects

### Backend Key Files
- `app.py` - Main Flask application with all routes
- `models/user.py` - Base user class
- `models/patient.py` - Patient class with appointment booking
- `models/doctor.py` - Doctor class with schedule management
- `models/hospital_admin.py` - Admin class with management features
- `portal_system.py` - CLI interface for the hospital system

## Deployment

### Production Build
```bash
npm run frontend:build
```

### Environment Variables
Create `.env` files for different environments:
- `frontend/.env` - Frontend environment variables
- `backend/.env` - Backend environment variables

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@aarogya.com or create an issue in the repository.
