from iris.extensions import db
from .models import Epic


class EpicService:
    @staticmethod
    def get_all_tags():
        """Get all unique tags from epics."""
        epics = Epic.query.all()
        all_tags = set()
        
        for epic in epics:
            all_tags.update(epic.tags)
        
        return sorted(list(all_tags))
    
    @staticmethod
    def get_epic_by_id(epic_id):
        """Get an epic by ID."""
        return Epic.query.get(epic_id)
    
    @staticmethod
    def create_epic(data, current_user):
        """Create a new epic."""
        epic = Epic(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            priority=data.get('priority'),
            created_by=current_user,
            assigned_to_id=data.get('assigned_to_id'),
            start_date=data.get('start_date'),
            target_date=data.get('target_date'),
            business_value=data.get('business_value'),
            acceptance_criteria=data.get('acceptance_criteria'),
            estimated_effort=data.get('estimated_effort')
        )
        
        # Set tags
        if 'tags' in data:
            epic.tags = data['tags']
        
        db.session.add(epic)
        db.session.commit()
        
        return epic
    
    @staticmethod
    def update_epic(epic, data):
        """Update an existing epic."""
        epic.title = data.get('title', epic.title)
        epic.description = data.get('description', epic.description)
        epic.status = data.get('status', epic.status)
        epic.priority = data.get('priority', epic.priority)
        epic.assigned_to_id = data.get('assigned_to_id', epic.assigned_to_id)
        epic.start_date = data.get('start_date', epic.start_date)
        epic.target_date = data.get('target_date', epic.target_date)
        epic.business_value = data.get('business_value', epic.business_value)
        epic.acceptance_criteria = data.get('acceptance_criteria', epic.acceptance_criteria)
        epic.estimated_effort = data.get('estimated_effort', epic.estimated_effort)
        
        # Set tags
        if 'tags' in data:
            epic.tags = data['tags']
        
        db.session.commit()
        
        return epic
    
    @staticmethod
    def delete_epic(epic):
        """Delete an epic."""
        db.session.delete(epic)
        db.session.commit()
