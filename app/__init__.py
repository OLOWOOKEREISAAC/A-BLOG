from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.configurations import config




app=Flask(__name__)
app.config.from_object(config)
Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
loginmanger = LoginManager(app)
loginmanger.login_view = 'users.login'
mail=Mail(app)



from app.users.views import users
from app.posts.views import posts
from app.main.views import main
from app.Errors.views import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)

