
from exts import db
from datetime import datetime
class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bannerName = db.Column(db.String(20),nullable=False)
    imglink = db.Column(db.String(200),nullable=False,unique=True)
    link = db.Column(db.String(200),nullable=False,unique=True)
    priority = db.Column(db.Integer,default=1)


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    boardname = db.Column(db.String(20),nullable=False)
    postnum = db.Column(db.String(200),nullable=False,default=0)
    create_time =db.Column(db.DateTime,default=datetime.now)