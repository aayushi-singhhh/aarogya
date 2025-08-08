from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional

class User(ABC):
    """Abstract base class for all user types"""
    
    def __init__(self, user_id: str, name: str, email: str, password: str, role: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.created_at = datetime.now()
        self.last_login = None
    
    @abstractmethod
    def get_dashboard_data(self) -> Dict:
        """Return role-specific dashboard data"""
        pass
    
    def login(self) -> bool:
        """Simulate login process"""
        self.last_login = datetime.now()
        return True
    
    def __str__(self):
        return f"{self.name} ({self.role})"
