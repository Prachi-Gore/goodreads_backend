# Generated by Django 5.1.1 on 2025-03-09 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_book_bookshelf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
