from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


# User --------------------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    
    def __init__(self, name, username, password):
        self.name=name
        self.username=username
        self.password = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password, password)


# Company -----------------------------------------------------------
class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_reason = db.Column(db.String(150), nullable=False)
    fantasy = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
    zip_code = db.Column(db.String(11), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __init__(self, company_reason, fantasy, address, id_number, zip_code, city, state, email, phone):
        self.company_reason=company_reason
        self.fantasy=fantasy
        self.address=address
        self.id_number=id_number
        self.zip_code=zip_code
        self.city=city
        self.state=state
        self.email=email
        self.phone=phone


# Employee ----------------------------------------------------------
class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    date_admission = db.Column(db.String)

    def __init__(self, name, phone, date_admission):
        self.name=name
        self.phone=phone
        self.date_admission=date_admission


# Category ----------------------------------------------------------
class Category(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    categories = db.relationship('Product', backref='category', cascade="all,delete") 

    def __init__(self, name):
        self.name=name


# Brand -------------------------------------------------------------
class Brand(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    brands = db.relationship('Product', backref='brand', cascade="all,delete") 

    def __init__(self, name):
        self.name=name

class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    code = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)
    cost_price = db.Column(db.Numeric(11,2), nullable=False)
    saler_price = db.Column(db.Numeric(11,2), nullable=False)
    profit = db.Column(db.Numeric(11,2), nullable=False)

    def __init__(self, code, category_id, brand_id, name, description, cost_price, saler_price, profit):
        self.code=code
        self.category_id=category_id
        self.brand_id=brand_id
        self.name=name
        self.description=description
        self.cost_price=cost_price
        self.saler_price=saler_price
        self.profit=profit


# descomente para criar o banco
db.create_all()
