import sqlite3
import configparser
import pandas as pd

class TennisServerPersitencyService:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("paths.properties")
        self.db_path = config.get("paths", "db_path")
        self.csv_path = config.get("paths", "csv_path")

    def load_tournaments(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tournament")
        tournaments = cursor.fetchall()
        conn.close()
        return tournaments

    def load_matches(self, tourney_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tennis_match WHERE tourney_id = ?", (tourney_id,))
        matches = cursor.fetchall()
        conn.close()
        return matches

    def create_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS tournament;")
        cursor.execute("DROP TABLE IF EXISTS tennis_match;")

        cursor.execute('''
                CREATE TABLE tournament (
                    tourney_id TEXT PRIMARY KEY,
                    tourney_name TEXT,
                    surface TEXT,
                    draw_size INTEGER,
                    tourney_level TEXT,
                    tourney_date INTEGER
                );
            ''')

        cursor.execute('''
                CREATE TABLE tennis_match (
                    match_num INTEGER,
                    tourney_id TEXT,
                    winner_id INTEGER,
                    winner_seed TEXT,
                    winner_entry TEXT,
                    winner_name TEXT,
                    winner_hand TEXT,
                    winner_ht REAL,
                    winner_ioc TEXT,
                    winner_age REAL,
                    loser_id INTEGER,
                    loser_seed TEXT,
                    loser_entry TEXT,
                    loser_name TEXT,
                    loser_hand TEXT,
                    loser_ht REAL,
                    loser_ioc TEXT,
                    loser_age REAL,
                    score TEXT,
                    best_of INTEGER,
                    round TEXT,
                    minutes INTEGER,
                    w_ace INTEGER,
                    w_df INTEGER,
                    w_svpt INTEGER,
                    w_1stIn INTEGER,
                    w_1stWon INTEGER,
                    w_2ndWon INTEGER,
                    w_SvGms INTEGER,
                    w_bpSaved INTEGER,
                    w_bpFaced INTEGER,
                    l_ace INTEGER,
                    l_df INTEGER,
                    l_svpt INTEGER,
                    l_1stIn INTEGER,
                    l_1stWon INTEGER,
                    l_2ndWon INTEGER,
                    l_SvGms INTEGER,
                    l_bpSaved INTEGER,
                    l_bpFaced INTEGER,
                    winner_rank REAL,
                    winner_rank_points REAL,
                    loser_rank REAL,
                    loser_rank_points REAL,
                    PRIMARY KEY (match_num, tourney_id),
                    FOREIGN KEY (tourney_id) REFERENCES tournaments(tourney_id)
                );
            ''')
        conn.commit()
        conn.close()


    def populate_database_with_csv_data(self):
        df = pd.read_csv(self.csv_path)
        conn = sqlite3.connect(self.db_path)

        tournament_data = df[['tourney_id', 'tourney_name', 'surface', 'draw_size', 'tourney_level', 'tourney_date']].drop_duplicates()
        tournament_data.to_sql('tournament', conn, if_exists='append', index=False)

        match_data = df.drop(columns=['tourney_name', 'surface', 'draw_size', 'tourney_level', 'tourney_date'])
        match_data.to_sql('tennis_match', conn, if_exists='append', index=False)

        conn.commit()
        conn.close()
        print(f"Database created and populated at {self.db_path} with composite key on matches table.")

