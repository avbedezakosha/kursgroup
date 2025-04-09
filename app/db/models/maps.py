from app.db.database import Database


class Maps:
    def __init__(self, map_id: int, map_name: str, image: bytearray or None) -> None:
        self.map_id = map_id
        self.map_name = map_name
        self.image = image

    def save(self) -> None:
        db: Database = Database()
        query: str = """
            INSERT INTO maps (map_name, image)
            VALUES (%s, %s)
        """
        db.execute_query(query, (
            self.map_name, self.image
        ))

    @classmethod
    def all(cls) -> list:
        db: Database = Database()
        query: str = """
            SELECT * FROM maps
        """
        return [cls(map_id=row[0], map_name=row[1], image=row[2]) for row in db.fetch_query(query)]

    @staticmethod
    def get_all_cols() -> list[str]:
        return ["map_id", "map_name", "image"]
