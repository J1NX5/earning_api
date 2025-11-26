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

    def _create_estimate_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estimates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date DATE,
            horizon VARCHAR(50),
            eps_estimate_average DECIMAL(10,4),
            eps_estimate_high DECIMAL(10,4),
            eps_estimate_low DECIMAL(10,4),
            eps_estimate_analyst_count INT,
            eps_estimate_average_7_days_ago DECIMAL(10,4),
            eps_estimate_average_30_days_ago DECIMAL(10,4),
            eps_estimate_average_60_days_ago DECIMAL(10,4),
            eps_estimate_average_90_days_ago DECIMAL(10,4),
            eps_estimate_revision_up_trailing_7_days INT,
            eps_estimate_revision_down_trailing_7_days INT,
            eps_estimate_revision_up_trailing_30_days INT,
            eps_estimate_revision_down_trailing_30_days INT,
            revenue_estimate_average DECIMAL(15,2),
            revenue_estimate_high DECIMAL(15,2),
            revenue_estimate_low DECIMAL(15,2),
            revenue_estimate_analyst_count INT
            );
        ''')
        return self.conn.commit()
    
    def insert_estimate(self, symb, date, horizon, eps_estimate_average, eps_estimate_high, eps_estimate_low, eps_estimate_analyst_count, eps_estimate_average_7_days_ago,
        eps_estimate_average_30_days_ago, eps_estimate_average_60_days_ago,
        eps_estimate_average_90_days_ago, eps_estimate_revision_up_trailing_7_days,
        eps_estimate_revision_down_trailing_7_days, eps_estimate_revision_up_trailing_30_days,
        eps_estimate_revision_down_trailing_30_days, revenue_estimate_average,
        revenue_estimate_high, revenue_estimate_low, revenue_estimate_analyst_count ):
        cursor = self.conn.cursor()
        cursor.execute('''
                    INSERT INTO estimates (
                    symbol, date, horizon, eps_estimate_average, eps_estimate_high, eps_estimate_low,
                    eps_estimate_analyst_count, eps_estimate_average_7_days_ago,
                    eps_estimate_average_30_days_ago, eps_estimate_average_60_days_ago,
                    eps_estimate_average_90_days_ago, eps_estimate_revision_up_trailing_7_days,
                    eps_estimate_revision_down_trailing_7_days, eps_estimate_revision_up_trailing_30_days,
                    eps_estimate_revision_down_trailing_30_days, revenue_estimate_average,
                    revenue_estimate_high, revenue_estimate_low, revenue_estimate_analyst_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (
                        symb, date, horizon, eps_estimate_average, eps_estimate_high, eps_estimate_low,
                        eps_estimate_analyst_count, eps_estimate_average_7_days_ago,
                        eps_estimate_average_30_days_ago, eps_estimate_average_60_days_ago,
                        eps_estimate_average_90_days_ago, eps_estimate_revision_up_trailing_7_days,
                        eps_estimate_revision_down_trailing_7_days, eps_estimate_revision_up_trailing_30_days,
                        eps_estimate_revision_down_trailing_30_days, revenue_estimate_average,
                        revenue_estimate_high, revenue_estimate_low, revenue_estimate_analyst_count
                    ))
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