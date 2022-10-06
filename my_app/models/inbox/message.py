from datetime import datetime
from my_app import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)    
    user_id_from = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, ondelete='CASCADE')
    user_id_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, ondelete='CASCADE')
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.integer, nullable=False)    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)