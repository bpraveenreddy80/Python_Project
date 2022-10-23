from markets import db
from markets import app,bcrypt
from markets import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=30), nullable=False, unique=True)
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
   
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    email_add = db.Column(db.String(length=40),nullable=False,unique=True)
    password_hash = db.Column(db.String(length=60),nullable=False)
    budget = db.Column(db.Integer(), default=10000)
    items = db.relationship('Item',backref='owned_user',lazy=True)
    
    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'
    @property
    def password(self):
        return self.password
    
    @password.setter 
    def password(self,plain_text_pwd):
        self.password_hash = bcrypt.generate_password_hash(plain_text_pwd).decode('utf-8')
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def check_purchase(self,obj):
        return self.budget >= obj.price
    