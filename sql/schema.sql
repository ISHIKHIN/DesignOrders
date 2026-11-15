PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clients (
    id    TEXT PRIMARY KEY,
    name  TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS designers (
    id             TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    specialization TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id          INTEGER PRIMARY KEY,
    client_id   TEXT NOT NULL,
    designer_id TEXT NOT NULL,
    design_type TEXT NOT NULL,
    price       REAL NOT NULL,
    is_urgent   INTEGER NOT NULL DEFAULT 0,
    deadline    TEXT NOT NULL,
    FOREIGN KEY (client_id)   REFERENCES clients(id),
    FOREIGN KEY (designer_id) REFERENCES designers(id)
);

CREATE TABLE IF NOT EXISTS stages (
    id       INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    name     TEXT NOT NULL,
    deadline TEXT NOT NULL,
    status   TEXT NOT NULL DEFAULT 'planned',
    FOREIGN KEY (order_id) REFERENCES orders(id)
);