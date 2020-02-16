from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
# add uploads file cho admin
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join

app = Flask(__name__)

app.secret_key = 'Thisissecrectkey'
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)  # SQL Achemy
admin = Admin(app, template_mode='bootstrap3')


# silly user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    join_date = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserView(ModelView):
    column_exclude_list = ['join_date']
    column_filters = ['name', 'email']
    can_export = True
    column_display_pk = True
    can_create = True
    can_delete = False
    can_edit = True
    create_modal = True  # su dung model bootstrap

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method='sha256')

    inline_models = [Comment]


class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notification.html')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def test():
    return 'Hello World!'


admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
path = join(dirname(__file__), 'uploads')
admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))
admin.add_view(NotificationsView(name='Notifications', endpoint='notify'))

if __name__ == '__main__':
    app.run()
