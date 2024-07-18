from src import db
from src.models.User import roles_users

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String())
    subcategory = db.Column(db.String())
    company_id = db.Column(db.Integer(), db.ForeignKey('company.company_id'))
    users = db.relationship("User", secondary=roles_users, back_populates="roles")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'subcategory': self.subcategory
        }