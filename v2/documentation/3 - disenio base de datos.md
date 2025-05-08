# Diagrama Entidad-Relación (ER) de la Base de Datos
Se presenta el diagrama entidad-relación (ER) de la base de datos utilizada en la aplicación. El diagrama ilustra las diferentes entidades y sus relaciones.

## Descripción de Entidades y Relaciones
### Entidades
- **FACULTY (Facultad)**: Representa las diferentes facultades dentro de la institución.
  
- **USER (Usuario)**: Representa a los usuarios que pueden ser administradores, profesores o estudiantes. Los usuarios pueden crear actividades, participar en ellas y dejar comentarios.
- **ACTIVITY (Actividad)**: Representa las actividades organizadas en la plataforma. Cada actividad puede tener comentarios y está asociada a un usuario que la crea.
- **COMMENT (Comentario)**: Representa los comentarios que los usuarios pueden dejar en las actividades. Cada comentario está asociado a un usuario y a una actividad.
- **SURVEY (Encuesta)**: Representa las encuestas que pueden contener preguntas.
- **QUESTION (Pregunta)**: Representa las preguntas dentro de una encuesta. Cada pregunta puede tener varias opciones de respuesta.
- **CHOICE (Opción)**: Representa las opciones de respuesta disponibles para cada pregunta en una encuesta.
- **RESPONSE (Respuesta)**: Representa las respuestas que los usuarios envían a las preguntas de las encuestas.
### Relaciones
- **pertenece_a**: Una facultad puede tener muchos usuarios (1 a muchos).
  
- **crea**: Un usuario puede crear muchas actividades (1 a muchos).
- **participa_en**: Un usuario puede participar en muchas actividades y una actividad puede tener muchos usuarios participando (muchos a muchos).
- **autor_de**: Un usuario puede ser el autor de muchos comentarios (1 a muchos).
- **tiene**: Una actividad puede tener muchos comentarios (1 a muchos).
- **contiene**: Una encuesta puede contener muchas preguntas (1 a muchos).
- **ofrece**: Una pregunta puede ofrecer muchas opciones de respuesta (1 a muchos).
- **recibe**: Una opción puede recibir muchas respuestas (1 a muchos).
- **envía**: Un usuario puede enviar muchas respuestas a las preguntas (1 a muchos).
Este diagrama y las descripciones proporcionan una visión general de la estructura de la base de datos y las relaciones entre las diferentes entidades en la aplicación.
  

---

## 1. `faculty`

| Columna | Tipo             | Restricciones        | Descripción                                                      |
|---------|------------------|----------------------|------------------------------------------------------------------|
| id      | INTEGER          | PK, autoincrement    | Identificador único de la facultad.                              |
| name    | VARCHAR(100)     | UNIQUE, NOT NULL     | Nombre oficial de la facultad (por ejemplo: “Informática”).      |

**Descripción:**  
La tabla **faculty** almacena las distintas facultades o unidades académicas. Cada facultad se identifica con un `id` y tiene un nombre único. Esta entidad permite asociar profesores y estudiantes a una unidad organizativa concreta.

---

## 2. `user`

| Columna         | Tipo        | Restricciones                          | Descripción                                                       |
|-----------------|-------------|----------------------------------------|-------------------------------------------------------------------|
| id              | INTEGER     | PK                                     | Identificador único del usuario.                                  |
| username        | VARCHAR(80) | UNIQUE, NOT NULL                       | Nombre de usuario para el inicio de sesión.                       |
| password_hash   | VARCHAR(128)| NOT NULL                               | Contraseña cifrada mediante hash seguro.                          |
| role            | ENUM        | (‘admin’,‘teacher’,‘student’), NOT NULL, DEFAULT ‘student’ | Rol del usuario dentro de la plataforma.     |
| faculty_id      | INTEGER     | FK → faculty.id, NULLABLE              | Facultad a la que pertenece (solo para roles ‘teacher’ y ‘student’). |

**Relaciones:**  
- **N:1** → `faculty` (un usuario puede pertenecer a una sola facultad).  
- **1:N** → `activity` (un usuario puede crear varias actividades).  
- **N:M** → `activity` (un usuario puede participar en muchas actividades, y cada actividad tiene muchos participantes).  
- **1:N** → `comment` (un usuario puede escribir varios comentarios).  
- **1:N** → `response` (un usuario puede responder múltiples preguntas de encuesta).

**Descripción:**  
La tabla **user** centraliza los datos de todos los usuarios de la aplicación: administradores, profesores y estudiantes. Emplea un ENUM para garantizar la consistencia de roles y relaciona opcionalmente al usuario con una facultad.

---

## 3. `activity`

| Columna       | Tipo            | Restricciones                          | Descripción                                                         |
|---------------|-----------------|----------------------------------------|---------------------------------------------------------------------|
| id            | INTEGER         | PK, autoincrement                      | Identificador único de la actividad.                                |
| title         | VARCHAR(150)    | NOT NULL                               | Título descriptivo de la actividad.                                 |
| description   | TEXT            |                                        | Descripción detallada de la actividad.                              |
| date          | DATETIME        | NOT NULL, DEFAULT now()                | Fecha y hora en que se celebra o se creó la actividad.             |
| type          | ENUM            | (‘official’,‘unofficial’), NOT NULL    | Indica si la actividad es oficial de la facultad o privada.        |
| creator_id    | INTEGER         | FK → user.id, NOT NULL                 | Referencia al usuario que creó la actividad.                        |

**Relaciones:**  
- **N:1** → `user` (cada actividad tiene un único creador).  
- **N:M** → `user` (vía tabla intermedia `activity_participants`).  
- **1:N** → `comment` (una actividad puede recibir múltiples comentarios).

**Descripción:**  
La tabla **activity** contiene todas las actividades del sistema, sean oficiales o no, con su metadata básica. El atributo `type` permite filtrar actividades institucionales de las generadas por usuarios.

---

## 4. `activity_participants`

| Columna      | Tipo      | Restricciones                         | Descripción                                                        |
|--------------|-----------|---------------------------------------|--------------------------------------------------------------------|
| activity_id  | INTEGER   | PK, FK → activity.id                  | Actividad en la que participa el usuario.                          |
| user_id      | INTEGER   | PK, FK → user.id                      | Usuario que participa en la actividad.                             |
| joined_at    | DATETIME  | NOT NULL, DEFAULT now()               | Fecha y hora en que el usuario se unió a la actividad.            |

**Descripción:**  
Tabla de asociación N–a–N que vincula usuarios con actividades. Almacenando `joined_at` queda registrado cuándo cada usuario se unió, lo que facilita auditoría y métricas de participación.

---

## 5. `comment`

| Columna       | Tipo       | Restricciones                         | Descripción                                                       |
|---------------|------------|---------------------------------------|-------------------------------------------------------------------|
| id            | INTEGER    | PK, autoincrement                     | Identificador único del comentario.                               |
| content       | TEXT       | NOT NULL                              | Texto del comentario.                                             |
| created_at    | DATETIME   | NOT NULL, DEFAULT now()               | Marca temporal de creación.                                       |
| author_id     | INTEGER    | FK → user.id, NOT NULL                | Usuario que redactó el comentario.                                |
| activity_id   | INTEGER    | FK → activity.id, NOT NULL            | Actividad a la que pertenece el comentario.                       |

**Relaciones:**  
- **N:1** → `user` (cada comentario tiene un autor).  
- **N:1** → `activity` (cada comentario está asociado a una actividad).

**Descripción:**  
La tabla **comment** permite almacenar textos libres asociados a actividades, con referencia clara al autor y momento de creación, facilitando la moderación y el historial de interacción.

---

## 6. `survey`

| Columna       | Tipo          | Restricciones                          | Descripción                                                     |
|---------------|---------------|----------------------------------------|-----------------------------------------------------------------|
| id            | INTEGER       | PK                                     | Identificador único de la encuesta.                            |
| title         | VARCHAR(255)  | NOT NULL                               | Título principal de la encuesta.                               |
| description   | VARCHAR(255)  |                                        | Texto explicativo o instrucción para la encuesta.              |
| editable      | BOOLEAN       | NOT NULL, DEFAULT false                | Indica si un profesor puede modificar preguntas/opciones.      |
| created_at    | DATETIME      | NOT NULL, DEFAULT now()                | Fecha de creación de la encuesta.                              |

**Relaciones:**  
- **1:N** → `question` (una encuesta agrupa varias preguntas).

**Descripción:**  
La tabla **survey** define encuestas, que pueden ser mayoritariamente estáticas (editable=false) o permitir edición limitada por profesores (editable=true), con trazabilidad de su fecha de creación.

---

## 7. `question`

| Columna         | Tipo           | Restricciones                         | Descripción                                                       |
|-----------------|----------------|---------------------------------------|-------------------------------------------------------------------|
| id              | INTEGER        | PK                                    | Identificador único de la pregunta.                              |
| survey_id       | INTEGER        | FK → survey.id, NOT NULL              | Encuesta a la que pertenece la pregunta.                         |
| question_text   | VARCHAR(255)   | NOT NULL                              | Texto de la pregunta.                                            |

**Relaciones:**  
- **N:1** → `survey`  
- **1:N** → `choice`  
- **1:N** → `response`

**Descripción:**  
La tabla **question** recoge cada una de las preguntas que conforman una encuesta, vinculada directamente a su encuesta padre.

---

## 8. `choice`

| Columna        | Tipo           | Restricciones                         | Descripción                                                      |
|----------------|----------------|---------------------------------------|------------------------------------------------------------------|
| id             | INTEGER        | PK                                     | Identificador único de la opción.                                |
| question_id    | INTEGER        | FK → question.id, NOT NULL             | Pregunta a la que pertenece esta opción.                         |
| choice_text    | VARCHAR(255)   | NOT NULL                               | Texto de la opción de respuesta.                                 |

**Relaciones:**  
- **N:1** → `question`  
- **1:N** → `response`

**Descripción:**  
La tabla **choice** almacena cada opción de respuesta posible para una pregunta de encuesta. Esto permite preguntas de selección única.

---

## 9. `response`

| Columna        | Tipo       | Restricciones                          | Descripción                                                      |
|----------------|------------|----------------------------------------|------------------------------------------------------------------|
| id             | INTEGER    | PK                                     | Identificador único de la respuesta.                            |
| user_id        | INTEGER    | FK → user.id, NOT NULL                 | Usuario que responde.                                            |
| question_id    | INTEGER    | FK → question.id, NOT NULL             | Pregunta contestada.                                             |
| choice_id      | INTEGER    | FK → choice.id, NOT NULL               | Opción elegida por el usuario.                                   |
| answered_at    | DATETIME   | NOT NULL, DEFAULT now()                | Fecha y hora en que se remitió la respuesta.                     |

**Relaciones:**  
- **N:1** → `user`  
- **N:1** → `question`  
- **N:1** → `choice`

**Descripción:**  
La tabla **response** registra cada voto o selección hecha por un usuario en una encuesta, lo que permite análisis de resultados y trazabilidad de respuestas.

---

### Consideraciones finales

- **Integridad referencial**: Todas las claves foráneas refuerzan la consistencia de los datos.  
- **Enums**: Facilitan el mantenimiento y evitan valores arbitrarios.  
- **Tablas intermedias**: Permiten enriquecer relaciones N–a–N con metadatos (ej. fecha de unión).  
- **Timestamps**: Quedan registradas fechas de creación y modificación para auditoría.  