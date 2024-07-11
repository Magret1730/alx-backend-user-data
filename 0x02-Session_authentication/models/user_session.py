#!/usr/bin/env python3
""" UserSession module """

from models.base import Base
import models
import uuid


class UserSession(Base):
    """ UserSession class """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id', str(uuid.uuid4()))

    def save(self):
        """ Save the session to the database (file) """
        models.storage.new(self)
        models.storage.save()
