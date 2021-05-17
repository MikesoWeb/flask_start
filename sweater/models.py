from peewee import Model, CharField, PrimaryKeyField, SqliteDatabase


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = [User(id=1, username='Anthony', password='password'), User(id=2, username='Becca', password='secret'),
         User(id=3, username='Mike', password='12345')]

dt = SqliteDatabase('db_1.db')


class English(Model):
    id = PrimaryKeyField(primary_key=True)
    word = CharField(max_length=50, unique=True)
    translate = CharField(max_length=50, unique=True)

    class Meta:
        database = dt
        db_table = 'english'
        order_by = '-word'


English.create_table()
