from sqlalchemy import func
from iris.modules.product_ideas.models import ProductIdea, ProductIdeaStatus
from iris.modules.epics.models import Epic, EpicStatus
from iris.extensions import db
from datetime import datetime, timedelta


class DashboardService:
    """Service class for dashboard operations."""
    
    @staticmethod
    def get_product_idea_stats():
        """
        Get statistics about product ideas.
        
        Returns:
            dict: Dictionary containing product idea statistics
        """
        total_count = ProductIdea.query.count()
        
        # Count by status
        status_counts = db.session.query(
            ProductIdea.status, 
            func.count(ProductIdea.id)
        ).group_by(ProductIdea.status).all()
        
        # Count by impact level
        impact_counts = db.session.query(
            ProductIdea.impact_level, 
            func.count(ProductIdea.id)
        ).group_by(ProductIdea.impact_level).all()
        
        # Count by priority
        priority_counts = db.session.query(
            ProductIdea.priority,
            func.count(ProductIdea.id)
        ).group_by(ProductIdea.priority).all()
        
        # Get upcoming deadlines (next 30 days)
        upcoming_deadlines = ProductIdea.query.filter(
            ProductIdea.target_date >= datetime.utcnow(),
            ProductIdea.target_date <= datetime.utcnow() + timedelta(days=30)
        ).order_by(ProductIdea.target_date).all()
        
        # Convert to dictionaries for easier access in templates
        status_dict = {status: count for status, count in status_counts}
        impact_dict = {impact: count for impact, count in impact_counts}
        priority_dict = {priority: count for priority, count in priority_counts}
        
        return {
            'total_count': total_count,
            'status_counts': status_dict,
            'impact_counts': impact_dict,
            'priority_counts': priority_dict,
            'approved_count': status_dict.get(ProductIdeaStatus.APPROVED, 0),
            'draft_count': status_dict.get(ProductIdeaStatus.DRAFT, 0),
            'high_impact_count': impact_dict.get('high', 0),
            'upcoming_deadlines': upcoming_deadlines
        }
    
    @staticmethod
    def get_epic_stats():
        """
        Get statistics about epics.
        
        Returns:
            dict: Dictionary containing epic statistics
        """
        total_count = Epic.query.count()
        
        # Count by status
        status_counts = db.session.query(
            Epic.status,
            func.count(Epic.id)
        ).group_by(Epic.status).all()
        
        # Count by priority
        priority_counts = db.session.query(
            Epic.priority,
            func.count(Epic.id)
        ).group_by(Epic.priority).all()
        
        # Get upcoming deadlines (next 30 days)
        upcoming_deadlines = Epic.query.filter(
            Epic.target_date >= datetime.utcnow(),
            Epic.target_date <= datetime.utcnow() + timedelta(days=30)
        ).order_by(Epic.target_date).all()
        
        # Calculate average completion percentage in Python
        epics = Epic.query.all()
        avg_completion = sum(epic.completion_percentage for epic in epics) / len(epics) if epics else 0
        
        # Convert to dictionaries for easier access in templates
        status_dict = {status: count for status, count in status_counts}
        priority_dict = {priority: count for priority, count in priority_counts}
        
        return {
            'total_count': total_count,
            'status_counts': status_dict,
            'priority_counts': priority_dict,
            'in_progress_count': status_dict.get(EpicStatus.IN_PROGRESS, 0),
            'completed_count': status_dict.get(EpicStatus.COMPLETED, 0),
            'avg_completion': round(avg_completion, 1),
            'upcoming_deadlines': upcoming_deadlines
        }
    
    @staticmethod
    def get_recent_product_ideas(limit=5):
        """
        Get the most recently created product ideas.
        
        Args:
            limit (int): Maximum number of ideas to return
            
        Returns:
            list: List of ProductIdea objects
        """
        return ProductIdea.query.order_by(
            ProductIdea.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_recent_epics(limit=5):
        """
        Get the most recently created epics.
        
        Args:
            limit (int): Maximum number of epics to return
            
        Returns:
            list: List of Epic objects
        """
        return Epic.query.order_by(
            Epic.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_user_product_ideas(user_id, limit=5):
        """
        Get product ideas created by a specific user.
        
        Args:
            user_id (str): User ID
            limit (int): Maximum number of ideas to return
            
        Returns:
            list: List of ProductIdea objects
        """
        return ProductIdea.query.filter_by(
            created_by_id=user_id
        ).order_by(
            ProductIdea.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_user_epics(user_id, limit=5):
        """
        Get epics created by a specific user.
        
        Args:
            user_id (str): User ID
            limit (int): Maximum number of epics to return
            
        Returns:
            list: List of Epic objects
        """
        return Epic.query.filter_by(
            created_by_id=user_id
        ).order_by(
            Epic.created_at.desc()
        ).limit(limit).all()
