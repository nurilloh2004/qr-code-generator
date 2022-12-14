# Generated by Django 4.1.3 on 2022-12-01 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='Tashkent', max_length=250)),
                ('scan_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='CommonModelFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, max_length=250, null=True)),
                ('logo_type', models.IntegerField(default=0)),
                ('scan_count', models.IntegerField(default=0)),
                ('background', models.CharField(blank=True, max_length=250, null=True)),
                ('symbol_color', models.CharField(blank=True, max_length=250, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='Uzbekistan', max_length=250)),
                ('scan_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='PC', max_length=250)),
                ('scan_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailQrCode',
            fields=[
                ('commonmodelfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qs_code.commonmodelfields')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=250)),
                ('message', models.TextField(blank=True, null=True)),
                ('email_image', models.FileField(blank=True, upload_to='email_qr_code/')),
            ],
            options={
                'verbose_name_plural': 'EmailQrCodes',
            },
            bases=('qs_code.commonmodelfields', models.Model),
        ),
        migrations.CreateModel(
            name='SmsQrCode',
            fields=[
                ('commonmodelfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qs_code.commonmodelfields')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=250)),
                ('message', models.TextField(blank=True, null=True)),
                ('url_id', models.IntegerField(default=1)),
                ('sms_image', models.FileField(blank=True, upload_to='sms_qr_code/')),
            ],
            options={
                'verbose_name_plural': 'SmsQrCodes',
            },
            bases=('qs_code.commonmodelfields', models.Model),
        ),
        migrations.CreateModel(
            name='TextQrCode',
            fields=[
                ('commonmodelfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qs_code.commonmodelfields')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('text_qr_image', models.FileField(blank=True, upload_to='text_qr_code/')),
                ('url_id', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'TextQrCodes',
            },
            bases=('qs_code.commonmodelfields', models.Model),
        ),
        migrations.CreateModel(
            name='TwitterQrCode',
            fields=[
                ('commonmodelfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qs_code.commonmodelfields')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(blank=True, max_length=250, null=True)),
                ('tweet', models.TextField(blank=True, null=True)),
                ('twitter_type', models.CharField(choices=[('Profile', 'Profile'), ('Post', 'Post')], default='Profile', max_length=10)),
                ('url_id', models.IntegerField(default=1)),
                ('twitter_image', models.FileField(blank=True, upload_to='twitter_qr_code/')),
            ],
            options={
                'verbose_name_plural': 'TwitterQrCode',
            },
            bases=('qs_code.commonmodelfields', models.Model),
        ),
        migrations.CreateModel(
            name='UrlQrCode',
            fields=[
                ('commonmodelfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qs_code.commonmodelfields')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('link', models.URLField(max_length=10000)),
                ('qr_image', models.ImageField(blank=True, upload_to='url_qr_codes/')),
                ('url_id', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'UrlQrCodes',
                'ordering': ['-id'],
            },
            bases=('qs_code.commonmodelfields', models.Model),
        ),
        migrations.CreateModel(
            name='VcardQrCode',
            fields=[
                ('commonmodelfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qs_code.commonmodelfields')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=250)),
                ('cellphone', models.CharField(max_length=250)),
                ('homephone', models.CharField(blank=True, max_length=250, null=True)),
                ('fax', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('company', models.CharField(blank=True, max_length=250, null=True)),
                ('job', models.CharField(blank=True, max_length=250, null=True)),
                ('street', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=250, null=True)),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('vcard_qr_image', models.FileField(blank=True, upload_to='vcard_qr_code/')),
                ('url_id', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'VcardQrCodes',
            },
            bases=('qs_code.commonmodelfields', models.Model),
        ),
        migrations.CreateModel(
            name='WifiQrCode',
            fields=[
                ('commonmodelfields_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qs_code.commonmodelfields')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('network_name', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('encryription_type', models.CharField(choices=[('None', 'None'), ('WPA/WPA2', 'WPA/WPA2'), ('WEP', 'WEP')], default='WPA/WPA2', max_length=10)),
                ('is_hidden', models.BooleanField(default=False)),
                ('url_id', models.IntegerField(default=1)),
                ('wifi_image', models.FileField(blank=True, upload_to='wifi_qr_code/')),
            ],
            options={
                'verbose_name_plural': 'WifiQrCodes',
            },
            bases=('qs_code.commonmodelfields', models.Model),
        ),
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField(default='84.54.74.20')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs_code.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs_code.country')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qs_code.device')),
            ],
            options={
                'verbose_name_plural': 'IpAddresses',
            },
        ),
    ]
