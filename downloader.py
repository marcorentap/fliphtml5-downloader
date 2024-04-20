import json
import aiohttp
import os
import random
import asyncio
import img2pdf


start = 1  # Starting page to download
end = 10  # Last page to download
bookID = "cmeau/oswz"  # The ID of the book
skipExisting = False  # Skip downloading existing file

folderName = bookID.replace("/", "-")


async def downloadImage(session, taskID, index_no):
    filepath = f"{folderName}/{index_no}.jpg"

    os.makedirs(folderName, exist_ok=True)

    URL = f"http://online.fliphtml5.com/{bookID}/files/large/{taskID}"

    with open("useragents.txt", "r") as f:
        useragents = [line.rstrip("\n") for line in f]

    useragent = useragents[random.randrange(0, len(useragents))]
    headers = {"User-Agent": useragent}
    print(f"[+] Downloading {URL}")
    async with session.get(URL, headers=headers) as r:
        with open(filepath, "wb") as f:
            f.write(await r.read())


def convert_images_to_pdf(folderName, start, end):
    print("Converting...")
    images = []
    for num in range(start, end):
        filepath = f"{folderName}/{num}.jpg"
        with open(filepath, "rb") as image:
            images.append(image.read())

    with open(f"{folderName}.pdf", "wb") as file:
        file.write(img2pdf.convert(images))

    print("\rFinished.")


async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        url = f"https://online.fliphtml5.com/{bookID}/javascript/config.js"
        async with session.get(url) as r:
            data = await r.text()
            data = data.replace("var htmlConfig = ", "")
            data = data[:-1]
            data = json.loads(data)
            fliphtml5_pages = data["fliphtml5_pages"]
            index_no = 0
            for i in fliphtml5_pages:
                for j in i["n"]:
                    image_path = f"{folderName}/{j}.jpg"
                    if not skipExisting or not os.path.exists(image_path):
                        await downloadImage(session, j, index_no)
                    index_no += 1
            convert_images_to_pdf(folderName, 0, index_no)


if __name__ == "__main__":
    asyncio.run(main())
