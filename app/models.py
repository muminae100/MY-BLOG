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
    bio = db.Column(db.String(500))
    admin = db.Column(db.Boolean, nullable = False, default = False)
    posts = db.relationship('Articles', backref = 'author', lazy = True)
    videos = db.relationship('Videos', backref = 'vid_author', lazy = True)
    article_comments = db.relationship('Articlecomments', backref='writer',lazy=True)
    video_comments = db.relationship('Videocomments', backref='its_writer',lazy=True)
    post_author = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    city = db.Column(db.String(50))
    facebook = db.Column(db.String(50))
    twitter = db.Column(db.String(50))
    instagram = db.Column(db.String(50))
    youtube = db.Column(db.String(50))
   

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


association_table = db.Table('association_table',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    cover_img = db.Column(db.String(100), nullable = False)
    pic_desc = db.Column(db.String(100), nullable = False)
    users_comments = db.relationship('Articlecomments', backref = 'its_article', lazy = True)

    def __repr__(self):
        return f"Article('{self.id}','{self.title}','{self.date_posted}')"


class Videos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    video_url = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    video_desc = db.Column(db.String(100), nullable = False)
    userscomments = db.relationship('Videocomments', backref = 'its_video', lazy = True)

    def __repr__(self):
        return f"Videos('{self.id}','{self.title}','{self.date_posted}')"

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(200), nullable = False,unique=True)
    articles = db.relationship('Articles', backref = 'category', lazy = True)
    videos = db.relationship('Videos', backref = 'category', lazy = True)
    tags = db.relationship('Tags', backref = 'its_category', lazy = True)
    def __repr__(self):
        return f"Categories('{self.id}','{self.categoryname}')"


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(200), nullable = False, unique=True)
    articles = db.relationship("Articles", secondary=association_table, backref=db.backref('its_tags', lazy= 'dynamic'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    def __repr__(self):
        return f"Tags('{self.id}','{self.tagname}')"



class Articlecomments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date_written = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    def __repr__(self):
        return f"Comment('{self.id}','{self.comment}')"

class Videocomments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date_written = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))

    def __repr__(self):
        return f"Comment('{self.id}','{self.comment}')"

class Subscribers(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(120), unique =True, nullable = False)