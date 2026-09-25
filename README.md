# Proyecto Blog - Oracle y PL/SQL

Aplicación desarrollada en Python para administrar un blog utilizando
una base de datos Oracle mediante procedimientos almacenados en PL/SQL.

## Tecnologías utilizadas

- Python
- Tkinter
- Oracle Database
- PL/SQL
- oracledb

## Archivos del proyecto

- `app.py` - Aplicación gráfica desarrollada en Python.
- `schema.sql` - Creación de las tablas y estructura de la base de datos.
- `procedures.sql` - Procedimientos almacenados utilizados por la aplicación.

## Configuración de la conexión a Oracle

Antes de ejecutar la aplicación, cada usuario debe configurar sus
propios datos de conexión a Oracle en el archivo `app.py`.

Se deben modificar los siguientes datos:

```python
DB_USER = "TU_USUARIO"
DB_PASSWORD = "TU_CONTRASEÑA"
DB_DSN = "localhost:1521/XEPDB1"
