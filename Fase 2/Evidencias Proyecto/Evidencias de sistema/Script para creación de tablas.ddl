-- Generado por Oracle SQL Developer Data Modeler 19.2.0.182.1216
--   en:        2024-11-27 21:23:08 CLST
--   sitio:      Oracle Database 11g
--   tipo:      Oracle Database 11g



CREATE TABLE anotaciones (
    anot_id              INTEGER NOT NULL,
    anot_titulo          VARCHAR2(100) NOT NULL,
    anot_descripcion     VARCHAR2(255) NOT NULL,
    anot_fechacreacion   DATE NOT NULL,
    anot_pepe_id         INTEGER NOT NULL,
    anot_curs_id         INTEGER NOT NULL,
    anot_asig_id         INTEGER NOT NULL,
    anot_anot_t_id       INTEGER NOT NULL
);

ALTER TABLE anotaciones ADD CONSTRAINT anotaciones_pk PRIMARY KEY ( anot_id );

CREATE TABLE anotaciones_tipo (
    anot_t_id       INTEGER NOT NULL,
    anot_t_nombre   VARCHAR2(50) NOT NULL
);

ALTER TABLE anotaciones_tipo ADD CONSTRAINT anotaciones_tipo_pk PRIMARY KEY ( anot_t_id );

CREATE TABLE asignatura (
    asi_id        INTEGER NOT NULL,
    asi_nombre    VARCHAR2(50) NOT NULL,
    asi_curs_id   INTEGER NOT NULL
);

ALTER TABLE asignatura ADD CONSTRAINT asignatura_pk PRIMARY KEY ( asi_id );

CREATE TABLE asistencias (
    asis_id                         INTEGER NOT NULL,
    asis_fecha                      DATE NOT NULL,
    asis_sino_presentacertificado   INTEGER NOT NULL,
    asis_sino_presente              INTEGER NOT NULL,
    asis_curs_id                    INTEGER NOT NULL,
    asis_pepe_id                    INTEGER NOT NULL
);

ALTER TABLE asistencias ADD CONSTRAINT asistencias_pk PRIMARY KEY ( asis_id );

CREATE TABLE comunas (
    comu_id        INTEGER NOT NULL,
    comu_nombre    VARCHAR2(30) NOT NULL,
    comu_regi_id   INTEGER NOT NULL
);

ALTER TABLE comunas ADD CONSTRAINT comunas_pk PRIMARY KEY ( comu_id );

CREATE TABLE cursos (
    curs_id       INTEGER NOT NULL,
    curs_nombre   VARCHAR2(20) NOT NULL,
    curs_sala     INTEGER NOT NULL,
    curs_anno     INTEGER NOT NULL
);

ALTER TABLE cursos ADD CONSTRAINT cursos_pk PRIMARY KEY ( curs_id );

CREATE TABLE notas (
    nota_id              INTEGER NOT NULL,
    nota_valor           NUMBER(3, 1) NOT NULL,
    nota_fechacreacion   DATE NOT NULL,
    nota_descripcion     CLOB,
    nota_pepe_alumno     INTEGER NOT NULL,
    nota_curs_id         INTEGER NOT NULL
);

ALTER TABLE notas ADD CONSTRAINT notas_pk PRIMARY KEY ( nota_id );

CREATE TABLE perfiles (
    perf_id       INTEGER NOT NULL,
    perf_nombre   INTEGER NOT NULL
);

ALTER TABLE perfiles ADD CONSTRAINT perfiles_pk PRIMARY KEY ( perf_id );

CREATE TABLE personas (
    pers_id               INTEGER NOT NULL,
    pers_nombrecompleto   VARCHAR2(60) NOT NULL,
    pers_appat            VARCHAR2(40) NOT NULL,
    pers_apmat            VARCHAR2(40) NOT NULL,
    pers_correo           VARCHAR2(30) NOT NULL,
    pers_contrasena       VARCHAR2(128) NOT NULL,
    pers_fechanac         DATE NOT NULL,
    pers_rut              VARCHAR2(9) NOT NULL,
    pers_telefono         VARCHAR2(14) NOT NULL,
    pers_direccion        VARCHAR2(40) NOT NULL,
    pers_comu_id          INTEGER NOT NULL
);

ALTER TABLE personas ADD CONSTRAINT personas_pk PRIMARY KEY ( pers_id );

CREATE TABLE personas_perfiles (
    pepe_id                 INTEGER NOT NULL,
    pepe_fechadecreacion    DATE NOT NULL,
    pepe_pers_id            INTEGER NOT NULL,
    pepe_perf_id            INTEGER NOT NULL,
    pepe_curs_id            INTEGER NOT NULL,
    pepe_pepe_responsable   INTEGER,
    pepe_sino_activo        INTEGER NOT NULL
);

ALTER TABLE personas_perfiles ADD CONSTRAINT personas_perfiles_pk PRIMARY KEY ( pepe_id );

CREATE TABLE publicaciones (
    publ_id              INTEGER NOT NULL,
    publ_titulo          VARCHAR2(30) NOT NULL,
    publ_descripcion     CLOB NOT NULL,
    publ_fechacreacion   DATE NOT NULL,
    publ_sino_estado     INTEGER NOT NULL,
    publ_puti_id         INTEGER NOT NULL,
    publ_pepe_autor      INTEGER NOT NULL
);

ALTER TABLE publicaciones ADD CONSTRAINT publicaciones_pk PRIMARY KEY ( publ_id );

CREATE TABLE publicaciones_comentarios (
    puco_id              INTEGER NOT NULL,
    puco_comentario      CLOB NOT NULL,
    puco_fechacreacion   DATE NOT NULL,
    puco_sino_estado     INTEGER NOT NULL,
    puco_publ_id         INTEGER NOT NULL,
    puco_pepe_autor      INTEGER NOT NULL
);

ALTER TABLE publicaciones_comentarios ADD CONSTRAINT publicaciones_comentarios_pk PRIMARY KEY ( puco_id );

CREATE TABLE publicaciones_tipos (
    puti_id            INTEGER NOT NULL,
    puti_nombre        VARCHAR2(30) NOT NULL,
    puti_sino_estado   INTEGER NOT NULL
);

ALTER TABLE publicaciones_tipos ADD CONSTRAINT publicaciones_tipos_pk PRIMARY KEY ( puti_id );

CREATE TABLE regiones (
    regi_id       INTEGER NOT NULL,
    regi_nombre   VARCHAR2(30) NOT NULL
);

ALTER TABLE regiones ADD CONSTRAINT regiones_pk PRIMARY KEY ( regi_id );

CREATE TABLE sino (
    sino_id       INTEGER NOT NULL,
    sino_nombre   VARCHAR2(30) NOT NULL,
    sino_estado   VARCHAR2(30) NOT NULL
);

ALTER TABLE sino ADD CONSTRAINT sino_pk PRIMARY KEY ( sino_id );

ALTER TABLE anotaciones
    ADD CONSTRAINT anotaciones_asignatura_fk FOREIGN KEY ( anot_asig_id )
        REFERENCES asignatura ( asi_id );

ALTER TABLE anotaciones
    ADD CONSTRAINT anotaciones_cursos_fk FOREIGN KEY ( anot_curs_id )
        REFERENCES cursos ( curs_id );

ALTER TABLE anotaciones
    ADD CONSTRAINT anotaciones_personask FOREIGN KEY ( anot_pepe_id )
        REFERENCES personas_perfiles ( pepe_id );

ALTER TABLE anotaciones
    ADD CONSTRAINT anotaciones_tipo_fk FOREIGN KEY ( anot_anot_t_id )
        REFERENCES anotaciones_tipo ( anot_t_id );

ALTER TABLE asignatura
    ADD CONSTRAINT asignatura_cursos_fk FOREIGN KEY ( asi_curs_id )
        REFERENCES cursos ( curs_id );

ALTER TABLE asistencias
    ADD CONSTRAINT asistencias_cursos_fk FOREIGN KEY ( asis_curs_id )
        REFERENCES cursos ( curs_id );

ALTER TABLE asistencias
    ADD CONSTRAINT asistencias_persona_fk FOREIGN KEY ( asis_pepe_id )
        REFERENCES personas_perfiles ( pepe_id );

ALTER TABLE asistencias
    ADD CONSTRAINT asistencias_sino_fk FOREIGN KEY ( asis_sino_presentacertificado )
        REFERENCES sino ( sino_id );

ALTER TABLE asistencias
    ADD CONSTRAINT asistencias_sino_fkv2 FOREIGN KEY ( asis_sino_presente )
        REFERENCES sino ( sino_id );

ALTER TABLE comunas
    ADD CONSTRAINT comunas_regiones_fk FOREIGN KEY ( comu_regi_id )
        REFERENCES regiones ( regi_id );

ALTER TABLE notas
    ADD CONSTRAINT notas_cursos_fk FOREIGN KEY ( nota_curs_id )
        REFERENCES cursos ( curs_id );

ALTER TABLE notas
    ADD CONSTRAINT notas_personas_fk FOREIGN KEY ( nota_pepe_alumno )
        REFERENCES personas_perfiles ( pepe_id );

ALTER TABLE personas
    ADD CONSTRAINT personas_comunas_fk FOREIGN KEY ( pers_comu_id )
        REFERENCES comunas ( comu_id );

ALTER TABLE personas_perfiles
    ADD CONSTRAINT personas_perfiles_cursos_fk FOREIGN KEY ( pepe_curs_id )
        REFERENCES cursos ( curs_id );

ALTER TABLE personas_perfiles
    ADD CONSTRAINT personas_perfiles_fk FOREIGN KEY ( pepe_pepe_responsable )
        REFERENCES personas_perfiles ( pepe_id );

ALTER TABLE personas_perfiles
    ADD CONSTRAINT personas_perfiles_perfiles_fk FOREIGN KEY ( pepe_perf_id )
        REFERENCES perfiles ( perf_id );

ALTER TABLE personas_perfiles
    ADD CONSTRAINT personas_perfiles_personas_fk FOREIGN KEY ( pepe_pers_id )
        REFERENCES personas ( pers_id );

ALTER TABLE personas_perfiles
    ADD CONSTRAINT personas_perfiles_sino_fk FOREIGN KEY ( pepe_sino_activo )
        REFERENCES sino ( sino_id );

ALTER TABLE publicaciones_comentarios
    ADD CONSTRAINT publicaciones_comentariofk FOREIGN KEY ( puco_pepe_autor )
        REFERENCES personas_perfiles ( pepe_id );

ALTER TABLE publicaciones_comentarios
    ADD CONSTRAINT publicaciones_comentarios_fk FOREIGN KEY ( puco_publ_id )
        REFERENCES publicaciones ( publ_id );

ALTER TABLE publicaciones
    ADD CONSTRAINT publicaciones_personas_fk FOREIGN KEY ( publ_pepe_autor )
        REFERENCES personas_perfiles ( pepe_id );

ALTER TABLE publicaciones
    ADD CONSTRAINT publicaciones_publicaciones_fk FOREIGN KEY ( publ_puti_id )
        REFERENCES publicaciones_tipos ( puti_id );

ALTER TABLE publicaciones
    ADD CONSTRAINT publicaciones_sino_fk FOREIGN KEY ( publ_sino_estado )
        REFERENCES sino ( sino_id );

ALTER TABLE publicaciones_comentarios
    ADD CONSTRAINT publicaciones_sino_fkv2 FOREIGN KEY ( puco_sino_estado )
        REFERENCES sino ( sino_id );

ALTER TABLE publicaciones_tipos
    ADD CONSTRAINT publicaciones_tipos_sino_fk FOREIGN KEY ( puti_sino_estado )
        REFERENCES sino ( sino_id );



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            15
-- CREATE INDEX                             0
-- ALTER TABLE                             40
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
