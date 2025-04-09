from app.db.database import Database


class Teams:
    def __init__(self, team_id: int, team_name: str, logo: str or None, captain_id: int or None) -> None:
        self.team_id = team_id
        self.team_name = team_name
        self.logo = logo
        self.captain_id = captain_id

    def save(self) -> None:
        db: Database = Database()
        query: str = """
            INSERT INTO teams (team_name, logo, captain_id)
            VALUES (%s, %s, %s)
        """
        db.execute_query(query, (
            self.team_name, self.logo, self.captain_id
        ))

    @classmethod
    def all(cls) -> list:
        db: Database = Database()
        query: str = """
            SELECT * FROM teams
        """
        return [cls(team_id=row[0], team_name=row[1], logo=row[2], captain_id=row[3]) for row in db.fetch_query(query)]

    @staticmethod
    def get_all_cols() -> list[str]:
        return ["team_name", "logo", "captain_id"]

    @classmethod
    def get_by_id(cls, team_id: int):
        db = Database()
        query = "SELECT * FROM teams WHERE team_id = %s"
        result = db.fetch_query(query, (team_id,))
        return cls(*result[0]) if result else None
