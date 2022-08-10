import ormar
import databases
import sqlalchemy

database = databases.Database("postgresql://weather_app:weather_app@localhost:5433/weather_app")
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=64, unique=True)
    hashed_password: str = ormar.String(max_length=255)
