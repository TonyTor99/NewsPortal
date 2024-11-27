from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление постов по категориям'

    def handle(self, *args, **options):
        categories = Category.objects.all().values_list('cat_name', flat=True)

        for cat in categories:
            obj = Category.objects.get(cat_name=cat)
            pk_category = obj.pk
            self.stdout.write(f'{pk_category}.{cat}')

        self.stdout.write('Напишите номер категории посты которых хотели бы удалить')
        category = input()

        self.stdout.write('Вы точно хотите удалить посты этой категории? Да/Нет')
        answer = input().lower()

        if answer == 'да':
            Post.objects.filter(category__pk=category).delete()
            self.stdout.write(self.style.SUCCESS('Посты в категории очищенны'))
            return

        self.stdout.write(self.style.ERROR('Отменено'))
