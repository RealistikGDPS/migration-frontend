from __future__ import annotations

from enum import Enum

from migration_frontend import hashes
from migration_frontend.repository import Repository


class ServiceError(Enum):
    PASSWORD_ALREADY_MIGRATED = 1  # Maybe Strings lolll
    PASSWORD_MISMATCH = 2
    USER_NOT_FOUND = 3

    @property
    def text(self) -> str:
        return _ERR_MAP[self]


_ERR_MAP = {
    ServiceError.PASSWORD_ALREADY_MIGRATED: "Your password may have already been migrated.",
    ServiceError.PASSWORD_MISMATCH: "You entered an incorrect password.",
    ServiceError.USER_NOT_FOUND: "The user with the given name was not found.",
}


async def migrate_password(
    repo: Repository,
    username: str,
    old_password: str,
    new_password: str,
) -> ServiceError | None:
    user_id = await repo.user_id_from_name(username)

    if user_id is None:
        return ServiceError.USER_NOT_FOUND

    old_creds = await repo.get_credentials_with_version(user_id, 1)

    if old_creds is None:
        return ServiceError.PASSWORD_ALREADY_MIGRATED

    if not await hashes.verify_password_version_1(old_creds.value, old_password):
        return ServiceError.PASSWORD_MISMATCH

    # Creating the gjp2 one.
    v2 = await hashes.hash_password_version_2(new_password)
    await repo.create_credentials(
        user_id,
        2,
        v2,
    )

    await repo.delete_credentials_with_id(old_creds.id)
