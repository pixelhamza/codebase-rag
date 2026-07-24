from src.repository.manager import RepositoryManager
from src.repository.loader import load_repository
from src.pipeline import answer

manager = RepositoryManager()

url = input("GitHub URL: ")

info = manager.prepare_repository(url)
repository = load_repository(info["directory"])

print("Repository ready!")

while True:
    query = input("Ask> ")

    if query == "exit":
        break

    result = answer(repository, query)
    print(result["answer"])