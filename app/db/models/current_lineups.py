from app.db.database import Database


class CurrentLineups:
    def __init__(self, lineup_id: int, player_id: int or None,
                 team_id: int or None) -> None:
        self.lineup_id = lineup_id
        self.player_id = player_id
        self.team_id = team_id

    def save(self) -> None:
        db: Database = Database()
        query: str = """
            INSERT INTO project25.currentlineups (player_id, team_id)
            VALUES (%s, %s)
        """
        db.execute_query(query, (
            self.player_id, self.team_id
        ))

    @classmethod
    def all(cls) -> list:
        db: Database = Database()
        query: str = """
            SELECT * FROM project25.currentlineups
        """
        return [cls(lineup_id=row[0], player_id=row[1], team_id=row[2]) for row in db.fetch_query(query)]

    @staticmethod
    def get_all_cols() -> list[str]:
        return ["player_id", "team_id", ""]
