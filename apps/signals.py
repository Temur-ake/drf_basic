from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from apps.models import User, ProductHistory, Product


@receiver(pre_save, sender=User)
def update_user_balance(sender, instance: User, **kwargs):
    if not isinstance(instance.balance, int) or instance.balance == 0:
        instance.balance = 5000


@receiver(post_save, sender=User)
def send_user_balance_via_email(sender, instance: User, **kwargs):
    send_mail(
        'Your Balance Update',
        f'Your balance has been updated to {instance.balance}.',
        'kozimovt0@gmail.com',
        [instance.email],
        fail_silently=False,

    )
    print(f'Pochtaga Yuborildi ({sender.email})')


@receiver(post_delete, sender=Product)
def after_delete_save__product(sender, instance: Product, **kwargs):
    ProductHistory.objects.create(
        name=instance.name,
        price=instance.price,
        is_premium=instance.is_premium,
        description=instance.description,
        category=instance.category,
        owner=instance.owner,
    )
    print(f"O'chirilgan {instance.name} ProductHistory ga saqlandi")