# Generated by Django 5.0.6 on 2025-03-01 21:09

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('student_class', models.CharField(max_length=50)),
                ('date_created', models.DateField()),
                ('type', models.CharField(choices=[('Day', 'Day'), ('Boarding', 'Boarding')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='AmountPaid',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ref_code', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_paying_amount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date_complete', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=False)),
                ('amount_paid', models.ManyToManyField(related_name='amount_paid', to='core.amountpaid')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_paying', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('admission_number', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('dob', models.DateField(blank=True, null=True)),
                ('npi', models.CharField(max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('about_student', models.CharField(max_length=255, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('type', models.CharField(choices=[('Day', 'Day'), ('Boarding', 'Boarding')], max_length=10)),
                ('parents', models.ManyToManyField(blank=True, related_name='parents', to=settings.AUTH_USER_MODEL)),
                ('payments', models.ManyToManyField(blank=True, related_name='students', to='core.payment')),
                ('students_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.fee')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_paying', to='core.student'),
        ),
        migrations.AddField(
            model_name='fee',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.studentclass'),
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('fee_deadline', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('fee_amount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.fee')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.term'),
        ),
    ]
