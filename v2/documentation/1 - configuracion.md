# Guía paso a paso para configurar migraciones con Flask-Migrate en PostgreSQL (sin código)

## 1. Preparar el entorno

- Instalar PostgreSQL y crear usuario y base de datos.
- Crear un entorno virtual e instalar dependencias:
  - pip install -r requirements.txt

---

## 2. Configurar la aplicación

- Archivo: `config.py`
  - Definir configuración básica.
  - Definir configuración de despliegue con variable de entorno para la URI de la base de datos.

- Archivo: `app/__init__.py` o archivo principal de la app
  - Inicializar Flask.
  - Configurar SQLAlchemy y Flask-Migrate.
  - Importar modelos para registro.

---

## 3. Inicializar migraciones

- Ejecutar en consola desde la raíz del proyecto:

  ```
  flask --app app:crear_app db init
  ```

- Esto crea la carpeta `migrations/`.

---

## 4. Crear migración inicial

- Ejecutar en consola:

  ```
  flask --app app:crear_app db migrate -m "Migración inicial"
  ```

- Revisar el archivo generado en `migrations/versions/`.

---

## 5. Aplicar migración a la base de datos

- Ejecutar en consola:

  ```
  flask --app app:crear_app db upgrade
  ```

- Esto crea o actualiza las tablas en PostgreSQL.

---

## 6. Ejecutar la aplicación

- Ejecutar en consola:

  ```
  flask --app app:crear_app run
  ```

- Abrir en navegador: `http://localhost:5000`

---

## 7. Flujo para futuros cambios en modelos

- Cada vez que modifiques modelos:

  1. Crear migración:

     ```
     flask --app app:crear_app db migrate -m "Descripción del cambio"
     ```

  2. Aplicar migración:

     ```
     flask --app app:crear_app db upgrade
     ```

---

## 8. Notas importantes

- Crear la base de datos PostgreSQL manualmente antes de usar migraciones.
- Mantener la carpeta `migrations/` bajo control de versiones.
- Usar variables de entorno para credenciales.
- Revisar siempre las migraciones generadas antes de aplicarlas.