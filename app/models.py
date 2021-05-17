from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app,db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique =True, nullable = False)
    profile_pic = db.Column(db.String(20), nullable = False, default = 'avatar.png')
    password = db.Column(db.String(100), nullable = False)
    admin = db.Column(db.Boolean, nullable = False, default = False)
    posts = db.relationship('Articles', backref = 'author', lazy = True)
    the_comments = db.relationship('Comments', backref='writer',lazy=True)
    post_author = db.Column(db.Boolean, nullable=False, default=False)
   

    def get_reset_token(self,expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)


    def __repr__(self):
        return str(self.username) + str(self.email) + str(self.profile_pic)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    category = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    slug = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    imgs = db.relationship('Images',backref = 'article',lazy = True)
    userscomments = db.relationship('Comments', backref = 'its_article', lazy = True)

    def __repr__(self):
        return f"Article('{self.id}','{self.title}','{self.date_posted}')"


class Images(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(20))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable = False)

    def __repr__(self):
        return f"Image('{self.id}','{self.image}')"

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable = False)

    def __repr__(self):
        return f"Comment('{self.id}','{self.comment}')"