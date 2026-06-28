-- Obtiene el top 5 de restaurantes con el menor tiempo promedio de preparación.
-- El tiempo (en minutos) se calcula como la diferencia entre el estado 'en preparación' 
-- y el cambio del pedido al estado 'en_camino'.

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


-- Ranking top 3 de los clientes que más han gastado según 
-- categoría de platos.

WITH consumo_total AS(
	SELECT u.id_usuario, u.nombre, r.categoria, SUM(pe.total_abonado) AS total_por_cat
	FROM restaurante r
		JOIN pedido pe
		ON r.id_restaurante = pe.id_restaurante
		JOIN usuario u
		ON pe.id_usuario = u.id_usuario
	GROUP BY u.id_usuario, r.categoria
	ORDER BY u.id_usuario
)
SELECT t.*	
FROM (
	SELECT ct.*,
	RANK() OVER(PARTITION BY categoria ORDER BY total_por_cat DESC) ranking
	FROM consumo_total ct
	) t
WHERE t.ranking <= 3
ORDER BY t.categoria, t.ranking ASC