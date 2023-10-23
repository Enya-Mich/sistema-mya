USE tramos_yungas;

INSERT INTO municipio (`nombre`,`ubicacion`) VALUES ('Terminal Minasa', '-16.1651,-40.65416'),
('Tranca', '-16.1651,-40.65416'),
('Velo de la novia', '-16.1651,-40.65416'),
('Unduavi', '-16.1651,-40.65416'),
('Irupana', '-16.1651,-40.65416');

INSERT INTO sindicato (`nombre`,`ubicacion`, `id_municipio`) VALUES ('TUNKI TOURS', '-16.1651,-40.65416', 1),
('Trans irupana', '-16.1651,-40.65416', 1),
('Trans arenas', '-16.1651,-40.65416', 5);

INSERT INTO persona (`ci`,`nombre`,`telefono`, `rol_sindicato`,`id_sindicato`) VALUES (9912007, 'Michelle Vargas', 77251751, 'Super administradora', 1),
(9912008, 'Juan Perez', 77251752, 'Secretario', 1),
(9912009, 'Pepe Perez', 77251753, 'Jefe de sindicato', 1),
(9912010, 'Jose Gonzales', 77251754, 'Conductor', 1),
(9912011, 'Luisa Lopez', 77251755, 'Conductor', 1),
(9912012, 'William Wallas', 77251756, 'Conductor', 1),
(9912013, 'Jose Feliciano', 77251757, 'Conductor', 1);

-- rol 1 es administrador
-- rol 2 es usuario comubn o conductor

INSERT INTO usuarios (`nombre_usuario`,`contrasena`, `rol_usuario`,`ci_usuario`) VALUES ('michellevargas', 'administrador', 1, 9912007),
('juanperez', 'administrador', 2, 9912008),
('pepeperez', 'administrador', 2, 9912009),
('josegonzales', 'conductor1', 3, 9912010),
('luisalopez', 'conductor2', 3, 9912011),
('willianwallas', 'conductor3', 3, 9912012),
('josefeliciano', 'conductor4', 3, 9912013);

INSERT INTO autos (`placa`,`tiempo_cambio_llanta`, `marca`,`color`,`id_chofer`) VALUES ('210HCK', 15, 'LADA', 'Beige', 4),
('211HTK', 5, 'TOYOTA', 'Blanco', 5),
('456GRRK', 10, 'NISSAN', 'Negro', 6),
('784PEL', 8, 'KEYTON', 'Azul', 7);


INSERT INTO nivel_alerta (`descripcion`) VALUES ('Alerta baja, posible fallo mecanico'),
('Alerta media, Posible embarrancamiento'),
('Alerta Alta, embarrancamiento');

-- ZONA RIESGOSA: 1 MUY BAJA, 2 BAJA, 3 MEDIA, 4 ALTA, 5 MUY ALTA
-- SEÑAL INTERNET: 1 HAY SEÑAL, 2 NO HAY SEÑAL
-- SEÑAL NORMAL, SEÑAL DE TELEFONIA NORMAL: 1 HAY SEÑAL, 2 NO HAY SEÑAL

INSERT INTO tramos (`id_tramo`,`km_inicio`,`km_final`, `zona_riesgosa`,`tiempo_ida`,`señal_internet`,`señal_normal`,`id_municipio`) VALUES
(1,'-16.469049472495275;-68.11605575655983', '-16.350058724719574;-68.0403933224296', 3, 28, 2, 1, 1),
(2,'-16.350058724719574;-68.0403933224296', '-16.327407122887553;-67.95503898847265', 5, 18, 2, 1, 1),
(3,'-16.327407122887553;-67.95503898847265', '-16.323726669715715;-67.8260676361114', 5, 44, 2, 1, 1),
(4,'-16.323726669715715;-67.8260676361114', '-16.400028278131167;-67.71950883630169', 5, 30, 2, 1, 1),
(5,'-16.400028278131167;-67.71950883630169', '-16.401757380663387;-67.64447135595758', 5, 20, 2, 1, 1),
(6,'-16.401757380663387;-67.64447135595758', '-16.37379355606211;-67.58384238148729', 5, 27, 2, 1, 1),
(7,'-16.37379355606211;-67.58384238148729', '-16.380675956463296;-67.53964877102905', 4, 24, 2, 1, 1),
(8,'-16.380675956463296;-67.53964877102905', '-16.396560648229226;-67.4787238654091', 5, 27, 2, 1, 1),
(9,'-16.396560648229226;-67.4787238654091', '-16.428441272715645;-67.4674779353273', 5, 10, 2, 1, 1),
(10,'-16.428441272715645;-67.4674779353273', '-16.473003;-67.453236', 5, 27, 2, 1, 1);
