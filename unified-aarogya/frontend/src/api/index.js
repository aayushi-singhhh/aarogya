// API configuration for backend integration
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://aarogya-1bcm9b9fl-aayushi-singhhs-projects.vercel.app' 
  : 'http://localhost:5001';

export const api = {
  // User authentication
  login: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });
    return response;
  },

  // Get user info
  getUserInfo: async () => {
    const response = await fetch(`${API_BASE_URL}/api/user_info`, {
      credentials: 'include',
    });
    return response.json();
  },

  // Patient endpoints
  patient: {
    getDashboard: async () => {
      const response = await fetch(`${API_BASE_URL}/patient/dashboard`, {
        credentials: 'include',
      });
      return response;
    },
    
    bookAppointment: async (appointmentData) => {
      const response = await fetch(`${API_BASE_URL}/patient/book_appointment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(appointmentData),
      });
      return response;
    },
  },

  // Doctor endpoints
  doctor: {
    getDashboard: async () => {
      const response = await fetch(`${API_BASE_URL}/doctor/dashboard`, {
        credentials: 'include',
      });
      return response;
    },
  },

  // Admin endpoints
  admin: {
    getDashboard: async () => {
      const response = await fetch(`${API_BASE_URL}/admin/dashboard`, {
        credentials: 'include',
      });
      return response;
    },
  },

  // Initialize demo data
  initializeDemoData: async () => {
    const response = await fetch(`${API_BASE_URL}/demo_data`, {
      credentials: 'include',
    });
    return response;
  },
};

export default api;
