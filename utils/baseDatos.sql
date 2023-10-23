CREATE DATABASE tramos_yungas;

USE tramos_yungas;

-- CREANDO TABLAS

CREATE TABLE municipio(
    id_municipio INT NOT NULL,
    nombre VARCHAR(30),
    ubicacion VARCHAR(50)
);

ALTER TABLE municipio
    ADD PRIMARY KEY (id_municipio);

ALTER TABLE municipio
    MODIFY id_municipio INT NOT NULL AUTO_INCREMENT;


CREATE TABLE sindicato(
    id_sindicato INT NOT NULL,
    nombre VARCHAR(50),
    ubicacion VARCHAR(50),
    id_municipio INT NOT NULL,
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
);

ALTER TABLE sindicato
    ADD PRIMARY KEY (id_sindicato);

ALTER TABLE sindicato
    MODIFY id_sindicato INT NOT NULL AUTO_INCREMENT;

CREATE TABLE persona(
    ci INT NOT NULL,
    nombre VARCHAR(50),
    telefono INT,
    rol_sindicato VARCHAR(30),
    id_sindicato INT NOT NULL,
    FOREIGN KEY (id_sindicato) REFERENCES sindicato(id_sindicato)
);

ALTER TABLE persona
    ADD PRIMARY KEY (ci);

CREATE TABLE usuarios(
    id_usuario INT NOT NULL,
    nombre_usuario VARCHAR(30),
    contrasena VARCHAR(50),
    rol_usuario INT,
    ci_usuario INT NOT NULL,
    FOREIGN KEY (ci_usuario) REFERENCES persona(ci)
);

ALTER TABLE usuarios
    ADD PRIMARY KEY (id_usuario);

ALTER TABLE usuarios
    MODIFY id_usuario INT NOT NULL AUTO_INCREMENT;

CREATE TABLE autos(
    id_auto INT NOT NULL,
    placa VARCHAR(8),
    tiempo_cambio_llanta INT,
    marca VARCHAR(20),
    color VARCHAR(20),
    id_chofer INT NOT NULL,
    FOREIGN KEY (id_chofer) REFERENCES usuarios(id_usuario)
);

ALTER TABLE autos
    ADD PRIMARY KEY (id_auto);

ALTER TABLE autos
    MODIFY id_auto INT NOT NULL AUTO_INCREMENT;

CREATE TABLE telefonos_sindicato(
    id_telefono INT NOT NULL,
    numero_telefono INT,
    id_sindicato INT NOT NULL,
    propietario VARCHAR(50),
    FOREIGN KEY (id_sindicato) REFERENCES sindicato(id_sindicato)
);

ALTER TABLE telefonos_sindicato
    ADD PRIMARY KEY (id_telefono);

ALTER TABLE telefonos_sindicato
    MODIFY id_telefono INT NOT NULL AUTO_INCREMENT;

CREATE TABLE telefonos_municipio(
    id_telefono_m INT NOT NULL,
    numero_telefono INT,
    id_municipio INT NOT NULL,
    propietario VARCHAR(50),
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
);

ALTER TABLE telefonos_municipio
    ADD PRIMARY KEY (id_telefono_m);

ALTER TABLE telefonos_municipio
    MODIFY id_telefono_m INT NOT NULL AUTO_INCREMENT;

CREATE TABLE tramos(
    id_tramo INT NOT NULL,
    km_inicio VARCHAR(50),
    km_final VARCHAR(50),
    zona_riesgosa INT,
    tiempo_ida INT,
    señal_internet INT,
    señal_normal INT,
    id_municipio INT NOT NULL
    -- FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
);

ALTER TABLE tramos
    ADD PRIMARY KEY (id_tramo);

ALTER TABLE tramos
    MODIFY id_tramo INT NOT NULL AUTO_INCREMENT;

CREATE TABLE nivel_alerta(
    id_alerta INT NOT NULL,
    descripcion VARCHAR(50)
);

ALTER TABLE nivel_alerta
    ADD PRIMARY KEY (id_alerta);

ALTER TABLE nivel_alerta
    MODIFY id_alerta INT NOT NULL AUTO_INCREMENT;

-- LA TABLA VIAJES ES DINAMICA, CAMBIA CONFORME AVANZA EL TIEMPO

CREATE TABLE viajes(
    id_viaje INT NOT NULL,
    origen VARCHAR(20),
    destino VARCHAR(20),
    fecha_viaje DATE,
    hora_inicio DATETIME,
    hora_final DATETIME,
    estado_viaje VARCHAR(20),
    ultima_ubicacion VARCHAR(50),
    hora_ultimo DATETIME,
    id_auto_viaje INT NOT NULL,
    pasajeros INT NOT NULL,
    id_tramo_viaje INT NOT NULL,
    id_nivel_alerta INT NOT NULL,
    estado_emb VARCHAR(20),
    FOREIGN KEY (id_auto_viaje) REFERENCES autos(id_auto),
    FOREIGN KEY (id_tramo_viaje) REFERENCES tramos(id_tramo),
    FOREIGN KEY (id_nivel_alerta) REFERENCES nivel_alerta(id_alerta)
);

ALTER TABLE viajes
    ADD PRIMARY KEY (id_viaje);

ALTER TABLE viajes
    MODIFY id_viaje INT NOT NULL AUTO_INCREMENT;

CREATE TABLE alertas_registradas(
    id_registro INT NOT NULL,
    alerta_registrada INT NOT NULL,
    id_viaje_alerta INT NOT NULL,
    FOREIGN KEY (id_viaje_alerta) REFERENCES viajes(id_viaje)
);

ALTER TABLE alertas_registradas
    ADD PRIMARY KEY (id_registro);

ALTER TABLE alertas_registradas
    MODIFY id_registro INT NOT NULL AUTO_INCREMENT;