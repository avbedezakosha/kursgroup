import json
import os
from pathlib import Path

import psycopg
from contextlib import contextmanager
from config.config import DB_CONFIG, USE_MOCK_DATA


class Database:
    def __init__(self):
        # под релиз снос
        self.mock_mode = USE_MOCK_DATA
        self.mock_file = Path(__file__).parent / "data" / "mock_data.json"
        self._init_mock_file()

    def _init_mock_file(self):
        # под релиз снос
        if not self.mock_file.exists():
            self.mock_file.parent.mkdir(exist_ok=True)
            with open(self.mock_file, "w") as f:
                json.dump({"players": [], "teams": [], "matches": []}, f)

    @contextmanager
    def get_connection(self):
        if self.mock_mode:
            yield None
        else:
            conn = psycopg.connect(**DB_CONFIG)
            try:
                yield conn
            finally:
                conn.close()
        # conn = psycopg.connect(**DB_CONFIG)
        # try:
        #     yield conn
        # finally:
        #     conn.close()

    def execute_query(self, query, params=None):
        if self.mock_mode:
            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params or ())
                        conn.commit()
                        return cursor.rowcount
            except psycopg.Error as e:
                conn.rollback()
                return -1
            except Exception as e:
                return -1
        else:
            self._mock_execute(query, params)
        # try:
        #     with self.get_connection() as conn:
        #         with conn.cursor() as cursor:
        #             cursor.execute(query, params or ())
        #             conn.commit()
        #             return cursor.rowcount
        # except psycopg.Error as e:
        #     print(f"Database error: {e}")
        #     conn.rollback()
        #     return -1
        # except Exception as e:
        #     print(f"General error: {e}")
        #     return -1

    def fetch_query(self, query, params=None):
        if self.mock_mode:
            return self._mock_fetch(query, params or ())
        else:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params or ())
                    return cursor.fetchall()

        # with self.get_connection() as conn:
        #     with conn.cursor() as cursor:
        #         cursor.execute(query, params or ())
        #         return cursor.fetchall()

    # под релиз снос
    def _mock_execute(self, query: str, params) -> int:
        data = self._load_mock_data()
        table = self._detect_table(query)

        if "INSERT" in query:
            new_id = max([item[f"{table}_id"] for item in data[table]] or [0]) + 1
            data[table].append({"id": new_id, **dict(params)})
            self._save_mock_data(data)
            return 1

        elif "DELETE" in query:
            ids_to_delete = [params[0]] if params else []
            data[table] = [item for item in data[table] if item[f"{table}_id"] not in ids_to_delete]
            self._save_mock_data(data)
            return len(ids_to_delete)

        return 0

    def _mock_fetch(self, query: str, params) -> list[tuple]:
        data = self._load_mock_data()
        table = self._detect_table(query)
        results = data.get(table, [])

        # обработка параметров запроса
        limit = None
        offset = 0

        # обработка LIMIT/OFFSET
        if params and len(params) >= 1:
            if "LIMIT" in query and "OFFSET" in query:
                limit = int(params[0])
                offset = int(params[1])
            elif "LIMIT" in query:
                limit = int(params[0])

        # фильтрация по WHERE
        if "WHERE" in query:
            where_clause = query.split("WHERE")[1].split("LIMIT")[0] if "LIMIT" in query else query.split("WHERE")[
                1]
            field = where_clause.split()[0].strip()
            value = params[0] if params else None
            if value:
                results = [item for item in results if str(item.get(field, "")) == str(value)]

        # пагинация
        if limit is not None:
            results = results[offset:offset + limit]

        # в кортежи
        if table == "matches":
            return [
                (
                    item["match_id"],
                    item.get("map_id", None),
                    item["team1_id"],
                    item["team2_id"],
                    item["match_date"],
                    item["match_status"],
                    item["team1_score"],
                    item["team2_score"]
                ) for item in results
            ]
        elif table == "teams":
            return [
                (
                    item["team_id"],
                    item["team_name"],
                    item.get("logo", ""),
                    item["country"]
                ) for item in results
            ]
        elif table == "players":
            return [
                (
                    item["player_id"],
                    item["nickname"],
                    item.get("first_last_name", None),
                    item["email"],
                    item.get("phone", None),
                    item.get("country", None),
                    item.get("date_of_birth", None),
                    item["steam_id"],
                    item.get("avatar", None)
                ) for item in results
            ]
        elif table == "maps":
            return [
                (
                    item["map_id"],
                    item["map_name"],
                    item["image"]
                ) for item in results
            ]
        elif table == "current_lineups":
            return [
                (
                    item["lineup_id"],
                    item["player_id"],
                    item["team_id"]
                ) for item in results
            ]
        elif table == "match_lineups":
            return [
                (
                    item["lineup_id"],
                    item["match_id"],
                    item["player_id"],
                    item["team_id"]
                ) for item in results
            ]
        return []

    def _detect_table(self, query: str) -> str:
        query = query.lower()
        if "from players" in query: return "players"
        if "from teams" in query: return "teams"
        if "from matches" in query: return "matches"
        if "from current_lineups" in query: return "current_lineups"
        if "from match_lineups" in query: return "match_lineups"
        if "from maps" in query: return "maps"
        raise ValueError("Unknown table in query")

    def _load_mock_data(self) -> dict:
        with open(self.mock_file, "r", encoding='utf-8') as f:
            return json.load(f)

    def _save_mock_data(self, data: dict):
        with open(self.mock_file, "w") as f:
            json.dump(data, f, indent=2)
