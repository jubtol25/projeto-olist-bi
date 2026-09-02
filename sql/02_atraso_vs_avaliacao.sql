-- Pergunta 2: pedidos atrasados recebem nota de avaliacao pior?
SELECT
    CASE WHEN is_late = 1 THEN 'Atrasado' ELSE 'No prazo' END AS situacao_entrega,
    ROUND(AVG(review_score), 2)                                AS nota_media,
    COUNT(*)                                                   AS n_pedidos
FROM fact_orders
WHERE review_score IS NOT NULL AND is_late IS NOT NULL
GROUP BY situacao_entrega;
