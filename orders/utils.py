from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _


def simple_mail(subject, content, name, send_to):

    plaintext = get_template('orders/email/simple_message.txt')
    html = get_template('orders/email/simple_message.html')

    content = content
    ctx = {'username': name, 'content': content}
    text_content = plaintext.render(ctx)
    html_content = html.render(ctx)

    from_email = 'contact@fluxel.co'
    msg = EmailMultiAlternatives(subject, text_content, from_email, send_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
