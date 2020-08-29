from datetime import datetime
from couponworld import db, login_manager, admin
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.companyname}', '{self.email}')"


class UserView(ModelView):
    form_columns = ['id', 'companyname', 'email', 'posts']


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    couponcode = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.couponcode}', '{self.date_posted}')"


class PostView(ModelView):
    form_columns = ['title', 'content', 'couponcode', 'date_posted', 'user_id']


admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
