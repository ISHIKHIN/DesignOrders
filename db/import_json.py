import json
from db.database import get_connection

def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)

def import_clients(conn):
    clients = load_json("data/clients.json")
    conn.executemany(
        "INSERT INTO clients (id, name, phone) VALUES (?, ?, ?)",
        [(cid, data["name"], data["phone"]) for cid, data in clients.items()]
    )

def import_designers(conn):
    designers = load_json("data/designers.json")
    conn.executemany(
        "INSERT INTO designers (id, name, specialization) VALUES (?, ?, ?)",
        [(did, data["name"], data["specialization"]) for did, data in designers.items()]
    )

def import_orders(conn):
    orders = load_json("data/orders.json")
    conn.executemany(
        """INSERT INTO orders (id, client_id, designer_id, design_type, price, is_urgent, deadline)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [(o["order_id"], str(o["client_id"]), str(o["designer_id"]), o["design_type"], float(o["price"]), int(o["is_urgent"]), o["deadline"]) for o in orders]
    )

def import_stages(conn):
    stages = load_json("data/stages.json")
    conn.executemany(
        "INSERT INTO stages (id, order_id, name, deadline, status) VALUES (?, ?, ?, ?, ?)",
        [(s["stage_id"], s["order_id"], s["name"], s["deadline"], s["status"]) for s in stages]
    )

def main():
    conn = get_connection()
    try:
        import_clients(conn)
        import_designers(conn)
        import_orders(conn)
        import_stages(conn)
        conn.commit()
        print("Импорт данных завершен успешно!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()