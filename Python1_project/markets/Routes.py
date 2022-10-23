from markets import app
from flask import render_template,redirect,url_for, flash, request
from markets import Model,db
from markets.Model import Item, User
from markets.Form import RegisterForm, addItemForm, LoginForm, PurchaseItemForm, SellItem
from flask_login import login_user, logout_user, login_required, current_user

db.init_app(app)


@app.route('/')
def home():
    return render_template('Starter.html')


@app.route('/home')
# @login_required
def index():
    return render_template('home.html')

@app.route('/createTable')
@login_required
def create():
    db.create_all()
    return 'Tables created sucessfully'

@app.route('/addItem', methods = ['GET','POST'])
@login_required
def addItem():
    form = addItemForm()
    if form.validate_on_submit():
        add_item = Item(name = form.name.data,price = form.price.data,barcode = form.barcode.data,description = form.description.data)
        db.session.add(add_item)
        db.session.commit()
        return redirect(url_for('market'))
    return render_template('additem.html',form = form)

@app.route('/Register', methods = ['GET','POST'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.u_name.data,email_add=form.email.data,password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('Login'))
    if  form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error with :{ err_msg }')
    
    return render_template('Register.html',form=form)
    
@app.route('/Login', methods =['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name = form.u_name.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Your Login was sucessful {form.u_name.data}')
            return redirect(url_for('market'))
        else:
            flash('User Name and password did\' match Try again with correct UserName and Password')    
            
    return render_template('Login.html',form=form)


@app.route('/Logout')
def Logout():
    logout_user()
    # flash('Logout sucessfull ')   
    return render_template('Starter.html')
    
@app.route('/market',methods=['GET','POST'])   
@login_required
def market():
    form_purchase = PurchaseItemForm()
    form_sell = SellItem()
    #puchase item logic
    if request.method == 'POST':
        purchase_item = request.form.get('purchase_item')
        p_item_obj = Item.query.filter_by(name=purchase_item).first()
        if p_item_obj:
            if current_user.check_purchase(p_item_obj):
                p_item_obj.owner = current_user.id
                current_user.budget -= p_item_obj.price
                db.session.commit()
            else:
                flash(f'Budget is less than item price { purchase_item}')
                print("Budget is less than item price",purchase_item)
                return redirect(url_for('market'))
    
        #sell item logic
        if form_sell.validate_on_submit():
            sold_item = request.form.get('Sell_item')
            s_item_obj = Item.query.filter_by(name = sold_item).first()
            if s_item_obj and s_item_obj.owner!='':
                current_user.budget += s_item_obj.price
                s_item_obj.owner=None
                db.session.commit()
        
    if request.method == 'GET':
        dic = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',dic = dic, purchase_form = form_purchase,selling_form=form_sell, owned_items = owned_items)
    
    return redirect(url_for('market'))