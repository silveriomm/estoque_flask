#####################################################################
# Controle de estoque usando Flask e SQLite
#####################################################################

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import app, db
from models import User, Category, Brand, Employee, Company, Product, generate_password_hash


# Home (Início)
#---------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')

# Users (Usuários)
#---------------------------------------------------------------------------

@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name, email, password)
        try:
            db.session.add(user)
            db.session.commit()
            if current_user.is_authenticated:
                flash('Usuário cadastrado com sucesso!','alert alert-success')
                return redirect(url_for('user'))
            else:
                flash('Usuário cadastrado com sucesso!','alert alert-success')
                return redirect(url_for('login'))
        except:
            db.session.rollback()
            if current_user.is_authenticated:
                flash('Email ou usuário já cadastrado!','alert alert-danger')
                return redirect(url_for('user'))
            else:
                flash('Email ou usuário já cadastrado!','alert alert-danger')
                return redirect(url_for('login'))
    
    return render_template('user.html')


@app.route('/user_view/<int:user_id>', methods=['GET'])
def user_view(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template('user_view.html', user=user)


@app.route('/user_edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template('user_edit.html', user=user)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = generate_password_hash(request.form['password'])
        try:
            db.session.commit()
            flash('Usuario alterado com sucesso!', 'alert alert-success')
            return render_template('user_edit.html', user=user)
        except:
            db.session.rollback()
            flash('Email ou usuário já existe!', 'alert alert-danger')
            return render_template('user_edit.html', user=user)
    else:
        return render_template('user_edit.html', user=user)

@app.route('/user_delete/<int:user_id>', methods=['GET'])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        try:
            db.session.delete(user)
            db.session.commit()
            flash('Usuário excluído com sucesso!', 'alert alert-warning')
            return redirect(url_for('users'))
        except:
            db.session.rollback()
            flash('Erro ao excluir usuário!', 'alert alert-danger')
            return redirect(url_for('users'))

# Fim de User

# Company (Empresa)
#---------------------------------------------------------------------------

@app.route('/company', methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        company_reason = request.form['company_reason']
        fantasy = request.form['fantasy']
        address = request.form['address']
        id_number = request.form['id_number']
        zip_code = request.form['zip_code']
        city = request.form['city']
        state = request.form['state']
        email = request.form['email']
        phone = request.form['phone']
        company = Company(company_reason, fantasy, address, id_number, zip_code, city, state, email, phone)
        try:
            db.session.add(company)
            db.session.commit()
            flash('Empresa cadastrada com sucesso', 'alert alert-success')
            return redirect(url_for('company_view'))
        except:
            db.session.rollback()
            flash('Erro ao cadastrar empresa', 'alert alert-danger')
            return redirect(url_for('company_view'))

    return render_template('company.html')


@app.route('/company_view')
def company_view():
    if Company.query.count() <= 0:
        return redirect(url_for('company'))
    else:
        company = Company.query.first()
        return render_template('company_view.html', company=company)


@app.route('/company_edit/<int:company_id>', methods=['GET', 'POST'])
def company_edit(company_id):
    company = Company.query.first()
    if request.method == 'GET':
        return render_template('company_edit.html', company=company)

    if request.method == 'POST':
        company.company_reason = request.form['company_reason']
        company.fantasy = request.form['fantasy']
        company.address = request.form['address']
        company.id_number = request.form['id_number']
        company.zip_code = request.form['zip_code']
        company.city = request.form['city']
        company.state = request.form['state']
        company.email = request.form['email']
        company.phone = request.form['phone']
        db.session.commit()
        flash('Empresa alterada com sucesso!', 'alert alert-success')
        return render_template('company_view.html', company=company)
    else:
        flash('Erro ao alterar empresa!', 'alert alert-danger')
        return render_template('company_edit.html', company=company)


@app.route('/company_delete/<int:company_id>', methods=['GET'])
def company_delete(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == 'GET':
        try:
            db.session.delete(company)
            db.session.commit()
            flash('Empresa excluída com sucesso!', 'alert alert-warning')
            return redirect(url_for('company'))
        except:
            flash('Erro ao excluir empresa!', 'alert alert-danger')
            return redirect(url_for('company'))


# Fim de Company

# Employees (Vendedor ou Funcionário)
#-----------------------------------------------------------------------


@app.route('/employees', methods=['GET'])
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)


@app.route('/employee_view/<int:employee_id>', methods=['GET'])
def employee_view(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'GET':
        return render_template('employee_view.html', employee=employee)


@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date_admission = request.form['date_admission']
        employee = Employee(name, phone, date_admission)
        try:
            db.session.add(employee)
            db.session.commit()
            flash('Funcionário cadastrado com sucesso!', 'alert alert-success')
            return redirect(url_for('employee'))
        except:
            flash('Já existe um funcionário com este nome!', 'alert alert-danger')
            return redirect(url_for('employee'))
    
    return render_template('employee.html')

@app.route('/employee_edit/<int:employee_id>', methods=['GET', 'POST'])
def employee_edit(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'GET':
        return render_template('employee_edit.html', employee=employee)

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.phone = request.form['phone']
        employee.date_admission = request.form['date_admission']
        try:
            db.session.commit()
            flash('Funcionário alterado com sucesso!', 'alert alert-success')
            return render_template('employee_edit.html', employee=employee)
        except:
            db.session.rollback()
            flash('Já existe um funcionário com este nome!', 'alert alert-danger')
            return render_template('employee_edit.html', employee=employee)
    else:
        return render_template('employee_edit.html', employee=employee)


@app.route('/employee_delete/<int:employee_id>', methods=['GET'])
def employee_delete(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'GET':
        try:
            db.session.delete(employee)
            db.session.commit()
            flash('Funcionário excluído com sucesso!', 'alert alert-warning')
            
            return redirect(url_for('employees'))
        except:
            db.session.rollback()
            flash('Erro ao excluir funcionário!', 'alert alert-danger')
            return redirect(url_for('employees'))


# Fim de Employees

# Category (Categoria)
#-----------------------------------------------------------------------

@app.route('/categories', methods=['GET'])
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@app.route('/category_view/<int:category_id>', methods=['GET'])
def category_view(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'GET':
        return render_template('category_view.html', category=category)


@app.route('/category', methods=['GET', 'POST'])
def category():
    if request.method == 'POST':
        name = request.form['name']
        category = Category(name)
        try:
            db.session.add(category)
            db.session.commit()
            flash('Categoria adicionada com sucesso!', 'alert alert-success')
            return redirect(url_for('category'))
        except:
            db.session.rollback()
            flash('Já existe uma categoria com este nome!', 'alert alert-danger')
            return redirect(url_for('category'))
        
    return render_template('category.html')


@app.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        category.name = request.form['name']
        try:
            db.session.commit()
            flash('Categoria alterada com sucesso!', 'alert alert-success')
            return render_template('category_edit.html', category=category)
        except:
            db.session.rollback()
            flash('Já existe uma categoria com este nome!', 'alert alert-danger')
            return render_template('category_edit.html', category=category)
    else:
        return render_template('category_edit.html', category=category)


@app.route('/category_delete/<int:category_id>', methods=['GET', 'POST'])
def category_delete(category_id):
    catgories = Category.query.all()
    category = Category.query.get_or_404(category_id)
    if request.method == 'GET':
        try:
            db.session.delete(category)
            db.session.commit()
            flash('Categoria excluida com sucesso!', 'alert alert-warning')
            return redirect(url_for('categories'))
        except:
            flash('Erro ao alterar categoria!', 'alert alert-danger')
            return redirect(url_for('categories'))

# Fim de Caegory

# Brand (Marca)
# ----------------------------------------------------------------------

@app.route('/brands', methods=['GET'])
def brands():
    brands = Brand.query.all()
    return render_template('brands.html', brands=brands)

@app.route('/brand', methods=['GET', 'POST'])
def brand():
    if request.method == 'POST':
        name = request.form['name']
        brand = Brand(name)
        try:
            db.session.add(brand)
            db.session.commit()
            flash('Marca cadastrada com sucesso!', 'alert alert-success')
            return redirect(url_for('brand'))
        except:
            flash('Já existe uma marca cadastrada com este nome!', 'alert alert-danger')
            return redirect(url_for('brand'))
    
    return render_template('brand.html')


@app.route('/brand_view/<int:brand_id>', methods=['GET'])
def brand_view(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    if request.method == 'GET':
        return render_template('brand_view.html', brand=brand)


@app.route('/brand_edit/<int:brand_id>', methods=['GET', 'POST'])
def brand_edit(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    if request.method == 'POST':
        brand.name = request.form['name']
        try:
            db.session.commit()
            flash('Marca alterada com sucesso!', 'alert alert-success')
            return render_template('brand_edit.html', brand=brand)
        except:
            db.session.rollback()
            flash('Já existe uma marca cadastrada com este nome!', 'alert alert-danger')
            return render_template('brand_edit.html', brand=brand)
    else:
        return render_template('brand_edit.html', brand=brand)


@app.route('/brand_delete/<int:brand_id>', methods=['GET', 'POST'])
def brand_delete(brand_id):
    brands = Brand.query.all()
    brand = Brand.query.get_or_404(brand_id)
    if request.method == 'GET':
        try:
            db.session.delete(brand)
            db.session.commit()
            flash('Marca excluída com sucesso!', 'alert alert-warning')
            return redirect(url_for('brands'))
        except:
            flash('Erro ao excluir marca!', 'alert alert-danger')
            return redirect(url_for('brands'))
    
    return redirect(url_for('brands'))

# Fim de Brand

# Product (Product)
# ----------------------------------------------------------------------

@app.route('/products', methods=['GET'])
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/product_view/<int:product_id>', methods=['GET'])
def product_view(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'GET':
        return render_template('product_view.html', product=product)


@app.route('/product', methods=['GET', 'POST'])
def product():
    categories = Category.query.all()
    brands = Brand.query.all()
    if request.method == 'POST':
        code = request.form['code']
        category_id = request.form['category_id']
        brand_id = request.form['brand_id']
        name = request.form['name']
        description = request.form['description']
        cost_price = request.form['cost_price'].replace(',', '.')
        saler_price = request.form['saler_price'].replace(',', '.')
        profit = float(saler_price) - float(cost_price)
        product = Product(code, category_id, brand_id, name, description, cost_price, saler_price, profit)
        try:
            db.session.add(product)
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'alert alert-success')
            return redirect(url_for('product'))
        except:
            db.session.rollback()
            flash('Erro ao cadastrar produto!', 'alert alert-danger')
            return redirect(url_for('product'))
    
    return render_template('product.html', categories=categories, brands=brands)


@app.route('/product_edit/<int:product_id>', methods=['GET', 'POST'])
def product_edit(product_id):
    categories = Category.query.all()
    brands = Brand.query.all()
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.code = request.form['code']
        product.category_id = request.form['category_id']
        product.brand_id = request.form['brand_id']
        product.name = request.form['name']
        product.description = request.form['description']
        product.cost_price = request.form['cost_price'].replace(',', '.')
        product.saler_price = request.form['saler_price'].replace(',', '.')
        product.profit = float(product.saler_price) - float(product.cost_price) 
        try:
            db.session.commit()
            flash('Produto alterado com sucesso!', 'alert alert-success')
            products = Product.query.all()
            return render_template('product_edit.html', product=product, products=products, categories=categories, brands=brands)
        except:
            db.session.rollback()
            flash('Erro ao alterar produto!', 'alert alert-danger')
            products = Product.query.all()
            return render_template('product_edit.html', product=product, products=products, categories=categories, brands=brands)
    else:
        products = Product.query.all()
        return render_template('product_edit.html', product=product, products=products, categories=categories, brands=brands)


@app.route('/product_delete/<int:product_id>', methods=['GET', 'POST'])
def product_delete(product_id):
    categories = Category.query.all()
    brands = Brand.query.all()
    product = Product.query.get_or_404(product_id)
    if request.method == 'GET':
        try:
            db.session.delete(product)
            db.session.commit()
            flash('Produto excluido com sucesso!', 'alert alert-warning')
            return redirect(url_for('products'))
        except:
            db.session.rollback()
            flash('Erro ao alterar produto!', 'alert alert-danger')
            return redirect(url_for('products'))
    
    return redirect(url_for('products'))

# Fim de Product

# Login (Acesso)
# ----------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(pwd):
            flash('Email ou senha inválidos! Verifique se estão corretos e tente novamente.', 'alert alert-danger')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
             
    return render_template('login.html')

# Logout (Sair)
# ----------------------------------------------------------------------

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
 
# Fim de Logout

