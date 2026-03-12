from fastapi import APIRouter
import psycopg2
import os

router = APIRouter()


def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "utdb"),
        user=os.getenv("DB_USER", "utdb_api"),
        password=os.getenv("DB_PASS")
    )


@router.get("/transactions/lookup/auction")
def lookup_auction(item: str | None = None):

    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT
            item_type,
            quantity,
            price_per_item,
            total_value,
            timestamp
        FROM transactions
        WHERE event_type='auction_sale'
    """

    params = []

    if item:
        query += " AND item_type=%s"
        params.append(item)

    cur.execute(query, params)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for r in rows:
        results.append({
            "item_type": r[0],
            "quantity": float(r[1]),
            "price_per_item": float(r[2]),
            "total_value": float(r[3]),
            "timestamp": r[4]
        })

    return results