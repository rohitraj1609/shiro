"""
Entry point script.

Keeps the CLI at the project root while all implementation
lives under the `voice` package.
"""

from voice.app import main_menu


if __name__ == "__main__":
    main_menu()


