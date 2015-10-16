# coding: utf-8

from app import db


class Content(db.Model):

    __tablename__ = "contents"
    session = db.session
    data = db.Column(db.Text())
    type_ = db.Column(db.String(80), primary_key=True)

    def __init__(self, data, type_):
        self.data = data
        self.type_ = type_

    def to_dict(self):
        return{
            "data": self.data,
            "type_": self.type_,
        }

    @classmethod
    def make_commit(cls):
        cls.session.commit()

    @classmethod
    def get_contents(cls):
        return cls.session.query(cls).all()

    @classmethod
    def get_content_by_type(cls, type_):
        return cls.session.query(cls).get(type_)

    @classmethod
    def save_content(cls, content):
        cls.session.add(content)
        cls.make_commit()

        return content.type_

    @classmethod
    def delete_content(cls, type_):
        cls.session.query(cls).filter(cls.type_ == type_).delete()
        cls.make_commit()
