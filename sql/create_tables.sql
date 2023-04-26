CREATE TABLE product
(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity_available INTEGER NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE address (
    id INTEGER PRIMARY KEY,
    line1 TEXT NOT NULL,
    line2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL
);

CREATE TABLE purchase (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    quantity_purchased INTEGER NOT NULL,
    date_purchased DATE NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (id),
    FOREIGN KEY (customer_id) REFERENCES customer (id)
);

CREATE TABLE supplier (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address_id INTEGER NOT NULL,
    phone TEXT NOT NULL,
    FOREIGN KEY (address_id) REFERENCES address (id)
);

CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    address_id INTEGER NOT NULL,
    phone TEXT NOT NULL,
    FOREIGN KEY (address_id) REFERENCES address (id)
);
