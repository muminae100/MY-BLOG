import timeago,datetime
import os
import secrets
from PIL import Image
from flask import render_template,redirect,request,url_for,flash,abort,jsonify
from app import app,db,bcrypt,mail
from app.models import Users,Articles,Images,Comments,ContactInfo,SocialMediaAccounts,Categories
from flask_login import login_user,current_user,logout_user,login_required
from app.forms import (RegistrationForm,LoginForm,UpdateAccountForm,
PostForm,RequestResetForm,ResetPasswordForm,ContactForm,CommentsForm,SendNotificationsForm,ContactInfoForm,
SocialMediaAccountsForm)
from flask_mail import Message



@app.route('/contacts_info')
@login_required
def contact_info():
    contacts = ContactInfo.query.all()
    form = ContactInfoForm()
    if form.validate_on_submit():
        company_name = form.company.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        city = form.city.data

        contacts = ContactInfo.query.first()
        contacts.company_name = company_name
        contacts.address = address
        contacts.phone = phone
        contacts.email = email
        contacts.city = city
        db.session.commit()

    return render_template('admin/contacts_info.html',form=form,title='Contact information')

@app.route('/social_media_accounts')
@login_required
def social_media_accounts():
    accounts = SocialMediaAccounts.query.all()
    form = SocialMediaAccountsForm()
    if form.validate_on_submit():
        facebook = form.facebook.data
        instagram = form.instagram.data
        twitter = form.twitter.data
        youtube = form.youtube.data
        

        contacts = ContactInfo.query.first()
        contacts.facebook = facebook
        contacts.instagarm = instagram
        contacts.twitter = twitter
        contacts.youtube = youtube
        db.session.commit()

    return render_template('admin/social_media_accounts.html',form=form,title='Social media accounts')


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    articles = Articles.query.order_by(Articles.date_posted.desc()).paginate(per_page=10, page=page)
    return render_template('index.html',articles = articles)

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('You have been successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Email or password incorrect!','danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        newuser = Users(email=form.email.data,username=form.username.data,password=hashed_password)
        db.session.add(newuser)
        db.session.commit()

        flash('Registered successfully! Login to access your account', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/imgs/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

@app.route('/img_upload', methods=['POST'])
@login_required
def img_uploader():
    img = request.files.get('file')
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/imgs/post_imgs', picture_fn)

    output_size = (250, 250)
    i = Image.open(img)
    i.thumbnail(output_size)

    i.save(picture_path)
    pic_location = url_for('static', filename = 'imgs/post_imgs/' + picture_fn)
    return jsonify({'location': pic_location})

@app.route('/account', methods = ['GET','POST'])
@login_required
def account():
    if current_user.admin == True:
        return redirect(url_for('admin_account'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'imgs/profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title = current_user.username, profile_pic = image_file, form = form)

def send_email_to_admin(email,message):
    msg = Message(f'Email from {email}', 
                   sender=email,
                   recipients=['smuminaetx100@gmail.com'])
    msg.body = f'''
Hi admin WORLDNEWS!
{message}
'''
    mail.send(msg)


@app.route('/contact', methods = ['GET','POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data
        send_email_to_admin(email,message)
        flash('Your email has been sent!','info')
    return render_template('contact.html',title='Contact us', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))








# posts
@app.route('/newpost', methods = ['GET', 'POST'])
@login_required
def new_post():
    # form =PostForm()
    # choices = [(category.id, category.category) for category in Categories.query.all()]
    # if form.validate_on_submit():
    #     article = Articles(title=form.title.data,category_id=form.category.data,
    #     content=form.content.data,author=current_user)
    #     db.session.add(article)
    #     db.session.commit()
    #     flash('Your have successfully posted a new article!', 'success')
    #     return redirect(url_for('post',id=article.id))
    return render_template('new_posts.html', title = 'New post')

@app.route('/post/<int:id>', methods = ['GET', 'POST'])
def post(id):
    article = Articles.query.get_or_404(id)
    for i in article.images:
        img=i.imagename
        imgdesc=i.imagedescription
    image = url_for('static', filename = 'imgs/post_imgs/' + img)
    posts = Articles.query.order_by(Articles.date_posted.desc()).all()
    comments = article.userscomments
    now = datetime.datetime.now() 
    time_posted = timeago.format(article.date_posted, now)
    form = CommentsForm()
    if form.validate_on_submit():
        comment = Comments(comment=form.comments.data,user_id=current_user.id,article_id=article.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your have successfully added your comment!', 'success')
        return redirect(url_for('post',id = id))
    return render_template('post.html', title=article.title, article = article,
    form=form,posts=posts,comments=comments,time_posted=time_posted,image=image,imgdesc=imgdesc)

@app.route('/post/<int:id>/update', methods = ['GET', 'POST'])
@login_required
def updatepost(id):
    article = Articles.query.get_or_404(id)
    if article.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.category = form.category.data
        article.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post',id = article.id))
    elif request.method == 'GET':
        form.title.data = article.title
        form.category.data = article.category
        form.content.data = article.content
    return render_template('new_posts.html', title = 'Update post', form = form, legend = 'Update post')


@app.route('/post/<int:id>/delete', methods = ['POST'])
@login_required
def deletepost(id):
    article = Articles.query.get_or_404(id)
    if current_user.admin != True:
        if article.author != current_user:
            abort(403)

    db.session.delete(article)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/author/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    articles = Articles.query.filter_by(author=user)\
        .order_by(Articles.date_posted.desc())\
        .paginate(per_page=20, page=page)
    return render_template('author_posts.html',articles = articles, user=user)


@app.route('/category/<string:category>')
def categories(category):
    page = request.args.get('page', 1, type=int)
    articles = Articles.query.filter_by(category=category)\
        .order_by(Articles.date_posted.desc())\
        .paginate(per_page=20, page=page)
    return render_template('pages/categories.html',articles = articles,heading=category)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                   sender='smuminaetx100@gmail.com',
                   recipients=[user.email])
    msg.body = f'''To reset your password, click the link below:
{url_for('reset_token',token=token,_external = True)}
Token expires within one hour!
If you did not make this request simply ignore this email and no changes will be made.
'''
    mail.send(msg)





@app.route('/reset_password', methods = ['GET','POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@app.route('/reset_password/<token>', methods = ['GET','POST'])
def reset_token(token):
    user = Users.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login and access your account', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)






@app.route('/search')
def search():
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    articles = Articles.query.whoosh_search(query).order_by(Articles
    .date_posted.desc()).paginate(per_page=10, page=page)()
    return render_template('index.html', articles = articles)
@app.route('/admin')
@login_required
def admin():
    if current_user.admin != True:
        abort(403)
    users = Users.query.paginate()
    articles = Articles.query.paginate()
    comments = Comments.query.paginate()
    image_file = url_for('static', filename = 'imgs/profile_pics/' + current_user.profile_pic)
    return render_template('admin/home.html',users=users,articles=articles,comments=comments,image_file=image_file)

@app.route('/adminaccount', methods = ['GET','POST'])
def admin_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'imgs/profile_pics/' + current_user.profile_pic)
    return render_template('admin/admin_account.html', title = current_user.username, profile_pic = image_file, form = form)

@app.route('/all_comments')
@login_required
def comments():
    comments = Comments.query.all()
    return render_template('admin/comments.html', comments = comments)


@app.route('/delete_comment/<int:commentid>')
@login_required
def delete_comment(commentid):
    message = 'Your comment was deleted because of:'
    comment = Comments.query.get_or_404(str(commentid))
    user = comment.writer
    db.session.delete(comment)
    db.session.commit()
    flash('The comment has been deleted!', 'success')
    send_user_email(user,message)
    return redirect(url_for('comments'))

@app.route('/post/<articleid>/comment/<int:commentid>/update', methods = ['GET', 'POST'])
@login_required
def updatecomment(commentid,articleid):
    article = Articles.query.get_or_404(str(articleid))
    comment = Comments.query.get_or_404(str(commentid))
    if comment.writer != current_user:
        abort(403)

    form = CommentsForm()
    if form.validate_on_submit():
        comment.comment = form.comments.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('post',id = article.id))
    elif request.method == 'GET':
        form.comments.data = comment.comment
    return render_template('post.html', title = 'Update comment', form = form,article=article)

@app.route('/post/<int:articleid>/comment/<int:commentid>/delete')
@login_required
def deletecomment(articleid,commentid):
    articleid = Articles.query.get_or_404(str(articleid))
    comment = Comments.query.get_or_404(str(commentid))
    if comment.writer != current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('post',id=articleid))


@app.route('/all_users')
@login_required
def all_users():
    users = Users.query.paginate()
    for user in users.items:
        image_file = url_for('static',filename='imgs/profile_pics/' + user.profile_pic)
    return render_template('admin/users.html', users = users, image_file=image_file,title='All users')

@app.route('/all_posts')
@login_required
def all_posts():
    posts = Articles.query.paginate()
    return render_template('admin/all_posts.html', posts = posts)

def send_user_email(user,message):
    msg = Message('Email from admin of Blog', 
                   sender= 'smuminaetx100@gmail.com',
                   recipients=[user.email])
    msg.body = f'''
{message}
'''
    mail.send(msg)


@app.route('/send_user_email/<int:id>/<string:message>')
@login_required
def send_user_email(id,message):
    user = Users.query.get_or_404(str(id))
    message = message
    if user:
        send_user_email(user,message)
    flash('User does not exist!')
    return render_template('admin/users.html')

@app.route('/all_admins')
@login_required
def all_admins():
    admins = Users.query.filter_by(admin=True).paginate()
    for admin in admins.items:
        image_file = url_for('static', filename = 'imgs/profile_pics/' + admin.profile_pic)
    return render_template('admin/all_admins.html', admins = admins, image_file = image_file, title='Site admins')

@app.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')

@app.route('/notifications', methods=['GET','POST'])
@login_required
def notifications():
    form = SendNotificationsForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_user_email(user,form.notification.data)
        flash('Notification sent successfully','success')
    return render_template('admin/notifications.html',form=form)


@app.route('/terms_and_conditions')
def terms_conditions():
    return render_template('Terms_and_conditions.html', title='Terms and conditions')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy policy')


@app.route('/magazine')
def magazine():
    return render_template('pages/categories.html', heading='Magazine')

@app.route('/business')
def business():
    return render_template('pages/categories.html', heading='Business')

@app.route('/sports')
def sports():
    return render_template('pages/categories.html', heading='Sports')

@app.route('/art')
def art():
    return render_template('pages/categories.html', heading='Art')

@app.route('/politics')
def politics():
    return render_template('pages/categories.html', heading='Politics')

@app.route('/travel')
def travel():
    return render_template('pages/categories.html', heading='Travel')

@app.route('/about')
def about():
    return render_template('pages/aboutus.html')

