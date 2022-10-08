from datetime import datetime
from my_app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # ondelete='CASCADE')

    def __init__(self, user_name, email, active, password) -> None:
        self.user_name=user_name
        self.email=email
        self.active=active
        self.password=password
        
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email_or_user_name(email_, user_name_):
        return User.query.filter((User.email == email_) | (User.user_name == user_name_)).first()

    @staticmethod
    def get_by_email(email_):
        return User.query.filter(User.email == email_).first()
    
    @staticmethod
    def get_all_except_me(id):
        return User.query.filter(User.id != id).order_by(User.user_name).all()