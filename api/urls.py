from django.urls import path, include
from .views import UserRolesCreateAPIView, UserRolesListAPIView, ChannelTypesAPIView

user_role_read_patterns = ([
                               path('', UserRolesListAPIView.as_view({'get': 'list'}), name='index'),
                           ], 'user-roles-read')

user_role_patterns = ([
                          path('', UserRolesCreateAPIView.as_view(
                              {
                                  'post': 'create',
                                  'delete': 'remove',
                              }
                          ), name='create-remove'),
                      ], 'user-roles-write')

sso_patterns = ([
                          path('', UserRolesCreateAPIView.as_view(
                              {
                                  'post': 'sso',
                              }
                          ), name='sso'),
                      ], 'user-sso')

channel_types_patterns = ([
                              path('/seed', ChannelTypesAPIView.as_view(
                                  {
                                      'post': 'seed',
                                  }
                              ), name='seed'),
                          ], 'channel_types'
)

public_urlpatterns = [
    path('user-roles', include(user_role_read_patterns)),
]

private_urlpatterns = [
    path('user-roles', include(user_role_patterns)),
    path('sso', include(sso_patterns)),
    path('channel-types', include(channel_types_patterns))
]
