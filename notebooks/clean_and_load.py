"""
Projeto Olist BI - limpeza e consolidacao dos dados
Le os CSVs brutos em data/raw/, trata e junta as tabelas, calcula metricas
de atraso de entrega e distancia vendedor-cliente, e gera:
  - data/processed/fact_orders.csv       (uma linha por pedido, pronta pro Power BI)
  - data/processed/dim_products.csv      (categoria em pt e en)
  - sql/olist.db                         (banco SQLite com as tabelas tratadas)

Rode este script a partir da raiz do projeto:
    python notebooks/clean_and_load.py
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "sql" / "olist.db"

DATE_COLS_ORDERS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def haversine_km(lat1, lon1, lat2, lon2):
    """Distancia em km entre dois pontos lat/lon (formula de haversine, vetorizada)."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c


def load_raw():
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv", dtype={"customer_zip_code_prefix": str})
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv", parse_dates=DATE_COLS_ORDERS)
    order_items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv", parse_dates=["shipping_limit_date"])
    payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
    reviews = pd.read_csv(
        RAW_DIR / "olist_order_reviews_dataset.csv",
        parse_dates=["review_creation_date", "review_answer_timestamp"],
    )
    products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
    sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv", dtype={"seller_zip_code_prefix": str})
    geolocation = pd.read_csv(RAW_DIR / "olist_geolocation_dataset.csv", dtype={"geolocation_zip_code_prefix": str})
    category_translation = pd.read_csv(RAW_DIR / "product_category_name_translation.csv", encoding="utf-8-sig")
    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "reviews": reviews,
        "products": products,
        "sellers": sellers,
        "geolocation": geolocation,
        "category_translation": category_translation,
    }


def build_geo_lookup(geolocation: pd.DataFrame) -> pd.DataFrame:
    """Um lat/lon medio por prefixo de CEP (reduz ruido de duplicidade)."""
    return (
        geolocation.groupby("geolocation_zip_code_prefix")
        .agg(lat=("geolocation_lat", "mean"), lon=("geolocation_lng", "mean"))
        .reset_index()
        .rename(columns={"geolocation_zip_code_prefix": "zip_code_prefix"})
    )


def clean_products(products: pd.DataFrame, category_translation: pd.DataFrame) -> pd.DataFrame:
    products = products.merge(category_translation, on="product_category_name", how="left")
    products["product_category_name_english"] = products["product_category_name_english"].fillna("unknown")
    return products[["product_id", "product_category_name", "product_category_name_english"]]


def clean_payments(payments: pd.DataFrame) -> pd.DataFrame:
    """Agrega pagamentos por pedido (um pedido pode ter varias parcelas/formas de pagamento)."""
    return (
        payments.groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_installments_max=("payment_installments", "max"),
            payment_types=("payment_type", lambda s: ", ".join(sorted(set(s)))),
        )
        .reset_index()
    )


def clean_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    """Mantem a review mais recente por pedido (existem poucos pedidos com mais de uma)."""
    reviews_sorted = reviews.sort_values("review_answer_timestamp")
    return reviews_sorted.drop_duplicates(subset="order_id", keep="last")[
        ["order_id", "review_score", "review_creation_date"]
    ]


def build_fact_orders(tables: dict) -> pd.DataFrame:
    orders = tables["orders"]
    customers = tables["customers"]
    order_items = tables["order_items"]
    sellers = tables["sellers"]
    products = clean_products(tables["products"], tables["category_translation"])
    payments = clean_payments(tables["payments"])
    reviews = clean_reviews(tables["reviews"])
    geo = build_geo_lookup(tables["geolocation"])

    # Nivel pedido+item: junta item -> produto -> vendedor
    items = order_items.merge(products, on="product_id", how="left")
    items = items.merge(sellers, on="seller_id", how="left")

    # Distancia vendedor -> cliente por item (via CEP do pedido)
    items = items.merge(
        orders[["order_id", "customer_id"]], on="order_id", how="left"
    ).merge(customers[["customer_id", "customer_zip_code_prefix", "customer_state", "customer_city"]], on="customer_id", how="left")

    items = items.merge(
        geo.rename(columns={"zip_code_prefix": "seller_zip_code_prefix", "lat": "seller_lat", "lon": "seller_lon"}),
        on="seller_zip_code_prefix",
        how="left",
    )
    items = items.merge(
        geo.rename(columns={"zip_code_prefix": "customer_zip_code_prefix", "lat": "customer_lat", "lon": "customer_lon"}),
        on="customer_zip_code_prefix",
        how="left",
    )
    items["distance_km"] = haversine_km(
        items["seller_lat"], items["seller_lon"], items["customer_lat"], items["customer_lon"]
    )

    # Agrega item -> pedido (1 linha por pedido)
    order_agg = (
        items.groupby("order_id")
        .agg(
            n_items=("order_item_id", "count"),
            items_price=("price", "sum"),
            freight_value=("freight_value", "sum"),
            avg_distance_km=("distance_km", "mean"),
            main_category=("product_category_name_english", lambda s: s.value_counts().idxmax() if len(s.dropna()) else "unknown"),
            seller_state=("seller_state", lambda s: s.value_counts().idxmax() if len(s.dropna()) else None),
        )
        .reset_index()
    )

    fact = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(order_agg, on="order_id", how="left")
        .merge(payments, on="order_id", how="left")
        .merge(reviews, on="order_id", how="left")
    )

    # Metricas de atraso (so faz sentido pra pedidos entregues)
    fact["delivery_delay_days"] = (
        fact["order_delivered_customer_date"] - fact["order_estimated_delivery_date"]
    ).dt.days
    fact["is_late"] = np.where(
        fact["order_delivered_customer_date"].notna(),
        fact["delivery_delay_days"] > 0,
        np.nan,
    )
    fact["purchase_month"] = fact["order_purchase_timestamp"].dt.to_period("M").astype(str)
    fact["purchase_weekday"] = fact["order_purchase_timestamp"].dt.day_name()

    cols = [
        "order_id", "customer_id", "customer_state", "customer_city",
        "order_status", "order_purchase_timestamp", "order_delivered_customer_date",
        "order_estimated_delivery_date", "delivery_delay_days", "is_late",
        "purchase_month", "purchase_weekday",
        "n_items", "items_price", "freight_value", "avg_distance_km",
        "main_category", "seller_state",
        "payment_value", "payment_installments_max", "payment_types",
        "review_score",
    ]
    return fact[cols]


def save_outputs(fact: pd.DataFrame, tables: dict):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    fact.to_csv(PROCESSED_DIR / "fact_orders.csv", index=False)
    clean_products(tables["products"], tables["category_translation"]).to_csv(
        PROCESSED_DIR / "dim_products.csv", index=False
    )

    conn = sqlite3.connect(DB_PATH)
    fact.to_sql("fact_orders", conn, if_exists="replace", index=False)
    tables["customers"].to_sql("dim_customers", conn, if_exists="replace", index=False)
    tables["sellers"].to_sql("dim_sellers", conn, if_exists="replace", index=False)
    clean_products(tables["products"], tables["category_translation"]).to_sql(
        "dim_products", conn, if_exists="replace", index=False
    )
    conn.close()


def main():
    print("Lendo CSVs brutos...")
    tables = load_raw()

    print("Tratando e consolidando (isso pode levar ~1 minuto por causa da geolocalizacao)...")
    fact = build_fact_orders(tables)

    print("Salvando data/processed/*.csv e sql/olist.db ...")
    save_outputs(fact, tables)

    print(f"Pronto! {len(fact):,} pedidos processados.".replace(",", "."))
    print(f"- {PROCESSED_DIR / 'fact_orders.csv'}")
    print(f"- {DB_PATH}")


if __name__ == "__main__":
    main()
