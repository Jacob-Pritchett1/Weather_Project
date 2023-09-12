# burgers.py
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.weather import main as get_weather
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/', methods =['GET', 'POST'])
def home():
    data = None
    user_logged_in = 'user_id' in session
    every_post = Post.post_users()
    if request.method == 'POST':
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        data = get_weather(city,state,country)
    return render_template('index.html', data=data, user_logged_in=user_logged_in, every_post=every_post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = { 'email' : request.form['email']}
        user_in_db = User.get_email(data)
        if not user_in_db:
            flash("Invalid Email/Password. Please try again.")
        elif not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Email/Password. Please try again.")
        else:
            session['user_id'] = user_in_db.id
            session['first_name'] = user_in_db.first_name
            return redirect('/')
    return render_template('login.html')

@app.route('/registration')
def register():
    return render_template('registration.html')

@app.route('/registration/process', methods=['POST'])
def registered():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
        "confirm_password": request.form["confirm_password"]
    }
    User.save(data)
    return redirect("/")

@app.route("/new/post/create", methods=['POST'])
def create_post():
    if not Post.validate_post(request.form):
        return redirect('/')
    if "user_id" not in session:
        return redirect(url_for('login'))
    session["text"] = request.form["text"]
    data = {
        "text": request.form["text"],
        "user_id": session["user_id"]
    }
    Post.create_post(data)
    return redirect("/")

@app.route('/edit/<int:id>')
def edit_post(id):
    if "user_id" not in session:
        return redirect('/')
    single_post=Post.get_one(id)
    return render_template("edit_post.html", single_post= single_post,id=id)

@app.route('/edit/<int:id>/finalize', methods=["POST"])
def finalize_edit(id):
    if not Post.validate_post(request.form):
        return redirect('/edit/<int:id>')
    data = {
        "text": request.form["text"],
        "id": id
    }
    Post.edit_post(data)
    return redirect('/')

@app.route('/post/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        return redirect(url_for('login'))
    Post.delete(id)
    return redirect('/')


@app.route('/logout')
def logging_out():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

