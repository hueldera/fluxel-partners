from django.db.models import *
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django_bleach.models import BleachField
from .utils import simple_mail
from django.utils.translation import gettext_lazy as _

BOOTSTRAP_COLORS = [
    ('primary', 'blue'), ('secondary', 'gray'),
    ('success', 'green'), ('danger', 'red'),
    ('warning', 'yellow'), ('info', 'ice blue'),
    ('light', 'light gray'), ('dark', 'dark gray'),
    ('white', 'white')]

ALLOWED_TAGS = ['strong', 'p', 'thead', 'blockquote', 'a', 'tbody', 'div',
                'input', 'textareaem', 'hr', 'img', 'tr', 'col' 'coltr', 'td', 'table',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'br', 'u', 's', 'code',
                'sub', 'sup', 'i', 'font', 'span', 'mark', 'em', 'li', 'ul', 'ol', 'cite']


class Type(Model):
    name = CharField(max_length=100, unique=True)
    description = CharField(max_length=255, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Status(Model):
    name = CharField(max_length=100, unique=True)
    description = CharField(max_length=255, blank=True)
    color = CharField(max_length=100, choices=BOOTSTRAP_COLORS)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "status"

    def __str__(self):
        return f"{self.name}"


class TypeItem(Model):
    name = CharField(max_length=100, unique=True)
    description = CharField(max_length=255, blank=True)
    cost_value = FloatField(blank=True)
    order_type = ForeignKey(Type, on_delete=PROTECT)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - BRL {self.cost_value}"


class Order(Model):
    description = BleachField(allowed_tags=ALLOWED_TAGS)
    item = ForeignKey(TypeItem, on_delete=PROTECT)
    status = ForeignKey(Status, on_delete=PROTECT)
    author = ForeignKey(User, on_delete=PROTECT)
    budget = FloatField()
    deadline = DateTimeField()
    customer = CharField(max_length=150)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.customer} - {self.status} @{self.created_at}'


class StatusChange(Model):
    new_status = ForeignKey(Status, on_delete=PROTECT)
    order = ForeignKey(Order, on_delete=PROTECT)
    author = ForeignKey(User, on_delete=PROTECT)
    note = TextField(null=True, blank=True)
    notify_author = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order} - {self.status}'


class Message(Model):
    author = ForeignKey(User, on_delete=PROTECT)
    message = TextField()
    order = ForeignKey(Order, on_delete=PROTECT)
    status = ForeignKey(Status, on_delete=PROTECT)
    created_at = DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.author != self.order.author:
            to = self.author.email
        else:
            to = 'fluxelco@gmail.com'
        simple_mail(_('You received a new message'), _('''You received a new message related 
to order #{order} in Fluxel Digital platform. 
For view the message access the system or this url: https://partners.fluxel.co/orders/messages/{order} .'''.format(order=self.order.id)),
                    self.author.username,
                    [to])

        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return f'#{self.id} - {self.author} - {self.order.customer}@{self.order.created_at}'
