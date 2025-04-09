from app.db.database import Database


class MatchLineups:
    def __init__(self, lineup_id: int, match_id: int or None, player_id: int or None,
                 team_id: int or None, position: int or None) -> None:
        self.lineup_id = lineup_id
        self.match_id = match_id
        self.player_id = player_id
        self.team_id = team_id
        self.position = position

    def save(self) -> None:
        db: Database = Database()
        query: str = """
            INSERT INTO match_lineups (match_id, player_id, team_id, position)
            VALUES (%s, %s, %s, %s)
        """
        db.execute_query(query, (
            self.match_id, self.player_id, self.team_id, self.position
        ))

    @classmethod
    def all(cls) -> list:
        db: Database = Database()
        query: str = """
            SELECT * FROM match_lineups
        """
        return [cls(lineup_id=row[0], match_id=row[1], player_id=row[2], team_id=row[3], position=row[4]) for row in db.fetch_query(query)]

    @staticmethod
    def get_all_cols() -> list[str]:
        return ["match_id", "player_id", "team_id", "position"]
