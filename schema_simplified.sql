-- PostgreSQL Schema for Rental Car System
-- Exact match to your requirements

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    birthdate DATE NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'customer', 'staff'))
);

-- Cars table
CREATE TABLE cars (
    car_id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    color VARCHAR(30) NOT NULL,
    category VARCHAR(30) NOT NULL CHECK (category IN ('economy', 'compact', 'mid_size', 'full_size', 'premium', 'luxury', 'suv', 'minivan', 'sports')),
    production_year INTEGER NOT NULL CHECK (production_year >= 1900 AND production_year <= 2030),
    gearbox VARCHAR(20) NOT NULL CHECK (gearbox IN ('manual', 'automatic', 'cvt')),
    fuel VARCHAR(20) NOT NULL CHECK (fuel IN ('petrol', 'diesel', 'hybrid', 'electric')),
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0)
);

-- Payments table
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tracking_code VARCHAR(50) NOT NULL UNIQUE
);

-- Rents table
CREATE TABLE rents (
    rent_id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(car_id) ON DELETE RESTRICT,
    renter_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    payment_id INTEGER REFERENCES payments(payment_id) ON DELETE SET NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price > 0),
    CONSTRAINT valid_rental_period CHECK (end_datetime > start_datetime)
);

-- Settings table
CREATE TABLE settings (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL
);

-- Create indexes for better performance
CREATE INDEX idx_cars_brand ON cars(brand);
CREATE INDEX idx_cars_category ON cars(category);
CREATE INDEX idx_cars_owner_id ON cars(owner_id);
CREATE INDEX idx_rents_car_id ON rents(car_id);
CREATE INDEX idx_rents_renter_id ON rents(renter_id);
CREATE INDEX idx_rents_payment_id ON rents(payment_id);
CREATE INDEX idx_rents_dates ON rents(start_datetime, end_datetime);
CREATE INDEX idx_payments_tracking_code ON payments(tracking_code);
CREATE INDEX idx_users_role ON users(role);

-- Insert some default settings
INSERT INTO settings (key, value) VALUES 
('company_name', 'RentaCar'),
('max_rental_days', '30'),
('late_fee_per_day', '25.00'),
('security_deposit_rate', '0.20'),
('tax_rate', '0.08');

-- Sample data
INSERT INTO users (first_name, last_name, phone_number, birthdate, role) VALUES 
('John', 'Smith', '+1234567890', '1985-03-15', 'admin'),
('Jane', 'Doe', '+1987654321', '1990-07-22', 'customer'),
('Mike', 'Johnson', '+1555123456', '1992-11-10', 'staff'),
('Sarah', 'Wilson', '+1777888999', '1988-05-05', 'customer');

INSERT INTO cars (owner_id, brand, model, color, category, production_year, gearbox, fuel, price) VALUES 
(1, 'Toyota', 'Corolla', 'White', 'economy', 2023, 'automatic', 'petrol', 28.00),
(1, 'Honda', 'Civic', 'Blue', 'compact', 2022, 'automatic', 'petrol', 38.00),
(1, 'BMW', '3 Series', 'Black', 'premium', 2024, 'automatic', 'petrol', 78.00),
(1, 'Mercedes-Benz', 'E-Class', 'Silver', 'luxury', 2024, 'automatic', 'petrol', 125.00),
(1, 'Toyota', 'RAV4', 'Red', 'suv', 2023, 'automatic', 'hybrid', 68.00);