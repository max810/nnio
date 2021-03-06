from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy_utils.types.password import PasswordType
from sqlalchemy_utils import force_auto_coercion

force_auto_coercion()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
        ],
    ))


class LayerSchema(Base):
    __tablename__ = 'layers_schemas'

    layer_type = Column(String, primary_key=True, index=True)
    layer_schema = Column(String)


class Architecture(Base):
    __tablename__ = 'architectures'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)
