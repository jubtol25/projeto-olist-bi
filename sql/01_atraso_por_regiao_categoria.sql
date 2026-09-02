-- Pergunta 1: qual o % de atraso na entrega por estado e categoria de produto?
SELECT
    customer_state,
    main_category,
    COUNT(*)                                       AS total_pedidos,
    SUM(is_late)                                   AS pedidos_atrasados,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 1)       AS pct_atraso
FROM fact_orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY customer_state, main_category
HAVING total_pedidos >= 20
ORDER BY pct_atraso DESC
LIMIT 20;
