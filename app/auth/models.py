from app import db


class Users(db.Model):
    """
    User database model
    """

    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    pwd = db.Column(db.String(64))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd

    def __repr__(self):
        return "<User: Username - {}; password - {};>".format(self.username, self.pwd)


class InvalidToken(db.Model):

    __tablename__ = "invalid_tokens"
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_invalid(cls, jti):
        """ Determine whether the jti key is on the blocklist return bool"""
        q = cls.query.filter_by(jti=jti).first()
        return bool(q)
    
