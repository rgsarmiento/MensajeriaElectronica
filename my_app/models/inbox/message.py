from datetime import datetime
from my_app import db
from markupsafe import Markup
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)    
    user_id_from = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False)    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id_from, user_id_to, subject, message, status) -> None:
        self.user_id_from=user_id_from
        self.user_id_to=user_id_to
        self.subject=subject
        self.message=message
        self.status=status

    @staticmethod
    def get_by_id(id):
        return Message.query.get(id)

    @staticmethod
    def get_all_sent(id):
        return Message.query.filter(Message.user_id_from == id).order_by(Message.created.desc()).all()

    @staticmethod
    def get_all_received(id):
        return Message.query.filter(Message.user_id_to == id).order_by(Message.created.desc()).all()
    
    @staticmethod
    def get_all_received_new(id):
        return Message.query.filter(Message.user_id_to == id, Message.status == 0).order_by(Message.created.desc()).all()

    @staticmethod
    def to_html(html):
        return Markup(html)