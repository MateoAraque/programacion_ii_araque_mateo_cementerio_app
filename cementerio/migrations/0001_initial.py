import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sectores_creados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'sector',
                'verbose_name_plural': 'sectores',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Difunto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('fecha_fallecimiento', models.DateField()),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='difuntos_creados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'difunto',
                'verbose_name_plural': 'difuntos',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Tumba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('estado', models.CharField(choices=[('DISPONIBLE', 'Disponible'), ('OCUPADA', 'Ocupada'), ('MANTENIMIENTO', 'En mantenimiento')], default='DISPONIBLE', max_length=20)),
                ('capacidad', models.PositiveSmallIntegerField(default=1)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tumbas_creadas', to=settings.AUTH_USER_MODEL)),
                ('difuntos', models.ManyToManyField(blank=True, related_name='tumbas', to='cementerio.difunto')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tumbas', to='cementerio.sector')),
            ],
            options={
                'verbose_name': 'tumba',
                'verbose_name_plural': 'tumbas',
                'ordering': ['codigo'],
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('INHUMACION', 'Inhumación'), ('EXHUMACION', 'Exhumación'), ('MANTENIMIENTO', 'Mantenimiento'), ('MISA', 'Misa / ceremonia')], max_length=20)),
                ('fecha', models.DateField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('responsable', models.CharField(max_length=100)),
                ('observaciones', models.TextField(blank=True)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servicios_creados', to=settings.AUTH_USER_MODEL)),
                ('tumba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios', to='cementerio.tumba')),
            ],
            options={
                'verbose_name': 'servicio',
                'verbose_name_plural': 'servicios',
                'ordering': ['-fecha'],
            },
        ),
    ]
