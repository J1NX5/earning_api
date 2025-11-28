import sqlite3

class DBManager:
    def __init__(self):
        self.db_path: str = "data.db"
        self.conn = self._create_connection(self.db_path)
        self.create_earning_report_table()

    def _create_connection(self, db_file):
        connection = sqlite3.connect(db_file)
        return connection
    
    def create_earning_report_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                eps_actual REAL NULL,
                eps_estimated REAL NULL,
                revenue_actual INTEGER NULL,
                revenue_estimated INTEGER NULL,
                last_updated TEXT NOT NULL,
                call_date TEXT NOT NULL,
                active BOOL DEFAULT True
                );
        ''')
        return self.conn.commit()
    
    def insert_earning_report(self, symbol, date, eps_actual, eps_estimated, revenue_actual, revenue_estimated, last_updated, call_date, active):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO earnings (symbol, date, eps_actual, eps_estimated, revenue_actual, revenue_estimated, last_updated, call_date)
            SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM earnings
                WHERE symbol = ? AND date = ? AND eps_actual = ? 
                AND eps_estimated = ? AND revenue_actual = ?
                AND revenue_estimated = ? AND last_updated = ? AND call_date = ? active = ?
            )
            ''', (  symbol, date, eps_actual, eps_estimated, revenue_actual, revenue_estimated, last_updated, call_date, active,
                    symbol, date, eps_actual, eps_estimated, revenue_actual, revenue_estimated, last_updated, call_date, active  )
        ) 
        return self.conn.commit()

    # returns None if nothing found
    def find_by_symbol(self, symbol):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM data WHERE symbol = ?;
        ''', (symbol,))
        return cursor.fetchone()
    
    # def update_values(self, symbol, name, reportDate, fiscalDate, estimate, currency, timeOfTheDay):
    #     cursor = self.conn.cursor()
    #     cursor.execute('''
    #         UPDATE data
    #         SET reportDate = ?, fiscalDate = ?, estimate = ?, currency = ?, timeOfTheDay = ?
    #         WHERE symbol = ? AND name = ?;
    #     ''', (reportDate, fiscalDate, estimate, currency, timeOfTheDay, symbol, name))
    #     return self.conn.commit()