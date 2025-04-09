import datetime

from app.db.database import Database


class Players:
    def __init__(self, player_id: int, nickname: str, first_name: str or None, last_name: str or None,
                 email: str, phone: str or None, country: str or None,
                 date_of_birth: datetime.date or None, steam_id: str, profile_picture: bytearray or None) -> None:
        self.player_id = player_id
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.country = country
        self.date_of_birth = date_of_birth
        self.steam_id = steam_id
        self.profile_picture = profile_picture

    def save(self) -> None:
        db: Database = Database()
        query: str = """
            INSERT INTO players (nickname, first_name, last_name, 
                email, phone, country, date_of_birth, steam_id, profile_picture)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.execute_query(query, (
            self.nickname, self.first_name, self.last_name, self.email,
            self.phone, self.country, self.date_of_birth, self.steam_id, self.profile_picture
        ))

    @classmethod
    def all(cls) -> list:
        db: Database = Database()
        query: str = """
            SELECT * FROM players
        """
        return [cls(player_id=row[0], nickname=row[1], first_name=row[2], last_name=row[3], email=row[4], phone=row[5],
                    country=row[6], date_of_birth=row[7], steam_id=row[8], profile_picture=row[9]) for row in
                db.fetch_query(query)]

    @staticmethod
    def get_all_cols() -> list[str]:
        return ["nickname", "first_name", "last_name",
                "email", "phone", "country", "date_of_birth",
                "steam_id", "profile_picture"]

    @classmethod
    def count_by_team(cls, team_id: int):
        db = Database()
        query = "SELECT COUNT(*) FROM players WHERE team_id = %s"
        result = db.fetch_query(query, (team_id,))
        return result[0][0] if result else 0

    @classmethod
    def get_by_id(cls, player_id: int):
        db = Database()
        query = "SELECT * FROM players WHERE player_id = %s"
        result = db.fetch_query(query, (player_id,))
        return cls(*result[0]) if result else None
