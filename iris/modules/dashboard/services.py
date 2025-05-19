from sqlalchemy import func
from iris.modules.product_ideas.models import ProductIdea
from iris.extensions import db


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
        
        # Convert to dictionaries for easier access in templates
        status_dict = {status: count for status, count in status_counts}
        impact_dict = {impact: count for impact, count in impact_counts}
        
        return {
            'total_count': total_count,
            'status_counts': status_dict,
            'impact_counts': impact_dict,
            'approved_count': status_dict.get('approved', 0),
            'draft_count': status_dict.get('draft', 0),
            'high_impact_count': impact_dict.get('high', 0)
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
