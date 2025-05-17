CREATE SCHEMA `oxxo` DEFAULT CHARACTER SET utf8mb4;
USE `oxxo`;

CREATE TABLE `proveedores` (
  `nombre` VARCHAR(100) NOT NULL,
  `contacto` VARCHAR(50) DEFAULT NULL,
  `telefono` VARCHAR(20) DEFAULT NULL,
  `email` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `categorias` (
  `id_categoria` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `articulos` (
  `id_articulo` VARCHAR(13) NOT NULL,
  `nombre` VARCHAR(100) NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `stock` INT(11) DEFAULT 0,
  `proveedores_nombre` VARCHAR(100) DEFAULT NULL,
  `categorias_id_categoria` INT(11) DEFAULT NULL,
  PRIMARY KEY (`id_articulo`),
  INDEX (`proveedores_nombre`),
  INDEX (`categorias_id_categoria`),
  CONSTRAINT `articulos_fk_proveedor` FOREIGN KEY (`proveedores_nombre`) REFERENCES `proveedores` (`nombre`),
  CONSTRAINT `articulos_fk_categoria` FOREIGN KEY (`categorias_id_categoria`) REFERENCES `categorias` (`id_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `empleados` (
  `id_empleado` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `puesto` ENUM('gerente', 'cajero', 'almacen') NOT NULL,
  `fecha_contratacion` DATE NOT NULL,
  `sueldo` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_empleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `cajas` (
  `id_caja` INT(11) NOT NULL AUTO_INCREMENT,
  `numero_caja` INT(11) NOT NULL,
  `estado` ENUM('activa', 'inactiva', 'mantenimiento') DEFAULT 'activa',
  `empleados_id_empleado` INT(11) NOT NULL,
  PRIMARY KEY (`id_caja`),
  UNIQUE INDEX `numero_caja` (`numero_caja`),
  INDEX `fk_cajas_empleados1_idx` (`empleados_id_empleado`),
  CONSTRAINT `fk_cajas_empleados1` FOREIGN KEY (`empleados_id_empleado`) REFERENCES `empleados` (`id_empleado`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `clientes` (
  `telefono` VARCHAR(20) NOT NULL,
  `nombre` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) DEFAULT NULL,
  `puntos` INT(11) DEFAULT 0,
  PRIMARY KEY (`telefono`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `pedidos` (
  `id_pedido` INT(11) NOT NULL AUTO_INCREMENT,
  `fecha_pedido` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` ENUM('Pendiente', 'Enviado', 'Recibido', 'Cancelado') DEFAULT 'Pendiente',
  `proveedores_nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_pedido`),
  INDEX (`proveedores_nombre`),
  CONSTRAINT `pedidos_fk_proveedor` FOREIGN KEY (`proveedores_nombre`) REFERENCES `proveedores` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `detalle_pedidos` (
  `id_detalle_pedido` INT(11) NOT NULL AUTO_INCREMENT,
  `pedidos_id_pedido` INT(11) NOT NULL,
  `articulos_id_articulo` VARCHAR(13) NOT NULL,
  `cantidad` INT(11) NOT NULL,
  `precio_unitario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_detalle_pedido`),
  INDEX (`pedidos_id_pedido`),
  INDEX (`articulos_id_articulo`),
  CONSTRAINT `detalle_pedidos_fk_pedido` FOREIGN KEY (`pedidos_id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  CONSTRAINT `detalle_pedidos_fk_articulo` FOREIGN KEY (`articulos_id_articulo`) REFERENCES `articulos` (`id_articulo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ventas` (
  `id_venta` INT(11) NOT NULL AUTO_INCREMENT,
  `fecha` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` DECIMAL(10,2) NOT NULL,
  `cajas_id_caja` INT(11) NOT NULL,
  `clientes_telefono` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX (`cajas_id_caja`),
  INDEX (`clientes_telefono`),
  CONSTRAINT `ventas_fk_caja` FOREIGN KEY (`cajas_id_caja`) REFERENCES `cajas` (`id_caja`),
  CONSTRAINT `ventas_fk_cliente` FOREIGN KEY (`clientes_telefono`) REFERENCES `clientes` (`telefono`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `detalles_venta` (
  `id_detalle` INT(11) NOT NULL AUTO_INCREMENT,
  `cantidad` INT(11) NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  `ventas_id_venta` INT(11) NOT NULL,
  `ventas_empleados_id_empleado` INT(11) NOT NULL,
  `ventas_clientes_telefono` VARCHAR(20) NOT NULL,
  `articulos_id_articulo` VARCHAR(13) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  INDEX (`ventas_id_venta`, `ventas_empleados_id_empleado`, `ventas_clientes_telefono`),
  INDEX (`articulos_id_articulo`),
  CONSTRAINT `detalles_venta_fk_venta` FOREIGN KEY (`ventas_id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `detalles_venta_fk_articulo` FOREIGN KEY (`articulos_id_articulo`) REFERENCES `articulos` (`id_articulo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `inventario` (
  `id_inventario` INT(11) NOT NULL AUTO_INCREMENT,
  `articulos_id_articulo` VARCHAR(13) NOT NULL,
  `cantidad_tienda` INT(11) DEFAULT 0,
  `cantidad_almacen` INT(11) DEFAULT 0,
  `ultima_actualizacion` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_inventario`),
  INDEX (`articulos_id_articulo`),
  CONSTRAINT `inventario_fk_articulo` FOREIGN KEY (`articulos_id_articulo`) REFERENCES `articulos` (`id_articulo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO proveedores (nombre, contacto, telefono, email) VALUES
('Nestle', 'Ana Gómez', '55-1234-5678', 'ana.gomez@nestle.com.mx'),
('Holanda', 'Luis Pérez', '55-2345-6789', 'luis.perez@holanda.com.mx'),
('Rincón Tarasco', 'María Sánchez', '55-3456-7890', 'maria.sanchez@rincontarasco.com.mx'),
('Topo Chico', 'Carlos Ruiz', '55-4567-8901', 'carlos.ruiz@topochico.com.mx'),
('Chiloka', 'Laura Fernández', '55-5678-9012', 'laura.fernandez@chiloka.com.mx'),
('Quaker', 'Jorge Martínez', '55-6789-0123', 'jorge.martinez@quaker.com.mx'),
('Grupo Modelo', 'Patricia López', '55-7890-1234', 'patricia.lopez@grupomodelo.com.mx'),
('Coca-Cola FEMSA', 'Ricardo Torres', '55-8901-2345', 'ricardo.torres@coca-colafemsa.com.mx'),
('Charras', 'Sandra Díaz', '55-9012-3456', 'sandra.diaz@charras.com.mx'),
('Gamesa', 'Miguel Herrera', '55-0123-4567', 'miguel.herrera@gamesa.com.mx');

INSERT INTO categorias (nombre) VALUES
('Bebidas'),
('Snacks'),
('Helados'),
('Botanas');

INSERT INTO articulos (id_articulo, nombre, precio, stock, proveedores_nombre, categorias_id_categoria) VALUES
('7506390202039', 'Paleta Carlos V', 19.50, 50, 'Nestle', 3),
('7506390201926', 'Paleta Nes Limon', 30.00, 30, 'Nestle', 3),
('7506390202213', 'Paleta Lapiz 48gr', 20.50, 25, 'Nestle', 3),
('7506306417502', 'Magnum Sunlight 90m', 43.00, 40, 'Holanda', 3),
('7506306418066', 'Mag Ch C Remix 85ml', 43.00, 20, 'Holanda', 3),
('7506306415010', 'Magnum Praliné 90ml', 43.00, 35, 'Holanda', 3),
('7501364502047', 'Toto.Rincon 280gr', 28.50, 15, 'Rincón Tarasco', 4),
('7501055373055', 'Topo Chico Hard Seltzer Piña 355ml', 15.00, 40, 'Topo Chico', 1),
('7501055373062', 'Topo Chico Hard Seltzer Limón 355ml', 15.00, 35, 'Topo Chico', 1),
('7503023741002', 'Chiloka Tamarindo 40g', 5.00, 50, 'Chiloka', 2),
('7501761850956', 'Cereal Quaker Avena Flakes 220g', 25.00, 20, 'Quaker', 2),
('7501761850925', 'Cereal Quaker Stars Malvaviscos 170g', 22.00, 18, 'Quaker', 2),
('7501058612908', 'Cerveza Corona 355ml', 18.00, 80, 'Grupo Modelo', 1),
('7501064191453', 'Cerveza Victoria 355ml', 17.50, 60, 'Grupo Modelo', 1),
('7501064191422', 'Cerveza Modelo Especial 355ml', 19.00, 60, 'Grupo Modelo', 1),
('7501020510104', 'Refresco Coca-Cola 600ml', 17.00, 100, 'Coca-Cola FEMSA', 1),
('7501031315200', 'Refresco Sprite 600ml', 17.00, 70, 'Coca-Cola FEMSA', 1),
('7501020520615', 'Refresco Fanta Naranja 600ml', 17.00, 60, 'Coca-Cola FEMSA', 1),
('7501009517435', 'Tostadas Charras 300g', 27.00, 20, 'Charras', 4),
('7501009517428', 'Tostadas Charras Maíz 200g', 20.00, 25, 'Charras', 4),
('7501022626448', 'Galleta Emperador Chocolate', 12.50, 50, 'Gamesa', 2),
('7501021100143', 'Galleta Marias 170g', 12.00, 60, 'Gamesa', 2);

