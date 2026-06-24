--Devuelve los 5 restaurantes que demoran menos tiempo en ir
--desde que el pedido esta en preparacion hasta que el pedido
--esta en camino

WITH tiempos_de_preparacion AS (
    SELECT hs.id_historial, hs.id_pedido,
           (fecha_hora_siguiente - fecha_hora) as tiempo_preparacion,
           p.id_restaurante
    FROM (
        SELECT h.*, 
               LEAD(estado) OVER (PARTITION BY id_pedido ORDER BY fecha_hora) as estado_siguiente, 
               LEAD(fecha_hora) OVER (PARTITION BY id_pedido ORDER BY fecha_hora) as fecha_hora_siguiente
        FROM historial_estado_pedido h
            ) hs
    JOIN pedido p ON hs.id_pedido = p.id_pedido
    WHERE estado_siguiente = 'en_camino'
)
SELECT ROUND(AVG(EXTRACT(MINUTE FROM t.tiempo_preparacion)), 2) as prom_tiempos_preparacion,
       t.id_restaurante, 
       r.nombre
FROM tiempos_de_preparacion t
JOIN restaurante r ON t.id_restaurante = r.id_restaurante
GROUP BY t.id_restaurante, r.nombre
ORDER BY prom_tiempos_preparacion ASC
LIMIT 5;