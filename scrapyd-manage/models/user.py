# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 10:10
# @Author  : 10867
# @FileName: user.py
# @Software: PyCharm
import hashlib

from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TINYINT
from sqlalchemy.orm import relationship

from models import Base


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(150), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(INTEGER(11), primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)

    def verify_password(self, password: str) -> bool:
        pwd = hashlib.md5(password.encode('utf-8')).hexdigest()

        if pwd == self.password:
            return True
        else:
            return False


class AuthPermission(Base):
    __tablename__ = 'auth_permission'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    codename = Column(String(100), nullable=False)


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthUser')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthUser')


# if __name__ == '__main__':
    # from sqlalchemy.engine.url import URL
    # from sqlalchemy import create_engine
    # from sqlalchemy.orm import Session
    # from sqlalchemy.ext.asyncio import create_async_engine
    #
    # drivername = 'mysql+pymysql'
    # username = 'root'
    # password = 'zh@852456'
    # host = '192.168.125.31'
    # port = '3306'
    # database = 'sanic_spider'
    #
    # connect_url = URL(drivername=drivername, username=username, password=password,
    #                   host=host, port=port, database=database)
    #
    # engine = create_engine(connect_url, echo=True)

    # Base.metadata.create_all(engine)
