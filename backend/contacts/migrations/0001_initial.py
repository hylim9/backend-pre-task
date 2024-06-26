# Generated by Django 3.2.20 on 2024-04-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=150, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('name', models.CharField(help_text='라벨', max_length=100)),
            ],
            options={
                'db_table': 'label',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=150, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=150, null=True)),
                ('profile_picture', models.URLField(help_text='프로필사진')),
                ('name', models.CharField(help_text='이름', max_length=50)),
                ('email', models.EmailField(help_text='이메일주소', max_length=254)),
                ('phone_number', models.CharField(help_text='전화번호', max_length=20, unique=True)),
                ('company', models.CharField(help_text='회사', max_length=20)),
                ('job_title', models.CharField(help_text='직책', max_length=20)),
                ('description', models.TextField(blank=True, help_text='메모', null=True)),
                ('address', models.CharField(blank=True, help_text='주소', max_length=250, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('homepage_url', models.URLField(blank=True, null=True)),
                ('label', models.ManyToManyField(related_name='contacts', to='contacts.Label')),
            ],
            options={
                'db_table': 'contact',
            },
        ),
    ]
