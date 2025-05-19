from datetime import datetime
from iris.extensions import db
from .models import User


class UserService:
    @staticmethod
    def create_user_from_ms_data(ms_id, graph_data):
        """Create a new user from Microsoft Graph API data."""
        user = User(
            ms_id=ms_id,
            email=graph_data.get('mail') or graph_data.get('userPrincipalName'),
            display_name=graph_data.get('displayName'),
            first_name=graph_data.get('givenName'),
            last_name=graph_data.get('surname'),
            job_title=graph_data.get('jobTitle'),
            department=graph_data.get('department'),
            profile_picture=graph_data.get('profile_photo'),
            last_login=datetime.utcnow()
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def update_last_login(user):
        """Update user's last login timestamp."""
        user.last_login = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def update_user_profile(user, graph_data):
        """Update user profile with data from Microsoft Graph API."""
        user.email = graph_data.get('mail') or graph_data.get('userPrincipalName') or user.email
        user.display_name = graph_data.get('displayName') or user.display_name
        user.first_name = graph_data.get('givenName') or user.first_name
        user.last_name = graph_data.get('surname') or user.last_name
        user.job_title = graph_data.get('jobTitle') or user.job_title
        user.department = graph_data.get('department') or user.department
        
        # Update profile picture if available
        if graph_data.get('profile_photo'):
            user.profile_picture = graph_data.get('profile_photo')
        
        db.session.commit()
