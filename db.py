from typing import Optional, List
import ormar
import databases
import sqlalchemy

database = databases.Database("postgresql://chatProject:chatProject@localhost:5433/chatProject")
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"
    
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64)
    email: str = ormar.String(max_length=64, unique=True)
    hashed_password: str = ormar.String(max_length=255)


class Chat(ormar.Model):
    class Meta(BaseMeta):
        tablename = "chats"

    id: int = ormar.Integer(primary_key = True)
    users: Optional[List[User]] = ormar.ManyToMany(User)


class Message(ormar.Model):
    class Meta(BaseMeta):
        tablename = "messages"

    id: int = ormar.Integer(primary_key = True)
    chat: Optional[Chat] = ormar.ForeignKey(Chat)
    text: str = ormar.String(max_length=255)
    user: User = ormar.ForeignKey(User)
