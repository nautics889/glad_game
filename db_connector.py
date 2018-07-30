import sqlite3
import sys

class DataBase:
    def __init__(self):
        self.con = sqlite3.connect('scores.db')
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Scores(Id INTEGER PRIMARY KEY AUTOINCREMENT, Score INT)')

    def add_score(self, score):
        with self.con:
            self.cur.execute('INSERT INTO Scores (Score) VALUES (?)', (score,))

    def get_highest_score(self):
        with self.con:
            self.cur.execute('SELECT MAX(Score) FROM Scores')
            try:
                score = self.cur.fetchone()[0]
            except TypeError:
                score = '0'
            finally:
                return score

    def close(self):
        self.con.close()