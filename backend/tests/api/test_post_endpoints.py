import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize("word", ["Python", "apple", "cloud", "Fastapi"])
async def test_add_word(word):
    payload = {"word": word}

    async with AsyncClient(base_url="http://localhost:8000/api/v1") as ac:
        response = await ac.post("/add-word", json=payload)

    if response.status_code == 200:
        assert response.json().get("message") == f"Word: {word} added successfully"
    elif response.status_code == 400:
        assert response.json().get("detail") == "Word already exists in database"
    else:
        assert response.status_code == 500
        assert "Failed to add word" in response.json().get("detail")
