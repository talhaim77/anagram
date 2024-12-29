import pytest
from httpx import AsyncClient

from backend.utils.string_utils import compute_letter_frequency
from backend.settings import settings

BASE_URL = f"http://localhost:8000/api/{settings.API_VERSION}/"


@pytest.mark.asyncio
async def test_get_stats():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "totalWords" in data
    assert "totalRequests" in data
    assert "avgProcessingTimeMs" in data


@pytest.mark.asyncio
@pytest.mark.parametrize("word, expected_anagrams", [
    ("apple", ["appel", "pepla"]),
    ("cloud", ["could"]),
    ("chip", ["pich"]),
])
async def test_get_similar_words(word: str, expected_anagrams: list):
    params = {"word": word}

    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/similar", params=params)

    if response.status_code == 200:
        similar_words = response.json().get("similar")
        assert isinstance(similar_words, list)

        input_signature = compute_letter_frequency(word)
        print(similar_words)
        for similar_word in similar_words:
            assert compute_letter_frequency(similar_word) == input_signature

        assert set(similar_words) == set(expected_anagrams)

    else:
        assert response.status_code == 404
        assert response.json().get("detail") == "Similar words not found"
