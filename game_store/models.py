from game_store import db, login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Numeric(4, 2))
    orders = db.relationship("Order", cascade="all, delete-orphan")
    returns = db.relationship("Return", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Customer('{self.username}', '{self.email}', '{self.balance}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    received = db.Column(db.Date, nullable=False)
    shipped = db.Column(db.Date, nullable=False)
    order_details = db.relationship("Odetails", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Order('{self.received}', '{self.shipped}')"


class Odetails(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    qty = db.Column(db.Integer)

    def __repr__(self):
        return f"Odetails('{self.qty}')"


class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Return('{self.date}')"


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Publisher('{self.publisher_name}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Numeric(4, 2), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
    order_details = db.relationship("Odetails", cascade="all, delete-orphan")
    runs = db.relationship("Run", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Game('{self.game_name}', '{self.genre}', '{self.release_date}', '{self.price}', '{self.publisher_id}')"


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Numeric(4, 2), nullable=False)
    runs = db.relationship("Run", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Game('{self.platform_name}', '{self.release_date}', '{self.price}')"


class Run(db.Model):
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)

    def __repr__(self):
        return f"Run('{self.platform_id}', '{self.game_id}')"


db.drop_all()
db.create_all()
games = [
    Game(game_name="Assassin's Creed", genre="action-adventure", release_date=datetime.date(2007, 11, 13), price=10.00,
         publisher_id=1),
    Game(game_name="Assassin's Creed II", genre="action-adventure", release_date=datetime.date(2009, 11, 17),
         price=15.00, publisher_id=1),
    Game(game_name="Assassin's Creed III", genre="action-adventure", release_date=datetime.date(2012, 10, 30),
         price=25.00, publisher_id=1),
    Game(game_name="Assassin's Creed Brotherhood", genre="action-adventure", release_date=datetime.date(2010, 11, 16),
         price=15.00, publisher_id=1),
    Game(game_name="Assassin's Creed Revelations", genre="action-adventure", release_date=datetime.date(2011, 11, 15),
         price=20.00, publisher_id=1),
    Game(game_name="Mass Effect 2", genre="action role-playing", release_date=datetime.date(2010, 1, 26), price=10.00,
         publisher_id=2),
    Game(game_name="Need for Speed", genre="racing", release_date=datetime.date(2015, 11, 3), price=25.00,
         publisher_id=2),
    Game(game_name="Anthem", genre="action role-playing", release_date=datetime.date(2019, 2, 22), price=60.00,
         publisher_id=2),
    Game(game_name="Titanfall", genre="first-person shooter", release_date=datetime.date(2014, 3, 11), price=20.00,
         publisher_id=2),
    Game(game_name="Battlefield 4", genre="first-person shooter", release_date=datetime.date(2013, 10, 29), price=15.00,
         publisher_id=2),
    Game(game_name="Call of Duty World at War", genre="first-person shooter", release_date=datetime.date(2008, 11, 11),
         price=5.00, publisher_id=3),
    Game(game_name="Destiny", genre="first-person shooter", release_date=datetime.date(2014, 9, 9), price=20.00,
         publisher_id=3),
    Game(game_name="Call of Duty Black Ops 4", genre="first-person shooter", release_date=datetime.date(2018, 10, 12),
         price=50.00, publisher_id=3),
    Game(game_name="Crash Bandicoot", genre="platform", release_date=datetime.date(2017, 6, 30), price=40.00,
         publisher_id=3),
    Game(game_name="Tony Hawk's Pro Skater", genre="sports", release_date=datetime.date(1999, 7, 31), price=2.00,
         publisher_id=3),
    Game(game_name="Bloodborne", genre="action role-playing", release_date=datetime.date(2015, 3, 24), price=30.00,
         publisher_id=4),
    Game(game_name="God of War", genre="action-adventure", release_date=datetime.date(2018, 4, 20), price=60.00,
         publisher_id=4),
    Game(game_name="The Last of Us", genre="action-adventure", release_date=datetime.date(2014, 7, 29), price=20.00,
         publisher_id=4),
    Game(game_name="Ratchet and Clank", genre="platform", release_date=datetime.date(2016, 4, 12), price=40.00,
         publisher_id=4),
    Game(game_name="Infamous Second Son", genre="action-adventure", release_date=datetime.date(2014, 3, 21),
         price=20.00, publisher_id=4),
    Game(game_name="The Legend of Zelda: Breath of the Wild", genre="action-adventure",
         release_date=datetime.date(2017, 3, 3), price=50.00, publisher_id=5),
    Game(game_name="Super Mario Odyssey", genre="platform", release_date=datetime.date(2017, 10, 27), price=50.00,
         publisher_id=5),
    Game(game_name="Super Smash Bros. Ultimate", genre="fighting", release_date=datetime.date(2018, 12, 7), price=60.00,
         publisher_id=5),
    Game(game_name="Splatoon 2", genre="third-person shooter", release_date=datetime.date(2017, 7, 21), price=50.00,
         publisher_id=5),
    Game(game_name="Animal Crossing: New Leaf", genre="social simulation", release_date=datetime.date(2012, 11, 8),
         price=15.00, publisher_id=5)
]

db.session.bulk_save_objects(games)
db.session.commit()

publishers = [
    Publisher(publisher_name="Ubisoft"),
    Publisher(publisher_name="EA"),
    Publisher(publisher_name="Activision"),
    Publisher(publisher_name="Sony"),
    Publisher(publisher_name="Nintendo")
]

db.session.bulk_save_objects(publishers)
db.session.commit()
