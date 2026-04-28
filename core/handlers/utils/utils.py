import httpx

API_BASE = "https://anilibria.top/api/v1/"
ANILIBRIA_BASE = "https://anilibria.top"


async def search_releases(user_input: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_BASE + "anime/catalog/releases",
            params={"f[search]": user_input, "limit": 10},
        )
        response.raise_for_status()
        return response.json()["data"]


def get_anime_titles(releases: list[dict]) -> list[tuple[str, int]]:
    return [(r["name"]["main"], r["id"]) for r in releases]


def get_poster_url(release: dict) -> str:
    return ANILIBRIA_BASE + release["poster"]["src"]


def get_external_player_url(release: dict) -> str | None:
    url = release.get("external_player")
    if not url:
        return None
    return "https:" + url if url.startswith("//") else url
