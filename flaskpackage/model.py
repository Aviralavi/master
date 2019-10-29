import collections
from collections import OrderedDict

from flaskpackage import db

class DeleteTable(db.Model):
    __table_args__ = {'extend_existing': True}
    name = db.Column(db.Text, primary_key=True)
    path = db.Column(db.Text, primary_key=False)

    def __repr__(self):
        return "{}:::{}".format(self.name, self.path)

class StartTable(db.Model):
    __table_args__ = {'extend_existing': True}
    name = db.Column(db.Text, primary_key=True)
    path = db.Column(db.Text, primary_key=False)
    repeat = db.Column(db.Text, primary_key=False)

    def __repr__(self):
        return "{}:::{}:::{}".format(self.name, self.path, self.repeat)

class ExecuteTable(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, primary_key=False)
    path = db.Column(db.Text, primary_key=False)

    def __repr__(self):
        return "{}:::{}".format(self.name, self.path)

class schedule_delete(db.Model):
    __table_args__ = {'extend_existing': True}
    name = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return "{}".format(self.name)

class schedule_execute(db.Model):
    __table_args__ = {'extend_existing': True}
    name = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return "{}".format(self.name)

class schedule_start(db.Model):
    __table_args__ = {'extend_existing': True}
    name = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return "{}".format(self.name)

# db.create_all()
# storeDel = DeleteTable(name = 'amp', path = "misys")
# db.session.add(storeDel)
# db.session.commit()
# print(DeleteTable.query.all())
# print(DeleteTable.query.get('kdjfk'))
# print(DeleteTable.query.first())
# print(DeleteTable.query.filter_by(name = 'kdjfk').all())
# print(DeleteTable.query.filter_by(name = 'kdjfk').first())
# x='asdf'
# print(ExecuteTable.query.filter_by(name = x).all())