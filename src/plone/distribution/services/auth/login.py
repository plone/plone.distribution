"""Authenticate a user in Zope root."""
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.interface import alsoProvides

import plone.protect.interfaces


class LoginPost(Service):
    def reply(self):
        """Authenticate on Zope Application root."""
        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)
        data = json_body(self.request)
        login = data.get("login")
        password = data.get("password")
        acl_users = self.context.acl_users
        # credentials_cookie_auth only exists after initial Plone site is added to zope
        cookie_pas = getattr(acl_users, "credentials_cookie_auth", None)
        if cookie_pas and acl_users.authenticate(login, password, self.request):
            cookie_pas.updateCredentials(
                self.request, self.request.response, login, password
            )
            return {}
        else:
            self.request.response.setStatus(401)
            return {
                "error": {
                    "type": "Invalid credentials",
                    "message": "Wrong login and/or password.",
                }
            }
