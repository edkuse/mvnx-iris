from datetime import datetime
from sqlalchemy.sql import func
from iris.extensions import db
import json
import uuid


# String constants for Epic status
class EpicStatus:
    DRAFT = 'draft'
    PLANNED = 'planned'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    @classmethod
    def values(cls):
        return [cls.DRAFT, cls.PLANNED, cls.IN_PROGRESS, cls.COMPLETED, cls.CANCELLED]
    

# String constants for Priority
class PriorityLevel:
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'
    
    @classmethod
    def values(cls):
        return [cls.LOW, cls.MEDIUM, cls.HIGH, cls.CRITICAL]
    

class Epic(db.Model):
    __tablename__ = 'epics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default=EpicStatus.DRAFT, nullable=False)
    priority = db.Column(db.String(20), default=PriorityLevel.LOW, nullable=False)
    
    # Relationships
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_by = db.relationship('User', foreign_keys=[created_by_id])
    
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])
    
    # Dates
    start_date = db.Column(db.Date)
    target_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields
    business_value = db.Column(db.Text)
    acceptance_criteria = db.Column(db.Text)
    estimated_effort = db.Column(db.Integer)  # In hours or story points
    tags_json = db.Column(db.Text, default='[]')
    
    @property
    def tags(self):
        """Get tags as a list."""
        if not self.tags_json:
            return []
        return json.loads(self.tags_json)
    
    @tags.setter
    def tags(self, value):
        """Set tags from a list."""
        self.tags_json = json.dumps(value)
    
    @property
    def completion_percentage(self):
        """Calculate the completion percentage of the epic based on its status."""
        if self.status == EpicStatus.COMPLETED:
            return 100
        elif self.status == EpicStatus.CANCELLED:
            return 0
        elif self.status == EpicStatus.IN_PROGRESS:
            return 50
        elif self.status == EpicStatus.PLANNED:
            return 25
        elif self.status == EpicStatus.DRAFT:
            return 0
        return 0
    
    @property
    def days_until_target(self):
        """Calculate days until target date."""
        if not self.target_date:
            return None
        
        today = datetime.utcnow().date()
        delta = (self.target_date - today).days
        return delta
    
    def to_dict(self):
        """Convert epic to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_by_id': self.created_by_id,
            'assigned_to_id': self.assigned_to_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'business_value': self.business_value,
            'acceptance_criteria': self.acceptance_criteria,
            'estimated_effort': self.estimated_effort,
            'tags': self.tags,
            'completion_percentage': self.completion_percentage
        }
