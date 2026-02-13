from orchestrator.router import handle_query

def main():
    print("Jarvis system started...\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = handle_query(user_input)
        print("\nJarvis:", response, "\n")

if __name__ == "__main__":
    main()