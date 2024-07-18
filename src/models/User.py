from src import db

roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), primary_key=True),
                       db.Column("role_id", db.Integer(), db.ForeignKey("role.id"), primary_key=True))

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    public_id = db.Column(db.String(50), unique = True)
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(1000))
    company_id = db.Column(db.Integer(), db.ForeignKey('company.company_id'))
    documents = db.relationship('Document', backref= 'User')
    roles = db.relationship("Role", secondary=roles_users, back_populates="users")

    def to_dict(self):
        return {
            "public_id" : self.public_id,
            "firstName" : self.firstName, 
            "lastName" : self.lastName,
            "email" : self.email,
            "company_id" : self.company_id,
            "roles" : [role.name for role in self.roles]
        }

