from app.extensions import db


class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'), nullable=False)

    usuario = db.relationship("Usuario", back_populates="estudiante")
    profesor = db.relationship("Profesor", back_populates="estudiantes")

class Profesor(db.Model):
    __tablename__ = 'profesor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_departamento = db.Column(db.Integer, db.ForeignKey('jefe_departamento.id'), nullable=False)

    usuario = db.relationship("Usuario", back_populates="profesor", uselist=False)
    estudiantes = db.relationship("Estudiante", back_populates="profesor")
    jefe_departamento = db.relationship("JefeDepartamento", back_populates="profesores")

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    usuario = db.relationship("Usuario", back_populates="administrador", uselist=False)

class JefeDepartamento(db.Model):
    __tablename__ = 'jefe_departamento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    usuario = db.relationship("Usuario", back_populates="jefe_departamento", uselist=False)
    profesores = db.relationship("Profesor", back_populates="jefe_departamento")
    
    