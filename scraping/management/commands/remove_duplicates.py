from django.db.models import Count, Max
from users.models import Post
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # define logic of command
    def handle(self, *args, **options):
        MyModel = Post

        unique_fields = ['title']
        duplicates = (
            MyModel.objects.values(*unique_fields)
            .order_by()
            .annotate(max_id=Max('id'), count_id=Count('id'))
            .filter(count_id__gt=1)
        )
        print(duplicates)
        self.stdout.write('Scanning...😁')

        msg = "Removing Duplicates✅"
        if not duplicates.exists():
            msg = "No Duplicates Was Found 🤷🏾‍♂️"

        for duplicate in duplicates:
            (
                MyModel.objects
                .filter(**{x: duplicate[x] for x in unique_fields})
                .exclude(id=duplicate['max_id'])
                .delete()
            )
            print('%s ❌' % (duplicate,))
        self.stdout.write(msg)
