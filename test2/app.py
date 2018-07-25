from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   )
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = True
app.config['SECRET_KEY'] = 'jiwon'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/add')
def add():
    user = User()
    user.email = 'jiwon@gamil.com'
    user.username = "jiwon"
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')

@app.route('/insert')
def insert():
    ue = request.args.get('ue')
    uu = request.args.get('uu')
    user = User()
    user.email = ue
    user.username = uu
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')

@app.route('/')
def  index():
    a = [1, 2, 3, 4, 5, 6, 7, 8]
    b = 'abcdewfk'
    #c = list(zip(a, b))
   # d = dict({'a': 1, 'b': 2, 'c': 3})
    users = User.query.all()
    print(users)
    return render_template("index.html", won=users)name


@app.route('/<name>')
def list(name):
    if name:
        return render_template("{}.html".format(name))
    else:
        return render_template("index.html")


@app.route('/search', methods =['POST'])
def search():
    search_term = request.form['test1']
    if search_term == 'test111':
        print(search_term)
        return render_template('index.html')
    return redirect('/search')

if __name__ == '__main__':
    app.run(debug= True)
