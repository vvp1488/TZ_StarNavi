# Generated by Django 3.2.6 on 2021-09-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_useractivity_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='user_last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='%Y-%m-%d %H:%M:%S'),
        ),
    ]