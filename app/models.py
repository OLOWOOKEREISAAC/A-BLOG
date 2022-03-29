from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  
from app import db,loginmanger, app
from sqlalchemy import ForeignKey
from flask_login import UserMixin


@loginmanger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content= db.Column(db.String(300), nullable = False )
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return f"task('{self.content}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String(30), unique = True, index = True) 
    users = db.relationship('User', backref= 'role')

    def __repr__(self):
        return f"Role('{self.role}')"


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), index = True)
    location = db.Column(db.String(60), index = True)
    About_me = db.Column(db.Text())
    profilepic = db.Column(db.String(), default= 'default.jpg')
    email = db.Column(db.String(70), unique = True, index = True)
    password = db.Column(db.String(10), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref = 'user', lazy = True)

    def generate_Rtoken(self, expires_sec= 2000):
        s = Serializer(app.config['SECRET_KEY'], expires_sec )
        return s.dumps({'user_id' : 'self.email' }).decode('utf-8')
        
    @staticmethod
    def verify_Rtoken(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Role('{self.id}','{self.name}','{self.email}')"

    @staticmethod 
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError        
        from random import seed        
        import forgery_py
        seed()        
        for i in range(count): 
            u = User(email=forgery_py.internet.email_address(),
                    password=forgery_py.lorem_ipsum.word(),
                    name=forgery_py.name.full_name(),
                    location=forgery_py.address.city(),
                    About_me=forgery_py.lorem_ipsum.sentence())
            db.session.add(u)
            try:
                db.session.commit() 
            except IntegrityError:
                db.session.rollback()



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index = True, nullable = False)
    content = db.Column(db.Text(60), index = True, nullable = False)
    posted = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.posted}')"

    @staticmethod    
    def generate_fake(count=50):        
        from random import seed, randint        
        import forgery_py
        seed()        
        user_count = User.query.count()        
        for i in range(count):            
            u = User.query.offset(randint(0, user_count - 1)).first()            
            p = Post(title=forgery_py.lorem_ipsum.word(), content=forgery_py.lorem_ipsum.sentences(randint(1, 3)), user=u)            
            db.session.add(p)            
            db.session.commit()
   