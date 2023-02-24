import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from imkertagebuch import app, db, bcrypt
from imkertagebuch.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, StockEintragForm, StockKarteForm, BeuteForm
from imkertagebuch.models import StockKarte, User, Post, StockEintrag, Beute
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")     # zwei Routes werden von einer Funktion verwaltet
def home():
    #posts= Post.query.all()
    stocks = StockEintrag.query.all()
    beuten = Beute.query.all()
    latest_stockeintraege = []
    for beute in beuten: 
        latest_stockeintrag = StockEintrag.query.filter(StockEintrag.beute_id == beute.id).order_by(StockEintrag.date_posted.desc()).first()
        latest_stockeintraege.append(latest_stockeintrag)
        print(latest_stockeintrag)
    return render_template('home.html', latest_stockeintraege=latest_stockeintraege, stocks=stocks, beuten=beuten )      # Struktur der Website wird von Template geladen , stocks=stocks

def get_latest_stockeintrag(beute):
    latest_stockeintrag = StockEintrag.query.filter(StockEintrag.beute_id == beute.id).order_by(StockEintrag.date_posted.desc()).first()
    smth = 1
    return smth

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account erstellt für {form.username.data}! Sie können sich jetzt anmelden', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrieren', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Anmeldung fehlgeschlagen. Bitte E-Mail und Passwort überprüfen', 'danger')
    return render_template('login.html', title='Anmelden', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)      # _ VAriable wird nicht benötigt
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

    output_size = (500, 500 )           # resizing, damit keine besonders großen Bilder gespeichert werden. Format wird so aber festgelegt 
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account erfolgreich aktualisiert!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Eintrag von Post in DB 
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        print('Neuer Post: ')
        print(post)
        print(post.content)
        print(post.date_posted)
        db.session.add(post)
        db.session.commit()
        flash('Post wurd erfolgreich erzeugt', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend = 'Create Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)   # Schaut ob id vorhanden. Ansonsten Return 404 
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)                          # 403 forbidden route 
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()                 # add nicht nötig da update und somit bereits in db 
        flash('Aktualisiert!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':           # bei GET werden die aktuellen Inhalte im Textfenster angezeigt und können dann aktualisiert werden
        form.title.data = post.title 
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend = 'Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit() 
    flash('Dein Post wurde erfolgreich gelöscht', 'success')
    return redirect(url_for('home')) 

    veraend_waben = db.Column(db.Integer)
    veraend_mittelwand = db.Column(db.Integer)
    veraend_brut = db.Column(db.Integer)
    veraend_drohnenrahmen = db.Column(db.Integer)
    veraend_bienen = db.Column(db.Integer)
    veraend_honig_kg = db.Column(db.Integer)
    einfutter_text = db.Column(db.String(150))
    kommentar = db.Column(db.String(150))

@app.route("/stock-eintrag/add/<int:beute>", methods=['GET', 'POST'])
@login_required
def new_stock_eintrag(beute):
    print('hey')
    print(beute)
    beuten = Beute.query.all()
    form = StockEintragForm()
    form.beute_id.choices = [(beute.id, beute.name) for beute in beuten]            # name beute als Auswahloption für select id als Wert 
    form.beute_id.default = beute
    form.process()
    karte_beute = StockKarte.query.filter_by(beute_id=form.beute_id.data)
    print(form.wabensitz.default)
    wabensitz_liste = ['Links', 'Mitte-Links','Mitte', 'Mitte-Rechts', 'Rechts']
    if  form.validate_on_submit():
        # Eintrag von Post in DB 
        wabensitz = form.wabensitz.data
        print(wabensitz)
        wabensitz = wabensitz_liste[form.wabensitz.data]
        print(wabensitz)
        data = StockEintrag(wabenbelegt=form.wabenbelegt.data, beute_id=form.beute_id.data, kommentar=form.kommentar.data, veraend_honig_kg=form.veraend_honig_kg.data, veraend_bienen=form.veraend_bienen.data, veraend_drohnenrahmen=form.veraend_drohnenrahmen.data, veraend_brut=form.veraend_brut.data, veraend_mittelwand=form.veraend_mittelwand.data, veraend_waben=form.veraend_waben.data, stockkarten_id=karte_beute.first().id, autor=current_user, brutw=form.brutw.data, brutei=form.brutei.data, brut_offen=form.brut_offen.data, brut_verdeckt=form.brut_verdeckt.data, sanftmut=form.sanftmut.data, wabensitz=wabensitz) # , 
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)                                                  # session refresh -> damit aktuelle ID ausgelsen werden kann (wird zu data hinzugefügt)
        flash('Stock-Karten Eintrag wurd erfolgreich erzeugt', 'success')
        return redirect(url_for('show_stockeintrag', stock_id=data.id))      
    else: 
        print('Form not validated')
    return render_template('stock_eintrag.html', form=form, beuten=beuten)


@app.route("/stock-karte/add", methods=['GET', 'POST'])                          # TODO prüfen ob GET entfernt werden kann 
@login_required
def new_stock_karte():
    form = StockKarteForm()
    data = StockKarte(standmass='hdsfkhsd') 
    db.session.add(data)
    print(data)

@app.route("/stockeintrag/<int:stock_id>", methods=['GET'])
def show_stockeintrag(stock_id):
    print(stock_id)
    stock_eintrag = StockEintrag.query.get_or_404(stock_id)
    #print(stock_eintrag.karte.id)
    return render_template('stockeintrag_detail_page.html', stock_eintrag=stock_eintrag)

@app.route("/stockeintrag/byBeute/<int:karte_id>", methods=['GET'])
def get_stockeintraege_byBeute(karte_id):
    stock_eintraege = StockEintrag.query.filter_by(stockkarten_id=karte_id)
    beute = stock_eintraege.first().karte.beute     # Name Beute für angezeigte StockKartenEinträge
    print('huu')
    print(beute)
    return render_template('all_stockeintraege.html', stock_eintraege=stock_eintraege, beute=beute)


@app.route("/beuten", methods=['GET'])
def get_beuten():
    beuten = Beute.query.all()
    print(beuten)
    return render_template('beuten.html', beuten=beuten)


@app.route("/beute/get/<int:beute_id>")
@login_required
def get_beute_byID(beute_id):
    form = BeuteForm()
    beute = Beute.query.get_or_404(beute_id)
    print(beute.stockkarte_id[0].id)
    print('hee')
    print(type(beute.stockkarte_id[0]))
    return render_template('beute_details.html', form=form, beute=beute, readonly=True)

@app.route("/beute/update/<int:beute_id>", methods=['GET', 'POST'])
@login_required
def update_beute(beute_id):
    beute = Beute.query.get_or_404(beute_id)
    form = BeuteForm()
    if form.validate_on_submit():
            for key, value in form.data.items():
                if value:                                               # prüfen ob Wert im Formular eingegeben wurde 
                    setattr(beute, key, value)
                else:                                                   # Werte aus DB überehmen, für unervänderte Einträge 
                    tmp = getattr(beute, key)
                    setattr(beute, key, tmp)
            db.session.commit()      
            return redirect(url_for('get_beute_byID',beute_id=beute.id, beute=beute, readonly=True))
    return render_template('beute_details.html', form=form, beute=beute, readonly=False)

@app.route("/beuten/add", methods=['GET','POST'])
@login_required
def add_beute():
    form = BeuteForm()
    standort = 'HTW Berlin'                                             # TODO entfernen wenn mehr Standorte als HTW möglich
    lat = '52.45457431051643'
    long = '13.526353757277207'
    if  form.validate_on_submit():
        data = Beute(name=form.name.data, nummer=form.nummer.data, standort=standort, lat=lat, long=long)
        db.session.add(data)
        db.session.commit()
        # TODO return template beute_details.html
    print(form.name.data)
    return render_template('add_beute.html', form=form)