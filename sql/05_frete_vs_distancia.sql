-- Pergunta 5: o frete e o cancelamento aumentam com a distancia vendedor-cliente?
-- (SQL Server / T-SQL)
SELECT
    CASE
        WHEN avg_distance_km < 200  THEN '0-200km'
        WHEN avg_distance_km < 500  THEN '200-500km'
        WHEN avg_distance_km < 1000 THEN '500-1000km'
        ELSE '1000km+'
    END                                                                       AS faixa_distancia,
    COUNT(*)                                                                  AS n_pedidos,
    ROUND(AVG(freight_value), 2)                                              AS frete_medio,
    SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END)                AS cancelados,
    ROUND(100.0 * SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_cancelado,
    MIN(avg_distance_km)                                                      AS min_distancia_ordenacao
FROM fact_orders
WHERE avg_distance_km IS NOT NULL
GROUP BY
    CASE
        WHEN avg_distance_km < 200  THEN '0-200km'
        WHEN avg_distance_km < 500  THEN '200-500km'
        WHEN avg_distance_km < 1000 THEN '500-1000km'
        ELSE '1000km+'
    END
ORDER BY min_distancia_ordenacao;
