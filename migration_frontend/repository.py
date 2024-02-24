from __future__ import annotations

from typing import NamedTuple

from migration_frontend.adapters.mysql import AbstractMySQLService


class UserCredentials(NamedTuple):
    id: int
    user_id: int
    version: int
    value: str


class Repository:
    __slots__ = ("sql",)

    def __init__(self, sql: AbstractMySQLService) -> None:
        self.sql = sql

    async def get_member_count(self) -> int:
        return await self.sql.fetch_val("SELECT COUNT(*) FROM users")

    async def get_credentials_with_version(
        self,
        user_id: int,
        version: int,
    ) -> UserCredentials | None:
        res = await self.sql.fetch_one(
            "SELECT * FROM user_credentials WHERE user_id = :user_id AND version = :version",
            {
                "user_id": user_id,
                "version": version,
            },
        )

        if res is None:
            return None

        return UserCredentials(**res)

    async def delete_credentials_with_id(self, credential_id: int) -> None:
        await self.sql.execute(
            "DELETE FROM user_credentials WHERE id = :id",
            {"id": credential_id},
        )

    async def create_credentials(
        self,
        user_id: int,
        version: int,
        value: str,
    ) -> UserCredentials:
        credentials_id = await self.sql.execute(
            "INSERT INTO user_credentials VALUES (NULL, :user_id, :version, :value)",
            {
                "user_id": user_id,
                "version": version,
                "value": value,
            },
        )

        return UserCredentials(
            credentials_id,
            user_id,
            version,
            value,
        )
