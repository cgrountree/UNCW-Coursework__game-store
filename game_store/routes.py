from flask import render_template, url_for, flash, redirect, request
from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, BuyForm, ReturnForm
from game_store.models import Customer, Purchase, Return
from flask_login import login_user, current_user, logout_user, login_required
from game_store.models import Game, Publisher
import datetime


@app.route("/")
@app.route("/home")
def home():
    publishers = Publisher.query.all()
    games = Game.query.all()
    return render_template('home.html', games=games, publishers=publishers)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/game/<selected_game>", methods=['GET', 'POST'])
@login_required
def game(selected_game):
    form = BuyForm()
    if form.validate_on_submit():
        game_name = selected_game
        buying_game = Game.query.filter_by(game_name=game_name).first()
        total_price = form.quantity.data * buying_game.price
        flash(str(total_price))
        current_user.balance -= total_price
        this_purchase = Purchase(customer_id=current_user.id, date=datetime.datetime.now(), game_id=buying_game.id, qty=form.quantity.data)
        db.session.add(this_purchase)
        db.session.commit()
        flash('your purchase was successful')
        return redirect(url_for('account'))
        # try:
        #     db.session.commit()
        #     flash('your purchase was successful')
        #     return redirect(url_for('account'))
        # except:
        #     db.session.rollback()
        #     flash('You do not have enough money for this purchase.')

    return render_template('game.html', game=selected_game, form=form, title='Game')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password, balance=40.00)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    orders = Purchase.query.all()
    games = Game.query.all()
    returns = Return.query.all()
    return render_template('account.html', orders=orders, games=games, returns=returns)

@app.route("/returns/<selected_purchase>", methods=['GET', 'POST'])
def returns(selected_purchase):
    form = ReturnForm()

    if form.validate_on_submit():
        thereturn = Return(current_user.id, datetime.datetime.now(), selected_purchase)
        db.session.add(thereturn)
        db.session.commit()
        return redirect(url_for('account'))

    return render_template('returns.html', form=form, title='Returns')

