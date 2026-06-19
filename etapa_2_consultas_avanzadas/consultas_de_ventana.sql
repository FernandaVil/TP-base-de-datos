# devuelve los 5 restaurantes que demoran menos tiempo en ir
# desde que el pedido esta en preparacion hasta que el pedido
# esta en camino

with tiempos_de_preparacion as (
select hs.id_historial, hs.id_pedido,
		(fecha_hora_siguiente - fecha_hora) as tiempo_preparacion,
		p.id_restaurante
from (select h.*
	 		, lead(estado) over (partition by id_pedido
			 order by fecha_hora) estado_siguiente
			, lead(fecha_hora) over (partition by id_pedido
			 order by fecha_hora) fecha_hora_siguiente
	  from historial_estado_pedido h
	  order by fecha_hora) hs
join pedido p
 on hs.id_pedido = p.id_pedido
where estado_siguiente = 'en_camino'
order by id_pedido asc
)

select round(avg(extract (minute from t.tiempo_preparacion)),2) prom_tiempos_preparacion,
	   t.id_restaurante, r.nombre
from tiempos_de_preparacion t
join restaurante r
 on t.id_restaurante = r.id_restaurante
group by t.id_restaurante, r.nombre
order by prom_tiempos_preparacion asc
limit 5

select nombre, count(nombre) cantidad
from plato
group by nombre
order by cantidad desc
