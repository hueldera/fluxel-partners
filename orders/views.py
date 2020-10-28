from django.shortcuts import render
from .forms import OrderForm
from .models import Order, Status, Message, StatusChange
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from allauth.account.models import EmailAddress
from .utils import simple_mail
const = {
    'NOT_ALLOWED_STATUS_LIST': ('Canceled', 'Done')
}


def status_update(old_status, order, author):
    if old_status != order.status:
        new_status = StatusChange()
        new_status.new_status = order.status
        new_status.order = order
        new_status.author = author
        new_status.note = ''
        notify_author = True

        simple_mail(
            _('Status of order #{order} has been updated').format(
                order=order.id),
            _('''The #{order} has been updated to status "{status}". 
            Access the Fluxel Digital Partners platform for more details.'''
              ).format(order=order.id, status=order.status.name),
            author.username, [order.author.email])

        new_status.save()


@login_required
def index(request):
    user_orders_list = Order.objects.filter(
        author=request.user).order_by('-updated_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(user_orders_list, 10)

    try:
        user_orders = paginator.page(page)
    except PageNotAnInteger:
        user_orders = paginator.page(1)
    except EmptyPage:
        user_orders = paginator.page(paginator.num_pages)

    return render(request, 'orders/index.html', dict({
        'user_orders': user_orders
    }, **const))


@login_required
def create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = Status.objects.get(name='Awaiting Aproval')
            order.author = request.user
            order.save()

            send_to = EmailAddress.objects.get(
                user=request.user, primary=True).email

            subject = _(
                'Order #{id} has been created successfully').format(id=order.id)
            content = _('''Your order #{id} ({customer}) has been created. At first the team should analyse the
briefing before you can follow to payment. You can track the status of your order in the system.
''').format(id=order.id, customer=order.customer)
            username = request.user.username

            simple_mail(subject, content, username, [send_to])

            messages.success(request,
                             f'Order #{ order.id } ({ order.customer }) created successfuly')
            return HttpResponseRedirect('/orders/')
        else:
            messages.warning(request,
                             _('Invalid Order! Please fill all fields'))
    else:
        form = OrderForm()
    return render(request, 'orders/create.html', {'order_form': form})


@login_required
def detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.author == request.user:
        return render(request, 'orders/details.html', {
            'order': order
        })

    return HttpResponseNotAllowed()


@login_required
def cancel(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status.name in const['NOT_ALLOWED_STATUS_LIST']:
        return HttpResponseRedirect('/orders')
    if order.author == request.user:
        if request.method == 'POST':
            pwd = request.POST.get('validate_password')
            if request.user.check_password(pwd):
                old_status = order.status
                order.status = order.status = Status.objects.get(
                    name='Canceled')
                order.save()
                send_to = EmailAddress.objects.get(
                    user=request.user, primary=True).email

                subject = _(
                    'Order #{id} has been canceled.').format(id=order.id)
                content = _('''Your order #{id} ({customer}) has been canceled.
    ''').format(id=order.id, customer=order.customer)
                username = request.user.username

                # simple_mail(subject, content, username, [send_to])
                status_update(old_status, order, request.user)
                messages.success(request, _('Order canceled successfuly'))
                return HttpResponseRedirect('/orders')
            else:
                messages.warning(request, _('Wrong password, try again'))
        return render(request, 'orders/confirmation.html', {
            'order': order
        })

    return HttpResponseNotAllowed()


@login_required
def update(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.status.name in const['NOT_ALLOWED_STATUS_LIST']:
        return HttpResponseRedirect('/orders')
    if order.author == request.user:
        if request.method == 'POST':
            order_form = OrderForm(request.POST, instance=order)
            if order_form.is_valid() and request.POST.get('agree') == 'on':
                order = order_form.save(commit=False)
                old_status = order.status
                order.status = Status.objects.get(
                    name='Awaiting Aproval')
                order.save()
                send_to = EmailAddress.objects.get(
                    user=request.user, primary=True).email

                subject = _(
                    'Order #{id} has been updated.').format(id=order.id)
                content = _('''Your order #{id} ({customer}) has been updated. 
Now you need to wait again to order be approved by our team.
    ''').format(id=order.id, customer=order.customer)
                username = request.user.username

                simple_mail(subject, content, username, [send_to])
                status_update(old_status, order, request.user)
                messages.success(request, _('Order updated successfuly'))
                return HttpResponseRedirect('/orders')
            else:
                messages.warning(
                    request, _('Invalid order, please check all fields'))

        order_form = OrderForm(instance=order)
        return render(request, 'orders/edit.html', {
            'order': order,
            'order_form': order_form
        })

    return HttpResponseNotAllowed()


@login_required
def order_messages(request, order_id):
    order = Order.objects.get(pk=order_id)

    if order.author == request.user:
        if request.method == 'POST':
            if order.status.name in const['NOT_ALLOWED_STATUS_LIST']:
                return HttpResponseRedirect('/orders')
            content = request.POST.get('msg_content')
            status = order.status
            author = request.user

            new_message = Message(
                message=content, status=order.status, order=order, author=request.user)
            new_message.save()

            return HttpResponseRedirect(f'/orders/messages/{order.id}')

        order_messages = Message.objects.filter(order=order)
        return render(request, 'orders/messages.html', dict({
            'order': order,
            'order_messages': order_messages
        }, **const))
