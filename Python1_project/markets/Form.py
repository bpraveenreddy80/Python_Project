from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, TextAreaField,EmailField,SubmitField, PasswordField
from wtforms.validators import Length, EqualTo, Email,DataRequired


class RegisterForm(FlaskForm):
    u_name = StringField('User Name',validators=[Length(min=2, max=30),DataRequired()])
    email = EmailField('Email',validators=[Email(), DataRequired()])
    password = PasswordField('Password',validators=[Length(min=6, max=30), DataRequired()])
    Password_c = PasswordField('Passwod confirmantion',validators=[EqualTo('password'), DataRequired()])
    Submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    u_name = StringField('User Name',validators=[Length(min=2, max=30),DataRequired()])
    password = PasswordField('Password',validators=[Length(min=6, max=30), DataRequired()])
    Submit = SubmitField('Login Account')
    
class addItemForm(FlaskForm):
    name = StringField('Item Name',validators=[Length(min=2, max=30),DataRequired()])
    price = IntegerField('Price')
    barcode = StringField('Barcode')
    description = TextAreaField('description')
    Submit = SubmitField('Add Product')
    
    
class PurchaseItemForm(FlaskForm):
    submit = SubmitField('Purchase Item')
    
    
class SellItem(FlaskForm):
    submit = SubmitField('Sell Item')
    