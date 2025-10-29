from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

import os
from werkzeug.utils import secure_filename

from estudo import db, bcrypt, app
from estudo.models import Contato, User, Post, PostComentarios

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('sobrenome', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validade_email(self, email):
        if User.query.filter(email=email.data).first():
            return ValidationError('Usúario ja cadastrado com esse E-mail !!!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))    
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha
        )

        db.session.add(user)
        db.session.commit()
        return user
    

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        #recuperar o usuario do email
        user = User.query.filter_by(email=self.email.data).first()

        #verificar se a senha é valida
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                #login user
                return user
            else:
                raise Exception('Senha está incorreta!!!')
        else:
            raise Exception('Usúario não encontrado!!!')
    

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )

        db.session.add(contato)
        db.session.commit()


class PostForm(FlaskForm):
        mensagem = StringField('Mensagem', validators=[DataRequired()])
        imagem = FileField('imagem', validators=[DataRequired()])
        btnSubmit = SubmitField('enviar')

        def save(self, user_id):
            imagem = self.imagem.data
            nome_seguro = secure_filename(imagem.filename)

            post = Post (
                mensagem = self.mensagem.data,
                user_id = user_id,
                imagem = nome_seguro
            )

            caminho = os.path.join(
                 os.path.abspath(os.path.dirname(__file__)), #pegar a pasta que está no nosso projeto 
                 app.config['UPLOAD_FILES'], #definir a pasta que configuramos para UPLOAD
                 'post', #a pasta que está os POST 
                 nome_seguro #defino nome seguro pra ela e 
            )
            

            imagem.save(caminho) #salvo 
            db.session.add(post)
            db.session.commit()


class PostComentarioForm(FlaskForm):
        comentario = StringField('Comentario', validators=[DataRequired()])
        btnSubmit = SubmitField('enviar')

        def save(self, user_id, post_id):
            comentario = PostComentarios (
                comentario = self.comentario.data,
                user_id=user_id,
                post_id = post_id
            )

            db.session.add(comentario)
            db.session.commit()
