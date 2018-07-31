from flask import (Flask,
                   render_template,
                   request, abort,
                   redirect)

from flask_moment import Moment
from datetime import datetime
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, roles_required
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin .contrib.sqla import ModelView


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT']= 'jiwon'
app.config['SECURITY_PASSWORD_HASH']= 'sha512_crypt'
app.config['SECURITY_REGISTERABLE']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECURITY_SEND_REGISTER_EMAIL']= False

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class MyModelView(ModelView):
    pass

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

moment= Moment(app)
admin= Admin(app)
user_datastore= SQLAlchemyUserDatastore(db, User,Role)
security= Security(app, user_datastore)


admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))


@app.route('/')
@login_required
def index():
    dt= datetime.utcnow()
    return render_template('index.html', dt= dt)


@app.route('/<path>')
def path():
    if path:
        return render_template('%.html' %path)

if __name__ == '__main__':
    app.run(debug= True)
