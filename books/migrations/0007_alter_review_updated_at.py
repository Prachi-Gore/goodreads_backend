# Generated by Django 5.1.1 on 2025-03-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_review_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
