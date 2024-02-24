from __future__ import annotations

import asyncio
import hashlib

import bcrypt


def _compare_bcrypt(hashed: str, plain: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def _hash_bcypt(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


async def compare_bcrypt(hashed: str, plain: str) -> bool:
    return await asyncio.to_thread(_compare_bcrypt, hashed, plain)


async def hash_bcypt(plain: str) -> str:
    return await asyncio.to_thread(_hash_bcypt, plain)


def hash_sha1(plain: str) -> str:
    return hashlib.sha1(plain.encode()).hexdigest()


GJP2_PEPPER = "mI29fmAnxgTs"


def hash_gjp2(plain: str) -> str:
    return hashlib.sha1((plain + GJP2_PEPPER).encode()).hexdigest()


async def hash_password_version_2(plain: str) -> str:
    return await hash_bcypt(
        hash_gjp2(plain),
    )


verify_password_version_1 = compare_bcrypt
