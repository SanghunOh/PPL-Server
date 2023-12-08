from .. import db, flask_bcrypt

class User(db.Model):
    """ User Model for storing user related details """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))

    interests = db.relationship('Interest', backref='user', lazy=True)
    papers = db.relationship('Paper', backref='user', lazy=True)

    
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 
    
    @property
    def password(self):
        raise AttributeError('password: write-only field')
    
    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token(self, user):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10),
                'iat': datetime.datetime.utcnow(),
                'email': user.email,
            }
            return jwt.encode(
                payload,
                key,
                algorithm
            )
        except Exception as e:
            return str(e)


    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            temp = jwt.decode(auth_token,key,algorithm)
            return temp
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.name
        }

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abstract = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'abstract': self.abstract,
            'author': self.author,
            'category': self.category,
            'link': self.link,
            'title': self.title,
            'user_id': self.user_id,
            'year': self.year
        }
