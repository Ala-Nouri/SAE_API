from src import db
from src.models.User import User

class Document(db.Model):
    document_id = db.Column(db.Integer(), primary_key=True)
    file_name = db.Column(db.String(255), unique=True)
    category = db.Column(db.String(255))
    subcategory = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime())
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'))
    properties = db.relationship('Property', backref='document', cascade="all,delete")
    file_path = db.Column(db.String(255))
    company_id = db.Column(db.Integer(), db.ForeignKey('company.company_id'))
    encryption_Key = db.Column(db.String())
    archived = db.Column(db.Boolean())

    def to_dict(self):
        user = User.query.filter_by(id= self.created_by).first_or_404()
        return {
            'document_id': self.document_id,
            'file_name': self.file_name,
            'category': self.category,
            'subcategory': self.subcategory,
            'upload_date': self.upload_date.isoformat(),
            'created_by': user.to_dict(),
            'properties': [property.to_dict() for property in self.properties],
            'file_path': self.file_path,
            'company_id': self.company_id,
            'archived': self.archived
        }