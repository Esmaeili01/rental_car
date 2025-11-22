-- =============================
-- USERS TABLE
-- =============================
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    last_login TIMESTAMP,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    birthdate DATE,
    email VARCHAR(254) UNIQUE,
    address TEXT,
    role VARCHAR(15) CHECK (role IN ('superadmin','admin','owner','renter')) DEFAULT 'renter'
);

-- =============================
-- CARS TABLE
-- =============================
CREATE TABLE cars (
    car_id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    production_year INTEGER NOT NULL,
    color VARCHAR(20),
    seats INTEGER,
    category VARCHAR(20) CHECK (category IN ('sedan','suv','hatchback','truck','van')),
    only_with_driver BOOLEAN DEFAULT FALSE,
    with_driver BOOLEAN DEFAULT TRUE,
    gearbox VARCHAR(10) CHECK (gearbox IN ('manual','automatic')),
    fuel VARCHAR(10) CHECK (fuel IN ('gasoline','diesel','electric','hybrid')),
    fee DECIMAL(10,2) NOT NULL,
    status VARCHAR(15) CHECK (status IN ('available','suspended','unavailable')) DEFAULT 'available',
    country TEXT,
    province TEXT,
    city TEXT,
    description TEXT,
    image_url TEXT
);

-- =============================
-- RENTS TABLE
-- =============================
CREATE TABLE rents (
    rent_id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(car_id) ON DELETE CASCADE,
    renter_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending payment','on your rent', 'not yet' , 'over')) DEFAULT 'pending payment',
    total_fee DECIMAL(10,2)
);

-- =============================
-- PAYMENTS TABLE
-- =============================
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    rent_id INTEGER UNIQUE NOT NULL REFERENCES rents(rent_id) ON DELETE CASCADE,
    total_amount DECIMAL(10,2) NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method VARCHAR(10) CHECK (method IN ('online','cash')),
    tracking_code VARCHAR(50),
    status VARCHAR(15) CHECK (status IN ('pending','successful','failed')) DEFAULT 'pending'
);

-- =============================
-- REVIEWS TABLE
-- =============================
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    rent_id INTEGER NOT NULL REFERENCES rents(rent_id) ON DELETE CASCADE,
    renter_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score SMALLINT CHECK (score BETWEEN 1 AND 5),
    comment TEXT
);

-- =============================
-- LOGINS TABLE
-- =============================
CREATE TABLE logins (
    login_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    is_signup BOOLEAN NOT NULL,
    datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);