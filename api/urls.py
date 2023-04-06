
from django.urls import path
from . import views

app_name = "api"
urlpatterns = [
    path('illusion/', views.IllusionList.as_view(), name='illusion_get_post'),
    path('illusion/<int:pk>', views.IllusionList.as_view(), name='illusion_put_delete'),
    path('users/', views.UserList.as_view(), name='user_get_post'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user_get_detail'),

]
