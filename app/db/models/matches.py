import datetime

from app.db.database import Database


class Matches:
    def __init__(
            self, match_id: int, map_id: str or None, team1_id: int or None, team2_id: int or None,
            match_date: datetime.datetime or None, match_status: str
    ) -> None:
        self.match_id = match_id
        self.map_id = map_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.match_date = match_date
        self.match_status = match_status

    def save(self) -> None:
        db: Database = Database()
        query: str = """
            INSERT INTO matches (map_id, team1_id, team2_id, match_date, match_status)
            VALUES (%s, %s, %s, %s, %s)
        """
        db.execute_query(query, (
            self.map_id, self.team1_id, self.team2_id,
            self.match_date, self.match_status
        ))

    @classmethod
    def all(cls) -> list:
        db: Database = Database()
        query: str = """
            SELECT * FROM matches
        """
        return [cls(match_id=row[0], map_id=row[1], team1_id=row[2], team2_id=row[3], match_date=row[4],
                    match_status=row[5]) for row in db.fetch_query(query)]

    @staticmethod
    def get_all_cols() -> list[str]:
        return ["map_id", "team1_id", "team2_id",
                "match_date", "match_status"]

    @classmethod
    def get_by_id(cls, match_id: int):
        db = Database()
        query = "SELECT * FROM matches WHERE match_id = %s"
        result = db.fetch_query(query, (match_id,))
        return cls(*result[0]) if result else None
