import aiohttp

from src.core.exceptions import BookServiceError


async def search(q: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.googleapis.com/books/v1/volumes", params={"q": q}
        ) as resp:
            if not resp.status == 200:
                raise BookServiceError(resp.status, "bad request")
            data = (await resp.json()).get("items")
            if not data:
                raise BookServiceError(404, "no search results")

            keys_ = ["authors", "categories", "description", "title"]
            data = []
            uniques = set()

            for item in data:
                volume = item.get("volumeInfo")

                if not all(key in volume for key in keys_):
                    continue

                unique_check = (
                    volume["title"].lower() + " " + volume["authors"][0].lower()
                )
                print(unique_check)
                if unique_check not in uniques:
                    print(unique_check not in uniques)
                    data.append(
                        {"id": item["id"]} | {key: volume[key] for key in keys_}
                    )
                    uniques.add(unique_check)
            return data


async def get_book_by_id(id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.googleapis.com/books/v1/volumes/{id}') as resp:
            
            if not resp.status == 200:
                raise BookServiceError(resp.status, 'bad request')
            
            data = (await resp.json())
            volume = data.get("volumeInfo")
            keys_ = ["authors", "categories", "description", "title"]
            return {"id": data["id"]} | {key: volume[key] for key in keys_}