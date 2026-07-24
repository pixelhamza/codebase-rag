from src.pipeline import answer

while True:
    query = input("Ask> ")

    if query.lower() == "exit":
        break

    result = answer(query)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:")
    for chunk in result["sources"]:
        print(f"- {chunk['qualified_name']} ({chunk['id']})")