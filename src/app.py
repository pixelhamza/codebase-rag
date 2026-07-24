from src.repository.manager import RepositoryManager
from src.pipeline import answer

manager = RepositoryManager()

url = input("GitHub URL: ")

repo = manager.prepare_repository(url)

print("Repository ready!")

while True:
    query = input("Ask> ")

    if query == "exit":
        break

    result = answer(query)
    print(result["answer"])