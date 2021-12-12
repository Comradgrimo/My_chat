from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Client_db(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password = Column(String)
    info = Column(String)

    def __init__(self, login, password, info):
        self.login = login
        self.password = password
        self.info = info

    def __repr__(self):
        return "<Client('%s','%s')>" % (self.login, self.info)


class Message_db(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(ForeignKey('client.id'))
    datetime = Column(DateTime)
    content = Column(String)

    def __init__(self, id_client, datetime, content):
        self.id_client = id_client
        self.datetime = datetime
        self.content = content

    def __repr__(self):
        return "<Client_history('%s', '%s', '%s')>" % (self.message, self.datetime, self.content)


class ContactList_db(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    id_master = Column(ForeignKey('client.id'))
    id_slave = Column(ForeignKey('client.id'))

    def __init__(self, id_master, id_slave):
        self.id_master = id_master
        self.id_slave = id_slave

    def __repr__(self):
        return "<Client('%s', '%s')>" % (self.id_master, self.id_slave)



base = 'sqlite3.db'
engine = create_engine(f'sqlite:///{base}', echo=True)
Base.metadata.create_all(engine)              #Создание БД
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
admin_user = Client_db("vasia", "123", "info")
session.add(admin_user)
session.commit()

q_user = session.query(Client_db).all()
print(q_user[0].login)