from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

# Formulario de Registro de Usuario
class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(), Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya existe.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese email ya está registrado.')

# Formulario de Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired()
    ])
    submit = SubmitField('Iniciar Sesión')

# Formulario de CRUD de Tareas
class TaskForm(FlaskForm):
    title = StringField('Título', validators=[
        DataRequired(), Length(min=3, max=200)
    ])
    description = TextAreaField('Descripción', validators=[])
    priority = SelectField('Prioridad', choices=[
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta')
    ])
    status = SelectField('Estado', choices=[
        ('pendiente', 'Pendiente'),
        ('en progreso', 'En Progreso'),
        ('hecho', 'Hecho')
    ])
    due_date = DateField('Fecha límite', validators=[], format='%Y-%m-%d', render_kw={"type": "date"})
    submit = SubmitField('Guardar Tarea')