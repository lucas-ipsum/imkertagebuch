from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from imkertagebuch.models import User, StockEintrag

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Passwort bestätigen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')
    # Error falls NUtzername bereits vergeben 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Benutzername bereits vergeben')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('E-Mail bereits vergeben')

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Angemeldet bleiben?')
    submit = SubmitField('Anmelden')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    picture = FileField('Profilbild aktualisieren', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Aktualisieren')

        # Error falls NUtzername bereits vergeben & ob User geändert wurde 
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Benutzername bereits vergeben')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('E-Mail bereits vergeben')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class StockEintragForm(FlaskForm):
    wabenbelegt = IntegerField('Waben Belegt?', default=0)             # , validators=[DataRequired()]
    brutw = BooleanField('brutw')
    brutei = BooleanField('brutei')
    brut_offen = BooleanField('brut_offen')
    brut_verdeckt = BooleanField('brut_verdeckt')
    sanftmut = IntegerRangeField(default=5)
    wabensitz = IntegerRangeField(default=2)
    futter = IntegerField(default=0)
    kommentar = TextAreaField()
    # Hinzugeben / Entnehmen 
    veraend_waben = IntegerField(default=0)
    veraend_mittelwand = IntegerField(default=0)
    veraend_brut = IntegerField(default=0)
    veraend_drohnenrahmen = IntegerField(default=0)
    veraend_bienen = IntegerField(default=0)
    veraend_honig_kg = IntegerField(default=0)    
    beute_id = SelectField('Beute wählen')
   # title = StringField('Title')
    submit = SubmitField('Post')

class StockKarteForm(FlaskForm):
    standmass = StringField('Standmass')
    submit = SubmitField('Speichern')

class BeuteForm(FlaskForm):
    name = StringField('Name')
    nummer = StringField('Nummer', validators=[DataRequired()])
    standort = StringField('Standort')
    date_created = DateField('Erstellt')
    date_updated = DateField('Geändert')
    submit = SubmitField('Speichern')