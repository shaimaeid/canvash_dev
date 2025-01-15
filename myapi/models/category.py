# In models/category.py

from datetime import datetime
from myapi.models import db
  # Import db from the same package to avoid circular import issues

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert model instance to dictionary for easy serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'icon': self.icon,
            'created_at': self.created_at.isoformat()
        }
