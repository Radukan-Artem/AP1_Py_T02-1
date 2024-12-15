import os
import asyncio
from enum import Enum
from prettytable import PrettyTable
import httpx
import uuid
from aioconsole import ainput


class StatusFile(Enum):
    Expectation = "Ожидание"
    Error = "Ошибка"
    Success = "Успех"

class FileInfo():
    def __init__(self, new_link):
        self.link = new_link
        self.status = StatusFile.Expectation

async def download_file(file_info, path):
    # print("!!!!")
    # await asyncio.sleep(3)
    async with httpx.AsyncClient() as session:
        try:
            resp = await session.get(file_info.link)
            resp.raise_for_status()
            path += "/" + f'{uuid.uuid1()}.jpg'
            file_info.status = StatusFile.Success
            with open(path, 'wb') as f:
                f.write(resp.content)
        except:
            file_info.status = StatusFile.Error

def print_table(list_files):
    clear = lambda: os.system('clear')
    clear()
    
    columns = ["Ссылка", "Статус"]
    table_files = PrettyTable(columns)
    
    for file in list_files:
        row = [file.link, file.status.value]
        table_files.add_row(row)
    print(table_files)

async def main():
    path = input()

    while os.path.exists(path) == False:
        print("Папки не существует")
        path = input()

    list_files = []
    link = input()
    tasks = []
   
    while link != "":
        new_file = FileInfo(link)
        list_files.append(new_file)

        task = asyncio.create_task(download_file(new_file, path))
        tasks.append(task)

        link = await ainput()

    print("Идет скачивание файлов")
    await asyncio.gather(*tasks)
    print_table(list_files)

if __name__ == "__main__":
    asyncio.run(main())