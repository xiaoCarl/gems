import sys
from dotenv import load_dotenv

# Load environment variables BEFORE importing any gems modules
load_dotenv()

from gems.agent import Agent
from gems.gli.terminal import GLITerminal, get_gli
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory


def main():
    # Initialize the GLI system
    gli = get_gli()
    
    # Show welcome screen
    gli.show_welcome()
    
    # Initialize agent
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
                gli.show_info("再见!")
                break
            if query:
                # Start live display for this query
                gli.start_live_display()
                try:
                    agent.run(query)
                finally:
                    # Stop live display after processing
                    gli.stop_live_display()
        except (KeyboardInterrupt, EOFError):
            gli.show_info("\n再见!")
            break


if __name__ == "__main__":
    main()
