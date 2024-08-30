import httpx
from fastapi import HTTPException

from core.config import settings


async def check_spelling(texts: list[str]) -> list[str]:
    corrected_texts = []
    async with httpx.AsyncClient() as client:
        for text in texts:
            response = await client.get(
                url=settings.spell.url,
                params={"text": text, "lang": "ru"},
            )
            if response.status_code == 200:
                corrections = response.json()
                corrected_text = text

                for correction in corrections:
                    start, end, suggestion = (
                        correction["pos"],
                        correction["len"],
                        correction["s"],
                    )
                    if suggestion:
                        corrected_text = (
                            corrected_text[:start]
                            + suggestion[0]
                            + corrected_text[start + end:]
                        )

                corrected_texts.append(corrected_text)
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при обращении к API",
                )
    return corrected_texts
