# Generated by Django 3.1.7 on 2021-05-02 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210501_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(blank=True, choices=[('email', '이메일'), ('github', '깃허브'), ('kakao', '카카오')], default='email', max_length=10),
        ),
    ]
