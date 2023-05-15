from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.text}"

    def show_type(self):
        return 'Our type Article'


with app.app_context():
    db.create_all()


# app2 = Flask(__name__)
# app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project2.db'
# db2 = SQLAlchemy(app2)


# class User(db2.Model):
#     id = db2.Column(db2.Integer, primary_key=True)
#     name = db2.Column(db2.String, unique=True, nullable=False)
#     email = db2.Column(db2.String(100), nullable=False)
#     password = db2.Column(db2.Text, nullable=False)
#     date = db2.Column(db2.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"{self.email}"

#     def show_type(self):
#         return 'Our type User'


# with app2.app_context():
#     db2.create_all()


# @app2.route('/')
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        username = request.form['username']
        title = request.form['title']
        text = request.form['text']

        article = Article(username=username, title=title, text=text)
        # print(article.show_type())
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return render_template("500.html")

    else:
        return render_template("create-article.html")


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == "POST":
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']

#         article = User(name=name, email=email, password=password)
#         try:
#             db2.session.add(article)
#             db2.session.commit()
#             return redirect('/')
#         except:
#             return render_template("500.html")

#     else:
#         return render_template("login.html")


@app.route('/posts')
def posts():
    article = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=article)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    print(article)
    return render_template('posts_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return render_template("500.html")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.username = request.form.get('username')
        article.title = request.form.get('title')
        article.text = request.form.get('text')

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return render_template("500.html")
    else:
        return render_template('post_edit.html', article=article)


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f"User page {name} - id {id}"


if __name__ == '__main__':
    app.run(debug=True)