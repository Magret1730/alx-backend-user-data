#!/usr/bin/env python3
""" SessionDBAuth module """

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ Create and store a new instance of UserSession """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return the user ID by querying UserSession """
        if session_id is None:
            return None

        try:
            sessions = models.storage.all(UserSession)
            for session in sessions.values():
                if session.session_id == session_id:
                    if self.session_duration <= 0:
                        return session.user_id

                    created_at = session.created_at
                    if created_at is None:
                        return None

                    exp_time = created_at +\
                        timedelta(seconds=self.session_duration)
                    if datetime.now() > exp_time:
                        return None

                    return session.user_id
        except Exception:
            return None
        return None

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the Session ID from the request cooki
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        try:
            sessions = models.storage.all(UserSession)
            for session in sessions.values():
                if session.session_id == session_id:
                    session.delete()
                    models.storage.save()
                    return True
        except Exception:
            return False
        return False
