# Generated by Django 4.0.6 on 2022-10-05 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Socket', '0002_message_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='img',
        ),
    ]