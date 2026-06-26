-- C1
SELECT 
    'id_usuario' AS columna,
    COUNT(*) AS cantidad_total_filas,
    COUNT(id_usuario) AS cantidad_no_nulos,
    ROUND(COUNT(id_usuario) * 100.0 / NULLIF(COUNT(*), 0), 2) AS porcentaje_no_nulos,
    COUNT(DISTINCT id_usuario) AS cantidad_valores_diferentes
FROM pedido

UNION ALL

SELECT 
    'id_promocion' AS columna,
    COUNT(*) AS cantidad_total_filas,
    COUNT(id_promocion) AS cantidad_no_nulos,
    ROUND(COUNT(id_promocion) * 100.0 / NULLIF(COUNT(*), 0), 2) AS porcentaje_no_nulos,
    COUNT(DISTINCT id_promocion) AS cantidad_valores_diferentes
FROM pedido;

--C2
WITH percentiles AS (
    SELECT 
        'total_abonado' AS columna,
        COUNT(*) AS total_filas,
        ROUND(STDDEV(total_abonado),2) AS desvio_estandard,
        MIN(total_abonado) AS minimo,
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY total_abonado) AS p05,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_abonado) AS primer_cuartil,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_abonado) AS mediana,
        ROUND(AVG(total_abonado),2) AS promedio,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_abonado) AS tercer_cuartil,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total_abonado) AS p95,
        MAX(total_abonado) AS maximo,
        COUNT(*) FILTER (WHERE total_abonado = 0) AS cantidad_ceros,
        COUNT(*) FILTER (WHERE total_abonado < 0) AS cantidad_negativos
    FROM pedido
    WHERE total_abonado IS NOT NULL
),
limites_iqr AS (
    SELECT 
        *,
        ROUND((cantidad_ceros * 100.0 / NULLIF(total_filas, 0)), 2) AS porcentaje_ceros,
        ROUND((cantidad_negativos * 100.0 / NULLIF(total_filas, 0)), 2) AS porcentaje_negativos,
        (primer_cuartil - 1.5 * (tercer_cuartil - primer_cuartil)) AS limite_inferior,
        (tercer_cuartil + 1.5 * (tercer_cuartil - primer_cuartil)) AS limite_superior
    FROM percentiles
)
SELECT 
    desvio_estandard, minimo, p05, primer_cuartil, mediana, promedio, 
    tercer_cuartil, p95, maximo, cantidad_ceros, porcentaje_ceros, 
    cantidad_negativos, porcentaje_negativos,
    (SELECT COUNT(*) FROM pedido 
     WHERE total_abonado < limites_iqr.limite_inferior 
        OR total_abonado > limites_iqr.limite_superior) AS cantidad_outliers
FROM limites_iqr;


--C3
WITH frecuencias AS (
    SELECT 
        id_restaurante::text AS categoria,
        COUNT(*) AS frecuencia,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM pedido WHERE id_restaurante IS NOT NULL), 2) AS porcentaje
    FROM pedido
    WHERE id_restaurante IS NOT NULL
    GROUP BY id_restaurante
),
ranking_categorias AS (
    SELECT 
        categoria,
        frecuencia,
        porcentaje,
        ROW_NUMBER() OVER (ORDER BY frecuencia DESC) AS puesto
    FROM frecuencias
)
SELECT 
    CASE 
        WHEN puesto <= 10 THEN categoria 
        ELSE 'Resto' 
    END AS valor_categorico,
    SUM(frecuencia) AS frecuencia_total,
    SUM(porcentaje) AS porcentaje_total
FROM ranking_categorias
GROUP BY 
    CASE 
        WHEN puesto <= 10 THEN categoria 
        ELSE 'Resto' 
    END
ORDER BY frecuencia_total DESC;