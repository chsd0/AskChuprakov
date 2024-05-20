from django.core.management.base import BaseCommand
from app.models import *

class Command(BaseCommand):

    help = "TEST FUNCTION"

    def handle(self, *args, **kwargs):
        for profile in Profile.objects.all():
            profile.image = 'pic/aph.jpg'
            profile.save()
        print('Done!')