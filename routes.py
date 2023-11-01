from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, LoginManager
from .models import Food, Counter, Orders, User
from . import db
import random
from datetime import date



routes = Blueprint('routes',__name__)
login_manager = LoginManager()
@routes.route('/home', methods = ['GET','POST'])
@login_required
@login_manager.user_loader
def home():
    if session.get('user_type') == 'hcl':
        counter_select = Counter.query.all()
        if request.method == 'POST':
            food_query = request.form.get('food_query')
            counter_query = request.form.get('counter_query')

            if food_query:
                food_results = Food.query.filter(Food.name.ilike(f"%{food_query}%")).all()
                return render_template('home.html', food_results=food_results, food_query=food_query, counter_select=counter_select, user=current_user)

            if counter_query:
                counter = Counter.query.filter_by(name=counter_query).all()
                return render_template('home.html', counter=counter, counter_query=counter_query, counter_select=counter_select, user=current_user)

        return render_template('home.html', counter_select=counter_select, user=current_user)
    counter_select = Counter.query.all()
    return render_template('home.html', counter_select=counter_select, user=current_user)

@routes.route('/myorders', methods=['GET','POST'])
@login_required
@login_manager.user_loader
def myorders():
    data = Orders.query.all()

    
    return render_template('myorders.html', data=data,  user=current_user)

@routes.route('/vendor', methods = ['GET','POST'])
@login_required
@login_manager.user_loader
def vendor():
    if session.get('user_type') == 'vendor':
        logged_in_user = current_user.email
        email_part = logged_in_user.split('@')
        name = email_part[0]

        orders = Orders.query.filter_by(counter_name=name).all()

        return render_template('vendor.html', data=orders)

@routes.route('/admin', methods = ['GET','POST'])
@login_required
@login_manager.user_loader
def admin():
    if session.get('user_type') == 'admin':
        if request.method == 'POST':
            food_name = request.form.get('food')
            price = request.form.get('price')
            counter = request.form.get('counter')
            quan = request.form.get('quan')

            counter_name = Counter.query.filter_by(name=counter).first()
            if counter_name is not None:
                new_table = Food(name=food_name, price=price,counter_name=counter,quantity=quan, counter=counter_name)
                db.session.add(new_table)
                db.session.commit()
            else:
                new_counter = Counter(name=counter)
                new_table = Food(name=food_name, price=price,counter_name=counter,quantity=quan, counter=new_counter)
                db.session.add(new_counter)
                db.session.add(new_table)
                db.session.commit()




        counter_details = Counter.query.all()


        return render_template('admin.html', counter_details=counter_details)

@routes.route('/update', methods=['GET','POST'])
@login_required
def update():
    if request.method == 'POST':
        my_data = Food.query.get(request.form.get('id'))
        my_data.name = request.form['edit_food']
        my_data.price = request.form['edit_price']
        my_data.quantity = request.form['edit_quantity']
        db.session.commit()
        flash('Feedback Updated')

        return redirect(url_for('routes.admin'))
    
@routes.route('/delete/<id>/', methods = ['GET','POST'])
@login_required
def delete(id):
    my_data = Food.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Task Deleted")

    return redirect(url_for('routes.admin'))

@routes.route('/delete_counter/<id>/', methods = ['GET','POST'])
@login_required
def delete_counter(id):
    my_data = Counter.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Task Deleted")

    return redirect(url_for('routes.admin'))

@routes.route('/delete_order/<id>/', methods = ['GET','POST'])
@login_required
def delete_order(id):
    my_data = Orders.query.get(id)
    db.session.delete(my_data)
    db.session.commit()


    return redirect(url_for('routes.myorders'))

@routes.route('/order', methods=['GET','POST'])
def order():
    counter_select = Counter.query.all()
    if request.method == 'POST':
        food = Food.query.get(request.form.get('id'))
        food_name = food.name
        quantity = request.form['quantity']
        time_slot = request.form['time_slot']
        counter_name = request.form['counter']
        rand = random.randint(1, 9999)
        ord_id = f'ORD000{rand}'

        
        today = date.today()
        status = 'Processing'

        new_order = Orders(food_name=food_name, quantity=quantity, time_slot=time_slot, counter_name=counter_name,status=status,ord_id=ord_id,date=today, user_id=current_user.id)
        db.session.add(new_order)
        db.session.commit()

        int_quantity = int(quantity)
        food.sold = food.sold + int_quantity

        food.quantity = food.quantity - food.sold
        db.session.commit()

        return render_template('home.html', user=current_user, counter_select=counter_select)



    return render_template('home.html')

@routes.route('/status', methods=['GET','POST'])
@login_required
def status():
    if request.method == 'POST':
        domain_id = request.form['domain_id']
        status_data = Orders.query.get(request.form.get('id'))

        if domain_id == 'vendor':
            status_data.status = 'Ready to collect'
            db.session.commit()

            return redirect(url_for('routes.vendor'))

        elif domain_id == 'employee':
            status_data.status = 'Closed'
            db.session.commit()

            return redirect(url_for('routes.myorders'))
        

@routes.route('/reports', methods=['GET','POST'])
@login_required
def reports():
    from_date = request.form.get('from')
    to_date = request.form.get('to')
    counter = request.form.get('counter')

    if from_date == to_date:
        data = Counter.query.filter_by(name=counter).all()


            
            

        return render_template('reports.html', data=data)


    return render_template('reports.html')






