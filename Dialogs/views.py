from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Message
from Users.models import Friend, Status
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
import datetime

User = get_user_model()


@login_required
def post(request, user_id):
    try:
        companion = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден'}, status=404)
    messages = Message.objects.filter(reciever=request.user, 
                                      sender=companion,
                                      is_readed=False)
    for message in messages:
        message.is_readed = True
        message.save()
    context = {'messages': messages, 'user': request.user}
    if messages:
        return JsonResponse({"result": True, "messages_count": len(messages),})
    else:
        return JsonResponse({"result": False,})


@login_required
def dialog(request, user_id):
    try:
        companion = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("Пользователь не найден")
    # Получаем сообщения
    messages = (Message.objects.filter(
        sender=request.user, 
        reciever=companion, 
        sender_visibility=True
    ) | Message.objects.filter(
        reciever=request.user, 
        sender=companion, 
        reciever_visibility=True
    )).order_by("-message_time")[:50]
    # Помечаем непрочитанные сообщения как прочитанные
    not_readed_messages = Message.objects.filter(
        reciever=request.user, 
        sender=companion, 
        is_readed=False
    )
    for message in not_readed_messages:
        message.is_readed = True
        message.save()
    context = {
        'sort_messages': messages[::-1],
        'friend': companion,
        'user': request.user
    }
    return render(request, 'dialogs/dialog.html', context)


#Проверка на новые сообщения
@login_required(login_url = '/')
def new_messages(request):
    messages = Message.objects.filter(reciever = request.user, is_readed = False)
    new_friends = Friend.objects.filter(users_friend = request.user, confirmed = False)
    status_for_update = {'online':timezone.now()}
    user_status, created = Status.objects.update_or_create(user = request.user, defaults = status_for_update)
    if messages or new_friends:
        return HttpResponse(
            json.dumps({
                "result": True,
                "messages_count": len(messages),
                "new_friends": len(new_friends),
            }), content_type="application/json"
        )
    else:
        return HttpResponse(json.dumps({"result": False,}),
                            content_type="application/json")


@login_required
def leave_message(request, user_id):
    try:
        reciever_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден'}, status=404)
    
    if request.method == 'POST':
        message_text = request.POST.get('message_text', '').strip()
        if not message_text:
            return JsonResponse({'error': 'Сообщение не может быть пустым'}, status=400)
        if len(message_text) > 500:
            save_message_text = message_text[:499]
        else:
            save_message_text = message_text
        message = Message(
            sender=request.user, 
            reciever=reciever_user, 
            message_text=save_message_text, 
            message_time=timezone.now()
        )
        message.save()
        return JsonResponse({'success': True,
                             'message_id': message.id,
                             'message_text': message.message_text,
                             'message_time': message.message_time.strftime("%H:%M"),
                             'is_readed': message.is_readed})
    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)


@login_required
def delete_dialog(request, companion_id):
    try:
        companion = User.objects.get(id=companion_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Собеседник не найден'}, status=404)
    # Сообщения где пользователь отправитель
    send_messages = Message.objects.filter(sender=request.user, reciever=companion)
    for message in send_messages:
        message.sender_visibility = False
        if not message.reciever_visibility:
            message.delete()
        else:
            message.save()
    # Сообщения где пользователь получатель
    reciever_messages = Message.objects.filter(reciever=request.user, sender=companion)
    for message in reciever_messages:
        message.reciever_visibility = False
        if not message.sender_visibility:
            message.delete()
        else:
            message.save()
    # return JsonResponse({'status': 'ok'})
    return redirect('Dialogs:my_dialogs')


#Вывод всех диалогов пользователя
@login_required
def messages(request):
    messages = (Message.objects.filter(sender = request.user, sender_visibility = True) | Message.objects.filter(reciever = request.user, reciever_visibility = True)).order_by("-message_time")
    users = []
    last_messages = []
    for message in messages:
        if message.sender != request.user:
            if not message.sender in users:
                users.append(message.sender)
                last_message = (Message.objects.filter(sender = message.sender, reciever = request.user)|Message.objects.filter(reciever = message.sender, sender = request.user)).order_by("-message_time")[:1]
                last_messages.append(last_message)
        if message.reciever != request.user:
            if not message.reciever in users:
                users.append(message.reciever)
                last_message = (Message.objects.filter(sender = message.reciever, reciever = request.user)|Message.objects.filter(reciever = message.reciever, sender = request.user)).order_by("-message_time")[:1]
                last_messages.append(last_message)
    last_messages_list = []
    for message_query in last_messages:
        for message in message_query:
            if not message.is_readed and message.reciever == request.user:
                last_messages_list.insert(0, message)
            else:
                last_messages_list.append(message)
    users_friends1 = Friend.objects.filter(user = request.user, confirmed = True)
    users_friends2 = Friend.objects.filter(users_friend = request.user, confirmed = True)
    context = {'messages': last_messages_list, 'friends1': users_friends1, 'friends2': users_friends2 }
    return render(request, 'dialogs/my_dialogs.html', context)


@login_required
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except:
        raise Http404("Сообщение не найдено!")
    message.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
