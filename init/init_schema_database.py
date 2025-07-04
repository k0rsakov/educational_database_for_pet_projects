from database.PostgreSQL import pg_connect_uri, run_query

query_init = """
-- Регионы и города
CREATE TABLE region (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE
);

CREATE TABLE city (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    region_id BIGINT NOT NULL REFERENCES region(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT uniq_city_region UNIQUE (name, region_id)
);

-- Поставщики
CREATE TABLE supplier (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    address TEXT,
    phone VARCHAR(32),
    email VARCHAR(128)
);

-- Магазины
CREATE TABLE market (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE,
    address TEXT,
    city_id BIGINT NOT NULL REFERENCES city(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Склады
CREATE TABLE warehouse (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    address TEXT,
    market_id BIGINT REFERENCES market(id) ON DELETE SET NULL ON UPDATE CASCADE,
    city_id BIGINT NOT NULL REFERENCES city(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT uniq_warehouse_city UNIQUE(name, city_id)
);

-- Категории
CREATE TABLE product_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE
);

CREATE TABLE users_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE -- Физическое лицо, Юридическое лицо, ИП
);

CREATE TABLE employees_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE
);

CREATE TABLE department (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE
);

-- Пользователи
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    middle_name VARCHAR(64),
    birthday DATE,
    gender CHAR(1),
    email VARCHAR(128) UNIQUE,
    users_category_id BIGINT NOT NULL REFERENCES users_category(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Сотрудники
CREATE TABLE employees (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    middle_name VARCHAR(64),
    birthday DATE,
    gender CHAR(1),
    email VARCHAR(128) UNIQUE,
    phone VARCHAR(32),
    employees_category_id BIGINT NOT NULL REFERENCES employees_category(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- История отделов сотрудников (если сотрудник переводился)
CREATE TABLE employees_department (
    id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT NOT NULL REFERENCES employees(id) ON DELETE CASCADE ON UPDATE CASCADE,
    department_id BIGINT NOT NULL REFERENCES department(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT uniq_employee_department UNIQUE(employee_id, department_id, start_date)
);

-- Товары, цены, остатки
CREATE TABLE product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    product_category_id BIGINT NOT NULL REFERENCES product_category(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    supplier_id BIGINT REFERENCES supplier(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE product_price (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES product(id) ON DELETE CASCADE ON UPDATE CASCADE,
    price NUMERIC(12,2) NOT NULL CHECK (price > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE INDEX idx_product_price_product_created_at ON product_price(product_id, created_at DESC);

CREATE TABLE stock (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES product(id) ON DELETE CASCADE ON UPDATE CASCADE,
    warehouse_id BIGINT NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE ON UPDATE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    CONSTRAINT uniq_product_warehouse UNIQUE(product_id, warehouse_id)
);

-- Заказы и их позиции
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    employee_id BIGINT REFERENCES employees(id) ON DELETE SET NULL ON UPDATE CASCADE,
    market_id BIGINT REFERENCES market(id) ON DELETE SET NULL ON UPDATE CASCADE,
    status VARCHAR(32) NOT NULL, -- created, confirmed, cancelled, completed
    total NUMERIC(14,2),
    comment TEXT
);

CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE ON UPDATE CASCADE,
    product_id BIGINT NOT NULL REFERENCES product(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price NUMERIC(12,2) NOT NULL CHECK (price > 0)
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- Продажи
CREATE TABLE sales (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    sale_date TIMESTAMP WITH TIME ZONE,
    total NUMERIC(14,2) NOT NULL,
    employee_id BIGINT REFERENCES employees(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Оплаты
CREATE TABLE payment (
    id BIGSERIAL PRIMARY KEY,
    sale_id BIGINT NOT NULL REFERENCES sales(id) ON DELETE CASCADE ON UPDATE CASCADE,
    amount NUMERIC(14,2) NOT NULL CHECK (amount > 0),
    payment_date TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    payment_type VARCHAR(32), -- cash, card, online
    status VARCHAR(32) -- paid, pending, failed
);

-- Доставка
CREATE TABLE delivery (
    id BIGSERIAL PRIMARY KEY,
    sale_id BIGINT NOT NULL UNIQUE REFERENCES sales(id) ON DELETE CASCADE ON UPDATE CASCADE,
    delivery_date DATE,
    delivery_address TEXT,
    city_id BIGINT NOT NULL REFERENCES city(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    employee_id BIGINT REFERENCES employees(id) ON DELETE SET NULL ON UPDATE CASCADE,
    status VARCHAR(32), -- in_progress, delivered, cancelled
    comment TEXT
);

-- Примеры индексов для ускорения выборок
CREATE INDEX idx_users_category_id ON users(users_category_id);
CREATE INDEX idx_employees_category_id ON employees(employees_category_id);
CREATE INDEX idx_product_category_id ON product(product_category_id);
CREATE INDEX idx_stock_warehouse_id ON stock(warehouse_id);

-- Проверочные ограничения и уникальности
ALTER TABLE users ADD CONSTRAINT chk_gender CHECK (gender IN ('M', 'F', 'O'));
ALTER TABLE employees ADD CONSTRAINT chk_gender CHECK (gender IN ('M', 'F', 'O'));

-- Дополнительные комментарии
COMMENT ON TABLE delivery IS 'Каждая доставка однозначно относится к одной продаже. Одна продажа — одна доставка.';
COMMENT ON TABLE sales IS 'Каждая продажа привязана к одному заказу (order).';
COMMENT ON TABLE order_items IS 'Позиции заказа: один заказ — много товаров.';
COMMENT ON COLUMN users_category.name IS 'Тип пользователя: Физическое лицо, Юридическое лицо, ИП.';

-- Пример наполнения справочников
INSERT INTO users_category(name) VALUES ('Физическое лицо'),('Юридическое лицо'),('ИП');
"""

run_query(
    engine=pg_connect_uri(),
    sql=query_init,
)
