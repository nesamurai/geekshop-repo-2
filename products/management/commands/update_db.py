from django.core.management.base import BaseCommand
from users.models import User, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            users_profile = ShopUserProfile.objects.create(user=user)
            users_profile.save()
