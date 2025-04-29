import datetime

from app.db.database import Database


class Players:
    def __init__(self, player_id: int, nickname: str, first_last_name: str or None,
                 email: str, phone: str or None, country: str or None,
                 date_of_birth: datetime.date or None, steam_id: str, avatar: bytearray or None) -> None:
        self.player_id = player_id
        self.nickname = nickname
        self.first_last_name = first_last_name
        self.email = email
        self.phone = phone
        self.country = country
        self.date_of_birth = date_of_birth
        self.steam_id = steam_id
        self.avatar = avatar

    def save(self) -> None:
        db: Database = Database()
        query: str = """
            INSERT INTO players (nickname, first_last_name, 
                email, phone, country, date_of_birth, steam_id, avatar)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        db.execute_query(query, (
            self.nickname, self.first_last_name, self.email,
            self.phone, self.country, self.date_of_birth, self.steam_id, self.avatar
        ))

    @classmethod
    def all(cls) -> list:
        db: Database = Database()
        query: str = """
            SELECT * FROM project25.players
        """
        return [cls(nickname=row[0], first_last_name=row[1], email=row[2], country=row[3],
                    phone=row[4], date_of_birth=row[5], steam_id=row[6], avatar=row[7], player_id=row[8]) for row in
                db.fetch_query(query)]

    @staticmethod
    def get_all_cols() -> list[str]:
        return ["nickname", "first_last_name",
                "email", "phone", "country", "date_of_birth",
                "steam_id", "avatar"]

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
