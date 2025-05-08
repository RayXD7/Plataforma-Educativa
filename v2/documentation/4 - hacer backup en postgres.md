# Cómo hacer un backup y restaurar una base de datos en PostgreSQL

## 1. Realizar un backup (copia de seguridad)

### Backup en formato SQL plano

Guarda toda la base de datos en un archivo `.sql` que puede ser restaurado fácilmente:

```
pg_dump -U  -h  -d  -f .sql
```

**Ejemplo:**

```
- pg_dump -U postgres -h localhost -d mi_base -f mi_base_backup.sql

- pg_dump -U postgres -h localhost -p 5432 UIJ_actividades > actividades.sql
```

- ``: Usuario de PostgreSQL (ej. `postgres`)
- ``: Servidor, normalmente `localhost`
- ``: Nombre de la base a respaldar
- `.sql`: Nombre del archivo de respaldo

---

### Backup en formato personalizado

Permite restauraciones más flexibles:

```
pg_dump -U  -h  -F c -d  -f .dump
```

---

### Backup de tablas específicas

```
pg_dump -U  -h  -d  -t  -f .sql
```

---

## 2. Restaurar una base de datos desde un backup

### Restaurar desde un archivo SQL plano

Primero crea la base de datos vacía si no existe:

```
createdb -U  -h  
```

Luego ejecuta:

```
psql -U  -h  -d  -f .sql
```

---

### Restaurar desde un backup en formato personalizado

```
pg_restore -U  -h  -d  .dump
```

---

## 3. Opciones útiles

| Opción         | Descripción                                   |
|----------------|-----------------------------------------------|
| -U    | Usuario de PostgreSQL                         |
| -h       | Host del servidor                             |
| -d         | Nombre de la base de datos                    |
| -f    | Archivo de salida o entrada                   |
| -F c           | Formato personalizado (custom)                |
| -t      | Solo una tabla específica                     |

---

## 4. Notas

- Siempre verifica que el usuario tenga permisos suficientes.
- Puedes automatizar el backup usando scripts y tareas programadas.
- Para restaurar, la base de datos debe existir (excepto si usas la opción `-C` en `pg_restore`).
- Nunca incluyas contraseñas en los scripts; usa el archivo `.pgpass` si es necesario.

