from datetime import datetime
from iris.extensions import db


class TimestampMixin:
    """Mixin that adds created_at and updated_at columns to a model."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class CRUDMixin:
    """Mixin that adds convenience methods for CRUD operations."""
    
    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it to the database."""
        instance = cls(**kwargs)
        return instance.save()
    
    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() if commit else self
    
    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
    
    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            db.session.commit()
        return self
