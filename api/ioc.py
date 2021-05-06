from injector import Module, singleton

from api.security.abstract_access_token_service import AbstractAccessTokenService
from api.security.access_token_service import AccessTokenService


# define here all root ioc bindings
class ApiAppModule(Module):
    def configure(self, binder):
        # services

        access_token_service = AccessTokenService()
        binder.bind(AbstractAccessTokenService, to=access_token_service, scope=singleton)
