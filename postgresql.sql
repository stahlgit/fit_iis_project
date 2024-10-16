-- Table for Konference (Conference)
CREATE TABLE Konference (
    id SERIAL PRIMARY KEY,
    název VARCHAR(255) NOT NULL,
    popis TEXT,
    žánr VARCHAR(255),
    místo VARCHAR(255),
    časový_interval tstzrange,  -- Assuming DateTimeRange as a timestamp range
    cena DECIMAL(10, 2),
    kapacita INT
);

-- Table for Místnost (Room)
CREATE TABLE Místnost (
    id SERIAL PRIMARY KEY,
    název VARCHAR(255) NOT NULL,
    kapacita INT,
    konference_id INT NOT NULL,
    FOREIGN KEY (konference_id) REFERENCES Konference(id) ON DELETE CASCADE
);

-- Table for Přednáška (Presentation)
CREATE TABLE Přednáška (
    id SERIAL PRIMARY KEY,
    název VARCHAR(255) NOT NULL,
    přednášející INT NOT NULL,  -- References User
    popis TEXT,
    čas tstzrange,  -- Assuming DateTimeRange as a timestamp range
    místnost_id INT NOT NULL,
    konference_id INT NOT NULL,
    tagy VARCHAR(255),
    obrázek VARCHAR(255),
    FOREIGN KEY (přednášející) REFERENCES Uživatel(id) ON DELETE CASCADE,
    FOREIGN KEY (místnost_id) REFERENCES Místnost(id) ON DELETE CASCADE,
    FOREIGN KEY (konference_id) REFERENCES Konference(id) ON DELETE CASCADE
);

-- Table for Uživatel (User)
CREATE TABLE Uživatel (
    id SERIAL PRIMARY KEY,
    jméno VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hash VARCHAR(255) NOT NULL,  -- Password hash
    role VARCHAR(50)  -- Role such as admin, registered user, etc.
);

-- Table for Rezervace (Reservation)
CREATE TABLE Rezervace (
    id SERIAL PRIMARY KEY,
    uživatel_id INT NOT NULL,
    konference_id INT NOT NULL,
    počet_vstupenek INT,
    stav VARCHAR(50),  -- Reservation status (e.g., "Reserved", "Paid")
    uhrazeno BOOLEAN,  -- Payment status
    FOREIGN KEY (uživatel_id) REFERENCES Uživatel(id) ON DELETE CASCADE,
    FOREIGN KEY (konference_id) REFERENCES Konference(id) ON DELETE CASCADE
);

-- Table for Podaná Prezentace (Submitted Presentation)
CREATE TABLE "Podaná prezentace" (
    id SERIAL PRIMARY KEY,
    uživatel_id INT NOT NULL,
    konference_id INT NOT NULL,
    návrh_prezentace TEXT NOT NULL,
    stav VARCHAR(50),  -- Status (e.g., "Approved", "Pending")
    FOREIGN KEY (uživatel_id) REFERENCES Uživatel(id) ON DELETE CASCADE,
    FOREIGN KEY (konference_id) REFERENCES Konference(id) ON DELETE CASCADE
);

-- Table for Vstupenka (Ticket)
CREATE TABLE Vstupenka (
    id SERIAL PRIMARY KEY,
    rezervace_id INT NOT NULL,
    vytvořeno TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    FOREIGN KEY (rezervace_id) REFERENCES Rezervace(id) ON DELETE CASCADE
);

-- Table for Hlasování (Voting)
CREATE TABLE Hlasování (
    id SERIAL PRIMARY KEY,
    uživatel_id INT NOT NULL,
    prezentace_id INT NOT NULL,
    hodnocení INT CHECK (hodnocení BETWEEN 1 AND 5),  -- Assuming rating 1-5
    FOREIGN KEY (uživatel_id) REFERENCES Uživatel(id) ON DELETE CASCADE,
    FOREIGN KEY (prezentace_id) REFERENCES Přednáška(id) ON DELETE CASCADE
);

-- Table for Otázka (Question)
CREATE TABLE Otázka (
    id SERIAL PRIMARY KEY,
    uživatel_id INT NOT NULL,
    prezentace_id INT NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (uživatel_id) REFERENCES Uživatel(id) ON DELETE CASCADE,
    FOREIGN KEY (prezentace_id) REFERENCES Přednáška(id) ON DELETE CASCADE
);
