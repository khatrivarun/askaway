# Generated by Django 3.1.2 on 2020-10-13 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions_answers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
