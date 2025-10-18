import sys
from dotenv import load_dotenv

# Load environment variables BEFORE importing any gems modules
load_dotenv()

from gems.agent import Agent
from gems.utils.intro import print_intro
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

def main():
    print_intro()
    agent = Agent()

    # Check if running in interactive terminal
    if sys.stdin.isatty():
        # Create a prompt session with history support for interactive terminals
        session = PromptSession(history=InMemoryHistory())
        prompt_func = lambda: session.prompt(">> ")
    else:
        # Use simple input for non-interactive environments
        prompt_func = lambda: input(">> ")

    while True:
        try:
            query = prompt_func()
            if query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if query:
                agent.run(query)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
