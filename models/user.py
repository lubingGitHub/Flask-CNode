from models import Model
from bson import ObjectId

Model = Model


class User(Model):

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('username', str, ''),
            ('password', str, ''),
            ('user_image', str, '/uploads/default.png'),
            ('signature', str, '这家伙很懒，什么东西都没有留下。'),
        ]
        return names

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form['username']
        password = form['password']
        signature = form['signature']
        if len(name) > 2 and User.one(username=name) is None:
            password = User.salted_password(password)
            u = User.new(dict(
                username=name,
                password=password,
                signature=signature,
            ))
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(
            username=form['username'],
            password=User.salted_password(form['password'])
        )
        return user

    @classmethod
    def verification_password(cls, id, old_password):
        user = User.one(
            _id = ObjectId(id),
        )
        if User.salted_password(old_password) == user.password:
            return True