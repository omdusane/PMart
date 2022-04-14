from unicodedata import name
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from . import db
from website.models import Item
from datetime import date


views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    try:
        if current_user.id:
             if request.method == "POST":
                item_to_search = request.form.get('name')
                item = Item.query.filter_by(name=item_to_search).first()
                print(item)
                print(item_to_search)
                if item:
                    id = item.id
                    #return render_template("report.html", user=current_user, item=item)
                    return redirect(url_for("views.report",id=id))
                else:
                    flash("Searched item does not exists.")
    except Exception as e:
        return redirect(url_for('auth.login'))
        
    return render_template("home.html", user=current_user)

@views.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        company = request.form.get('company')
        price = request.form.get('price')
        description = request.form.get('description')
        rack = request.form.get('rack')
        m_date = request.form.get('m_date')
        e_date = request.form.get('e_date')

        item = Item.query.filter_by(name=name).first()

        if item:
            item.quantity += int(quantity)
            item.last_modified_date = date.today()
            db.session.commit()
            flash('Item Updated', category='success')
        else:
            new_item = Item(name=name,category=category,quantity=quantity,price=price,company=company,description=description, rack_no = rack, manufactured_date = m_date, expiry_date=e_date, user_id=current_user.id)
            db.session.add(new_item)
            db.session.commit()
            flash('Item Added!', category='success')
    
    return render_template('add_item.html', user=current_user)

@views.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        #what if item of entered name does not exists
        item_to_delete = Item.query.filter_by(name=name).first()
        if int(item_to_delete.quantity) < int(quantity):
            flash('Amount entered is more than available Quantity', category='error')
        elif int(item_to_delete.quantity) == int(quantity):
            id = item_to_delete.id
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Item deleted Succesfully.!', category='success')
        else:
            item_to_delete.quantity = int(item_to_delete.quantity) - int(quantity)
            db.session.commit()
            flash('Entered Quantity deleted Succesfully.', category='success')

    return render_template('delete_item.html', user = current_user)


        


@views.route('/categories', methods=['GET', 'POST'])
def categories():
    items = Item.query.order_by(Item.rack_no).all()
    return render_template("categories.html", items=items, user=current_user)

@views.route('/report/<int:id>', methods=['GET', 'POST'])
def report(id):
    item = Item.query.filter_by(id=id).first()
    if item.quantity < 10:
        flash('Quantity in stock is too low.!!')
    return render_template('report.html', Item = item, user=current_user)

@views.route('/expired_items', methods=['GET', 'POST'])
def expired_items():
    if request.method =='POST':
        item = request.form.get('name')
        item_to_delete = Item.query.filter_by(name=name).first()
        item_name= item_to_delete.name
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f"{item_name} deleted succesfully.", category='success')
    expired = Item.query.filter(Item.expiry_date >= date.today())
    return render_template('expired.html', expired=expired, user=current_user)