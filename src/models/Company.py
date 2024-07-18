from src import db

class Company(db.Model):
    company_id = db.Column(db.Integer(), primary_key = True, unique = True)
    company_name = db.Column(db.String(255))
    admin_email = db.Column(db.String(70), unique = True)
    users = db.relationship('User', backref= 'User', cascade="all,delete")
    roles = db.relationship('Role', backref= 'Role', cascade="all,delete")