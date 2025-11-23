import sqlite3

class DBManager:
    def __init__(self):
        self.db_path: str = "data.db"
        self.conn = self._create_connection(self.db_path)
        self._create_table()

    def _create_connection(self, db_file):
        connection = sqlite3.connect(db_file)
        return connection
    
    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                name TEXT NOT NULL,
                reportDate DATE,
                fiscalDate DATE,
                estimate REAL,
                currency TEXT,
                timeOfTheDay TEXT
            );
        ''')
        return self.conn.commit()
    
    def insert_data(self, symbol, name, reportDate, fiscalDate, estimate, currency, timeOfTheDay):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO data (
                symbol,
                name,
                reportDate,
                fiscalDate,
                estimate,
                currency,
                timeOfTheDay
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        ''', (symbol, name, reportDate, fiscalDate, estimate, currency, timeOfTheDay))
        return self.conn.commit()
    
    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM data;")
        rows = cursor.fetchall()
        return rows
    
    def find_by_symbol_name(self, symbol, name):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM data WHERE symbol = ? AND name = ? ORDER BY reportDate DESC LIMIT 1;
        ''', (symbol, name))
        return cursor.fetchone()
    
    def find_by_symbol(self, symbol):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM data WHERE symbol = ? ORDER BY reportDate DESC LIMIT 1;
        ''', (symbol,))
        return cursor.fetchone()
    
    def update_values(self, symbol, name, reportDate, fiscalDate, estimate, currency, timeOfTheDay):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE data
            SET reportDate = ?, fiscalDate = ?, estimate = ?, currency = ?, timeOfTheDay = ?
            WHERE symbol = ? AND name = ?;
        ''', (reportDate, fiscalDate, estimate, currency, timeOfTheDay, symbol, name))
        return self.conn.commit()