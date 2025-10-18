# Agent Guidelines for Gems

## Commands
- **Install**: `uv sync`
- **Run**: `uv run gems-agent`
- **Build**: No build step required (pure Python)
- **Test**: No test framework configured
- **Lint**: No linter configured
- **Format**: No formatter configured
- **Type Check**: Run `python -m mypy src/` to check types (errors present)

## Code Style
- **Imports**: Standard library → third-party → local modules
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Types**: Use type hints for all function parameters and return values
- **Error Handling**: Use try/except with specific exceptions, log errors appropriately
- **Docstrings**: Use triple quotes for function documentation
- **Constants**: UPPER_CASE for module-level constants
- **Structure**: Group related functionality in classes/methods
- **Dependencies**: Check pyproject.toml before adding new packages
- **Type Issues**: Fix type errors in agent.py (TOOLS access, AIMessage attributes)