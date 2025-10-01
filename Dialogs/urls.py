from django.urls import path
from Dialogs import views as v

app_name = 'Dialogs'

urlpatterns = [
    path('messages/', v.messages, name='my_dialogs'),
    path('dialog/<int:user_id>/', v.dialog, name='dialog'),
    path('post/<int:user_id>/', v.post, name='post'),
    path('leave_message/<int:user_id>/', v.leave_message, name='leave_message'),
    path('delete_message/<int:message_id>/', v.delete_message, name='delete_message'),
    path('delete_dialog/<int:companion_id>/', v.delete_dialog, name='delete_dialog'),
    path('new_messages/', v.new_messages, name='new_messages'),
]
