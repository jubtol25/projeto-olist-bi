-- Pergunta 4: quais categorias geram mais receita, e como estao em atraso/avaliacao?
-- (SQL Server / T-SQL)
SELECT TOP 15
    main_category,
    COUNT(*)                                          AS n_pedidos,
    ROUND(SUM(items_price), 2)                         AS receita_total,
    ROUND(AVG(CAST(review_score AS FLOAT)), 2)          AS nota_media,
    ROUND(100.0 * SUM(CAST(is_late AS INT)) / NULLIF(COUNT(is_late), 0), 1) AS pct_atraso
FROM fact_orders
GROUP BY main_category
ORDER BY receita_total DESC;
