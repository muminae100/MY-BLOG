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
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    images = db.relationship('Images',backref = 'article',lazy = True)
    userscomments = db.relationship('Comments', backref = 'its_article', lazy = True)

    def __repr__(self):
        return f"Article('{self.id}','{self.title}','{self.date_posted}')"

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(200), nullable = False)
    articles = db.relationship('Articles', backref = 'category', lazy = True)

    def __repr__(self):
        return f"Categories('{self.id}','{self.category}')"

class Images(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    imagename = db.Column(db.String(100), nullable = False)
    imagedescription= db.Column(db.String(200), nullable = False)
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

class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    city = db.Column(db.String(50))
    
    def __repr__(self):
        return f"Comment('{self.id}','{self.company_name}','{self.address}','{self.phone_number}','{self.city}')"

class SocialMediaAccounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook = db.Column(db.String(50))
    twitter = db.Column(db.String(50))
    instagram = db.Column(db.String(50))
    youtube = db.Column(db.String(50))
    
    def __repr__(self):
        return f"Comment('{self.id}','{self.facebook}','{self.twitter}','{self.instagram}','{self.youtube}')"
