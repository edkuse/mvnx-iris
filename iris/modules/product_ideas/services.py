from iris.extensions import db
from .models import ProductIdea
from sqlalchemy.dialects.postgresql import array
from sqlalchemy import func


class ProductIdeaService:
    """Service class for product idea operations."""
    
    @staticmethod
    def get_all(filters=None):
        """
        Get all product ideas with optional filtering.
        
        Args:
            filters (dict): Dictionary of filter parameters
            
        Returns:
            list: List of ProductIdea objects
        """
        query = ProductIdea.query
        
        if filters:
            # Apply status filter
            if filters.get('status'):
                query = query.filter(ProductIdea.status == filters['status'])
            
            # Apply impact filter
            if filters.get('impact'):
                query = query.filter(ProductIdea.impact_level == filters['impact'])
            
            # Apply tag filter
            if filters.get('tag'):
                query = query.filter(ProductIdea.tags.contains(array([filters['tag']])))
            
            # Apply search filter
            if filters.get('search'):
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    (ProductIdea.title.ilike(search_term)) | 
                    (ProductIdea.description.ilike(search_term)) |
                    (ProductIdea.problem_statement.ilike(search_term))
                )
        
        return query.order_by(ProductIdea.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(idea_id):
        """
        Get a product idea by ID.
        
        Args:
            idea_id (int): Product idea ID
            
        Returns:
            ProductIdea: Product idea object or None
        """
        return ProductIdea.query.get(idea_id)
    
    @staticmethod
    def create(data):
        """
        Create a new product idea.
        
        Args:
            data (dict): Product idea data
            
        Returns:
            ProductIdea: Created product idea
        """
        # Process tags if they're a string
        if 'tags' in data and isinstance(data['tags'], str):
            tags = [tag.strip() for tag in data['tags'].split(',')] if data['tags'] else []
            data['tags'] = tags
        
        product_idea = ProductIdea(**data)
        db.session.add(product_idea)
        db.session.commit()
        return product_idea
    
    @staticmethod
    def update(idea_id, data):
        """
        Update an existing product idea.
        
        Args:
            idea_id (int): Product idea ID
            data (dict): Updated product idea data
            
        Returns:
            ProductIdea: Updated product idea or None if not found
        """
        product_idea = ProductIdeaService.get_by_id(idea_id)
        if not product_idea:
            return None
        
        # Process tags if they're a string
        if 'tags' in data and isinstance(data['tags'], str):
            tags = [tag.strip() for tag in data['tags'].split(',')] if data['tags'] else []
            data['tags'] = tags
        
        for key, value in data.items():
            setattr(product_idea, key, value)
        
        db.session.commit()
        return product_idea
    
    @staticmethod
    def delete(idea_id):
        """
        Delete a product idea.
        
        Args:
            idea_id (int): Product idea ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        product_idea = ProductIdeaService.get_by_id(idea_id)
        if not product_idea:
            return False
        
        db.session.delete(product_idea)
        db.session.commit()
        return True
    
    @staticmethod
    def get_all_tags():
        """
        Get all unique tags used in product ideas.
        
        Returns:
            list: List of unique tags
        """
        return []
    
        # tags = db.session.query(func.unnest(ProductIdea.tags).distinct()).all()
        # return [tag[0] for tag in tags]
    
    @staticmethod
    def change_status(idea_id, status):
        """
        Change the status of a product idea.
        
        Args:
            idea_id (int): Product idea ID
            status (str): New status
            
        Returns:
            ProductIdea: Updated product idea or None if not found
        """
        product_idea = ProductIdeaService.get_by_id(idea_id)
        if not product_idea:
            return None
        
        product_idea.status = status
        db.session.commit()
        return product_idea
