from django.urls import path
from Users import views as v
from .views import CustomLoginView, CustomLogoutView, search_users

app_name = 'Users'

urlpatterns = [
    path('registration/', v.registration, name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('my_profile/', v.my_profile, name='my_profile'),
    path('another_profile/<int:user_id>', v.another_profile, name='another_profile'),
    path('search/', v.search_users, name='search'),
    path('send_request/<int:user_id>/', v.send_request, name='send_request'),
    path('confirm_friend/<int:user_id>/', v.confirm_friend, name='confirm_friend'),
    path('delete_friend/<int:user_id>/', v.delete_friend, name='delete_friend'),
    path('subscribe/<int:user_id>/', v.subscribe,  name='subscribe'),
    path('cancel_subscribe/<int:user_id>/', v.cancel_subscribe, name='cancel_subscribe'),
    path('my_friends/', v.show_my_friends, name='my_friends'),
    path('my_subscribes/', v.show_my_subscribes, name='my_subscribes'),
    path('my_subscribers/', v.show_my_subscribers, name='my_subscribers'),
    path('my_dialogs/', v.show_my_dialogs, name='show_my_dialogs'),
    path('my_apps/', v.show_my_apps, name='my_apps'),
    path('change_info/', v.change_info, name='change_info')
    ]
