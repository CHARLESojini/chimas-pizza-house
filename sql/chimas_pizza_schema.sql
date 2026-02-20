-- Drop tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS Order_Items CASCADE;
DROP TABLE IF EXISTS Menu_Item_Ingredients CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Customers CASCADE;
DROP TABLE IF EXISTS Stores CASCADE;
DROP TABLE IF EXISTS Menu_Items CASCADE;
DROP TABLE IF EXISTS Ingredients CASCADE;


-- CREATE TABLE (STORE)

CREATE TABLE Stores (
    store_id  SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    city  VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE (CUSTOMERS)

CREATE TABLE Customers(
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100)NOT NULL,
    last_name VARCHAR(100)NOT NULL,
    email VARCHAR(255)UNIQUE NOT NULL,
    phone_number VARCHAR(20)UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE (INGREDIENTS)

CREATE TABLE Ingredients(
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(100)UNIQUE NOT NULL,
    stock_quantity NUMERIC(10,2) NOT NULL DEFAULT 0,
    unit VARCHAR(20) NOT NULL
);

-- CREATE TABLE (MENU_ITEMS)

CREATE TABLE Menu_Items(
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    size VARCHAR(20),
    price NUMERIC(10,2) NOT NULL
);

-- CREATE TABLE (ORDERS)

CREATE TABLE Orders(
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES Customers(customer_id) ON DELETE SET NULL,
    store_id INTEGER NOT NULL REFERENCES Stores(store_id) ON DELETE RESTRICT,
    order_timestamp TIMESTAMP NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL
);

-- CREATE TABLE (ORDER_ITEMS)

CREATE TABLE Order_Items(
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES Orders(order_id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES Menu_Items(item_id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    item_price NUMERIC(10,2) NOT NULL
);

-- CREATE TABLE (Menu_Item_Ingredients)

CREATE TABLE Menu_Item_Ingredients(
    menu_item_ingredient_id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES Menu_Items(item_id) ON DELETE CASCADE,
    ingredient_id INTEGER REFERENCES Ingredients(ingredient_id) ON DELETE CASCADE,
    quantity_needed NUMERIC(10,2)NOT NULL DEFAULT 1 CHECK (quantity_needed > 0)
);

-- INDEXES (Performance optimization for common queries)

CREATE INDEX idx_orders_customer_id ON Orders(customer_id);
CREATE INDEX idx_orders_store_id ON Orders(store_id);
CREATE INDEX idx_orders_timestamp ON Orders(order_timestamp);
CREATE INDEX idx_order_items_order_id ON Order_Items(order_id);
CREATE INDEX idx_order_items_item_id ON Order_Items(item_id);