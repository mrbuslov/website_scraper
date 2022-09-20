from django.core.mail import send_mail

def send_file_email(user_email):
    send_mail(
        'Тема',
        'Описание',
        'buslovdmitrij0@gmail.com',
        [user_email],
        fail_silently=False
    )