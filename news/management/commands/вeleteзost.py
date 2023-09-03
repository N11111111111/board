from django.core.management.base import BaseCommand, CommandError
from news.models import *


class Command(BaseCommand):
    help = 'УДАЛЕНИЕ ВСЕХ ПОСТОВ С САЙТА'

    def handle(self, *args, **options):
        admin_code = '0000'
        answer = input('Введите код для удаления всех постов: ')

        if answer == admin_code:
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Все посты удалены!'))
        else:
            self.stdout.write(self.style.ERROR('Не верный код, в доступе отказано!'))