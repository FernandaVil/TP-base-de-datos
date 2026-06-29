-- ===============================================================================================================
-- 1. Vigencia de promociones: La fecha de creación del pedido debe estar comprendida obligatoriamente 
-- dentro del rango de vigencia (fecha de inicio y fecha de fin) de la promoción que tiene aplicada.
-- ===============================================================================================================
SELECT pe.id_pedido, pe.id_promocion, pe.fecha_hora_creacion, pr.fecha_inicio, pr.fecha_fin
FROM pedido pe
	JOIN promocion pr
	ON pe.id_promocion = pr.id_promocion
WHERE NOT(pe.fecha_hora_creacion >= pr.fecha_inicio AND 
			pe.fecha_hora_creacion <= pr.fecha_fin)
;
-- FAIL. Hay 16 pedidos con fecha del 2026-06-24 en el que no se cumple la consistencia.

-- ===============================================================================================================
-- 2. Cronología del historial: La fecha y hora de cualquier registro en el historial de estados debe ser 
-- estrictamente posterior (o igual) a la fecha y hora de creación del pedido asociado en la tabla principal.
-- ===============================================================================================================
SELECT pe.id_pedido, pe.fecha_hora_creacion, h.estado, h.fecha_hora
FROM pedido pe
	JOIN historial_estado_pedido h
	ON pe.id_pedido = h.id_pedido
WHERE pe.fecha_hora_creacion > h.fecha_hora
;
-- OK

-- ===============================================================================================================
-- 3. Consistencia financiera: El monto total abonado en la cabecera del pedido debe coincidir exactamente con la 
-- sumatoria del precio unitario por la cantidad de todos sus ítems en el detalle, restando el porcentaje de 
-- descuento si existe una promoción aplicada.
-- ===============================================================================================================
WITH aplicar_desc AS(
	SELECT dp.id_pedido,
		SUM(precio_unitario_historico * cantidad * (1.0 - COALESCE(pr.porcentaje_descuento,0)*0.01))
			AS total_con_desc
	FROM detalle_pedido dp
		JOIN pedido pe
		ON dp.id_pedido = pe.id_pedido
		LEFT JOIN promocion pr
		ON pe.id_promocion = pr.id_promocion
	GROUP BY dp.id_pedido
)
SELECT pe.id_pedido, pe.total_abonado, ad.total_con_desc
FROM pedido pe
	JOIN aplicar_desc ad
	ON pe.id_pedido = ad.id_pedido
WHERE pe.total_abonado != ROUND(ad.total_con_desc,2)
;
-- OK

-- ===============================================================================================================
-- 4. Unicidad de estados por pedido: Para un mismo identificador de pedido, no pueden existir dos registros con 
-- el mismo estado en el historial (no se puede pasar a 'en_preparacion' dos veces).
-- ===============================================================================================================
SELECT id_pedido, estado, COUNT(*)
FROM historial_estado_pedido
GROUP BY id_pedido, estado
HAVING COUNT(*)>1
;
-- OK

-- ===============================================================================================================
-- 5. Cronología de usuarios: La fecha de creación de un pedido debe ser posterior a la fecha de registro en la 
-- plataforma del usuario que lo realizó.
-- ===============================================================================================================
SELECT pe.id_pedido, u.id_usuario, u.fecha_registro, pe.fecha_hora_creacion
FROM pedido pe
	JOIN usuario u
	ON pe.id_usuario = u.id_usuario
WHERE pe.fecha_hora_creacion::date < u.fecha_registro
;
-- OK

-- ===============================================================================================================
-- 6. Integridad del catálogo: Todos los platos registrados en el detalle de un pedido deben pertenecer de manera 
-- estricta al identificador del restaurante registrado en la cabecera del pedido.
-- ===============================================================================================================
SELECT pe.id_pedido, p.id_plato, p.id_restaurante AS restaurante_del_plato,
	pe.id_restaurante AS restaurante_del_pedido
FROM pedido pe
	JOIN detalle_pedido dp
	ON pe.id_pedido = dp.id_pedido
	JOIN plato p
	ON dp.id_plato = p.id_plato
WHERE pe.id_restaurante != p.id_restaurante
;
-- OK

-- ===============================================================================================================
-- 7. Consistencia logística: Todo pedido que posea un registro de estado 'en_camino' o 'entregado' en su 
-- historial debe tener un identificador de repartidor asignado (no nulo)
-- ===============================================================================================================
WITH pedidos_por_entregar AS(
	SELECT DISTINCT id_pedido
	FROM historial_estado_pedido
	WHERE estado = 'en_camino' OR estado = 'entregado'
)
SELECT *
FROM pedido pe
	JOIN pedidos_por_entregar e
	ON pe.id_pedido = e.id_pedido
WHERE pe.id_repartidor IS NULL
;
-- OK

-- ===============================================================================================================
-- 8. Máquina de estados finitos: Las transiciones de estado en el historial de un pedido deben respetar un flujo 
-- secuencial válido mediante las siguientes únicas rutas permitidas:
-- De 'creado' solo a 'en_preparacion' o 'cancelado'.
-- De 'en_preparacion' solo a 'en_camino' o 'cancelado'.
-- De 'en_camino' solo a 'entregado' o 'cancelado'.
-- ===============================================================================================================
WITH transiciones AS (
    SELECT 
        id_pedido,
        id_historial,
        estado AS estado_actual,
        fecha_hora,
        LAG(estado) OVER (PARTITION BY id_pedido ORDER BY fecha_hora) AS estado_anterior
    FROM 
        historial_estado_pedido
)
SELECT *
FROM transiciones
WHERE NOT (
    -- 1. El estado inicial obligatorio (no hay estado anterior)
    (estado_anterior IS NULL AND estado_actual = 'creado') 
    OR
    -- 2. Transiciones válidas desde 'creado'
    (estado_anterior = 'creado' AND estado_actual IN ('en_preparacion', 'cancelado')) 
    OR
    -- 3. Transiciones válidas desde 'en_preparacion'
    (estado_anterior = 'en_preparacion' AND estado_actual IN ('en_camino', 'cancelado')) 
    OR
    -- 4. Transiciones válidas desde 'en_camino'
    (estado_anterior = 'en_camino' AND estado_actual IN ('entregado', 'cancelado'))
);
-- OK