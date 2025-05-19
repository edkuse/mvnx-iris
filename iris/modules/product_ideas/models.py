from iris.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Text, CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property


# Define constants for status, priority, and impact level
class ProductIdeaStatus:
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    
    @classmethod
    def values(cls):
        return [cls.DRAFT, cls.SUBMITTED, cls.UNDER_REVIEW, cls.APPROVED, cls.REJECTED, cls.IMPLEMENTED]


class PriorityLevel:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    @classmethod
    def values(cls):
        return [cls.LOW, cls.MEDIUM, cls.HIGH, cls.CRITICAL]


class ImpactLevel:
    MINIMAL = "minimal"      # Affects a small number of users or has minor improvements
    MODERATE = "moderate"    # Affects a significant user segment or provides notable improvements
    SIGNIFICANT = "significant"  # Affects most users or provides major improvements
    TRANSFORMATIVE = "transformative"  # Game-changing feature that transforms the product experience
    
    @classmethod
    def values(cls):
        return [cls.MINIMAL, cls.MODERATE, cls.SIGNIFICANT, cls.TRANSFORMATIVE]


class ProductIdea(db.Model):
    __tablename__ = 'product_ideas'
    __table_args__ = (
        CheckConstraint(
            f"status IN ({','.join([f"'{v}'" for v in ProductIdeaStatus.values()])})",
            name='check_status_values'
        ),
        CheckConstraint(
            f"priority IN ({','.join([f"'{v}'" for v in PriorityLevel.values()])})",
            name='check_priority_values'
        ),
        CheckConstraint(
            f"impact_level IN ({','.join([f"'{v}'" for v in ImpactLevel.values()])})",
            name='check_impact_values'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Status and priority as strings with check constraints
    status = db.Column(
        db.String(20),
        default=ProductIdeaStatus.DRAFT,
        nullable=False
    )
    
    priority = db.Column(
        db.String(20),
        default=PriorityLevel.LOW,
        nullable=False
    )
    
    # Impact level as string with check constraint
    impact_level = db.Column(
        db.String(20),
        default=ImpactLevel.MODERATE,
        nullable=False
    )
    
    # Relationships with User model
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref=db.backref('created_ideas', lazy='dynamic'))
    
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref=db.backref('assigned_ideas', lazy='dynamic'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    target_date = db.Column(db.DateTime)
    
    # Additional fields
    business_value = db.Column(db.Text)
    technical_feasibility = db.Column(db.Text)
    estimated_effort = db.Column(db.Integer)  # In hours or story points
    
    # Tags
    tags = db.Column(ARRAY(Text))
    
    # Hybrid properties
    @hybrid_property
    def is_active(self):
        """Check if the idea is in an active state (not rejected or implemented)."""
        return self.status not in [ProductIdeaStatus.REJECTED, ProductIdeaStatus.IMPLEMENTED]
    
    @hybrid_property
    def days_since_creation(self):
        """Calculate days since the idea was created."""
        if self.created_at:
            return (datetime.utcnow() - self.created_at).days
        return None
    
    @hybrid_property
    def days_until_target(self):
        """Calculate days until the target date."""
        if self.target_date:
            return (self.target_date - datetime.utcnow()).days
        return None
    
    @hybrid_property
    def value_score(self):
        """Calculate a value score based on priority and impact level."""
        priority_weights = {
            PriorityLevel.LOW: 1,
            PriorityLevel.MEDIUM: 2,
            PriorityLevel.HIGH: 3,
            PriorityLevel.CRITICAL: 4
        }
        
        impact_weights = {
            ImpactLevel.MINIMAL: 1,
            ImpactLevel.MODERATE: 2,
            ImpactLevel.SIGNIFICANT: 3,
            ImpactLevel.TRANSFORMATIVE: 4
        }
        
        priority_weight = priority_weights.get(self.priority, 2)
        impact_weight = impact_weights.get(self.impact_level, 2)
        
        # Value score is a combination of priority and impact
        return priority_weight * impact_weight
    
    # Helper methods
    def get_tags_list(self):
        """Get tags as a list, regardless of database type."""
        if isinstance(self.tags, list):
            return self.tags
        elif isinstance(self.tags, str) and self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def set_tags_list(self, tags_list):
        """Set tags from a list, handling different database types."""
        if isinstance(self.tags, list) or hasattr(self.tags, 'append'):
            self.tags = tags_list
        else:
            self.tags = ','.join(tags_list)
    
    def to_dict(self):
        """Convert the model to a dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'impact_level': self.impact_level,
            'created_by': {
                'id': self.created_by.id,
                'name': self.created_by.display_name
            } if self.created_by else None,
            'assigned_to': {
                'id': self.assigned_to.id,
                'name': self.assigned_to.display_name
            } if self.assigned_to else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'business_value': self.business_value,
            'technical_feasibility': self.technical_feasibility,
            'estimated_effort': self.estimated_effort,
            'tags': self.get_tags_list(),
            'is_active': self.is_active,
            'days_since_creation': self.days_since_creation,
            'days_until_target': self.days_until_target,
            'value_score': self.value_score
        }
    
    def __repr__(self):
        return f'<ProductIdea {self.id}: {self.title}>'
    