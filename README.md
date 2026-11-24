# Cementerio App

**Tema asignado:** gestión de un cementerio (sectores, difuntos, tumbas y servicios).

## Levantar el proyecto desde cero

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # si dejas DB_NAME vacío/sin definir usa SQLite; con DB_NAME usa PostgreSQL
python manage.py makemigrations   
python manage.py migrate          # también crea los grupos y permisos
python manage.py cargar_datos     
python manage.py runserver
python manage.py test cementerio  # pruebas
```

Comandos útiles: `python manage.py crear_grupos` (recrea grupos y permisos).

## Usuarios de prueba (contraseña de todos: `Cementerio2026*`)

| Usuario | Rol / grupo | Qué puede hacer |
|---|---|---|
| superadmin | Superusuario | Todo, incluido `/admin/` |
| admin_cementerio | administradores | Crear, editar y eliminar en las 4 entidades |
| consultor1 | consultores | Ver todo; crear tumbas; editar/eliminar solo las tumbas que creó |
| consultor2 | consultores | Igual que consultor1 (sirve para probar la regla de propiedad) |

Los usuarios que se registran en `/cuentas/registro/` entran al grupo **consultores**.

## Reglas de acceso

- Todas las vistas requieren `@login_required` y `@permission_required`; los botones se ocultan con `perms.*`.
- Regla de propiedad (`creado_por`): solo quien creó un registro (o un administrador) puede editarlo o eliminarlo.
