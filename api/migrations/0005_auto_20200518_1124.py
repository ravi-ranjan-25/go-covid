# Generated by Django 3.0.2 on 2020-05-18 11:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_auto_20200511_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0, max_length=256)),
                ('orderid', models.CharField(default='NA', max_length=256, unique=True)),
                ('accept', models.IntegerField(default=-1, max_length=256)),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 5, 18, 11, 24, 34, 291931, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0, max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=256, unique=True)),
                ('admin', models.BooleanField(default=False)),
                ('objectname', models.CharField(default='NA', max_length=256)),
                ('category', models.CharField(default='NA', max_length=256)),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 5, 18, 11, 24, 34, 287498, tzinfo=utc))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='storerestro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preparing_packaging', models.BooleanField(default=False)),
                ('dispatched', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('Rating', models.FloatField(default=0.0, max_length=256)),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 5, 18, 11, 24, 34, 293168, tzinfo=utc))),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(default='NA', max_length=256)),
                ('productid', models.CharField(default='NA', max_length=256, unique=True)),
                ('productDescription', models.CharField(default='NA', max_length=256)),
                ('stock', models.IntegerField(default=-1, max_length=256)),
                ('active', models.BooleanField(default=True)),
                ('display', models.CharField(default='https://www.vikasanvesh.in/wp-content/themes/vaf/images/no-image-found-360x260.png', max_length=256)),
                ('costPrice', models.FloatField(default=0.0, max_length=256)),
                ('sellingPrice', models.FloatField(default=0.0, max_length=256)),
                ('discount', models.FloatField(default=0.0, max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
