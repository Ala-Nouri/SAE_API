from src import db

class Property(db.Model):
    property_id = db.Column(db.Integer(), primary_key=True)
    document_id = db.Column(db.Integer(), db.ForeignKey('document.document_id'))
    property_name = db.Column(db.String(255))
    property_value= db.Column(db.Text())

    def to_dict(self):
        return {
            'property_id': self.property_id,
            'document_id': self.document_id,
            'property_name': self.property_name,
            'property_value': self.property_value
        }