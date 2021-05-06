from django.urls import path, include
from .views import UserRolesCreateAPIView, UserRolesListAPIView

user_role_read_patterns = ([
                               path('', UserRolesListAPIView.as_view({'get': 'list'}), name='index'),
                           ], 'user-roles-read')

user_role_patterns = ([
                          path('', UserRolesCreateAPIView.as_view(
                              {
                                  'post': 'create',
                                  'delete': 'remove',
                              }
                          ), name='create'),
                      ], 'user-roles-write')

public_urlpatterns = [
    path('user-roles', include(user_role_read_patterns)),
]

private_urlpatterns = [
    path('user-roles', include(user_role_patterns)),
]
