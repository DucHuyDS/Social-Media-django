# Generated by Django 4.0.6 on 2022-10-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Socket', '0005_alter_message_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='chat'),
        ),
    ]