-- Pergunta 4: quais categorias geram mais receita, e como estao em atraso/avaliacao?
SELECT
    main_category,
    COUNT(*)                                          AS n_pedidos,
    ROUND(SUM(items_price), 2)                         AS receita_total,
    ROUND(AVG(review_score), 2)                         AS nota_media,
    ROUND(100.0 * SUM(is_late) / COUNT(is_late), 1)      AS pct_atraso
FROM fact_orders
GROUP BY main_category
ORDER BY receita_total DESC
LIMIT 15;
