from json import dump, dumps, load, loads
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import matplotlib.pyplot as plt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email is not registered', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    fig= plt.figure()
    fig.savefig('website/static/graph_plot.jpg')
    flash("Logged out succesfully")
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        phone = request.form.get("phone")
        city = request.form.get("city")
        pass1 = request.form.get("password")
        pass2 = request.form.get("confirmPass")
        company = request.form.get("company")
        company = True if company == "" else False
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email is already in use", category='error')
        elif len(firstName) < 1:
            flash("Name field is required", category='error')
        elif len(pass1) <= 7:
            flash("Password is too short", category='error')
        elif pass1 != pass2:
            flash("Passwords do not match", category='error')
        else:
            new_user = User(email=email, firstName=firstName, lastName=lastName, phone=phone, city=city, company=company, password=generate_password_hash(pass1, method='sha256'))

            with open('website/users.json', 'r') as file:
                data = file.read()
            users = loads(data) if data else {}
            id = len(users.keys()) if data else 0
            users[id] = {"id": id,
                         "firstName": firstName,
                         "lastName": lastName,
                         "email": email,
                         "phone": phone,
                         "city": city,
                         "company": company
                         }
            with open('website/users.json', 'w') as file:
                dump(users, file)

            with open('website/graph.json', 'r') as file:
                data = file.read()
            if data:
                graph = loads(data)
                graph.append([])
            else:
                graph = [[]]
            with open('website/graph.json', 'w') as file:
                dump(graph, file)

            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)

# from flask import Blueprint, render_template, request, flash, redirect, url_for
# from .models import User
# from werkzeug.security import generate_password_hash, check_password_hash
# import json
# from flask_login import login_user, login_required, logout_user, current_user

# auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['POST', 'GET'])
# def login():

#     if request.method == "POST":
#         log = True
#         email = request.form.get('email')
#         password = request.form.get('password')
    
#         with open('website/users.json', 'r') as file:
#             data = file.read()
#         users = json.loads(data)
#         for key in users:
#             if users[key]['email'] == email:
#                 user = key
#                 break
#         else:
#             flash("Email is not registered", category='error')
#             log = False

#         if log:
#             if check_password_hash(users[user]['password'], password):
#                 flash('Logged in succesfully', category='success')
#                 login_user(users[user], remember=True)
#                 return redirect(url_for('views.home'))
#             else:
#                 flash('Password is not correct', category='error')
    

#     return render_template("login.html")

# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))

# @auth.route('/signup', methods=['POST', 'GET'])
# def signup():
#     formData = request.form

#     email = request.form.get("email")
#     name = request.form.get("name")
#     pass1 = request.form.get("password1")
#     pass2 = request.form.get("password2")

#     if formData:
#         if len(name) < 2:
#             flash("Name is too short", category='error')
#         if len(pass1) <= 7:
#             flash("Password is too short", category='error')
#         elif pass1 != pass2:
#             flash("Passwords do not match", category='error')
#         else:
#             with open('website/users.json', 'r') as file:
#                 data = file.read()
#             users = json.loads(data) if data else {}
#             id = len(users) if users else 0
#             for user in users:
#                 if users[user]['email'] == email:
#                     flash("Email already in use", category='error')
#                     break
#             else:
#                 new_user = User(id=id, email=email, name=name, password=generate_password_hash(pass1, method='sha256'))
#                 users[id] = vars(new_user)
#                 with open('website/users.json', 'w') as file:
#                     json.dump(users, file)

#                 flash("Account created succesfully", category='success')


#     return render_template("signup.html")

