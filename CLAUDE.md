# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gems is an autonomous value investment research agent for Chinese stock market analysis (A-shares and Hong Kong stocks). It uses AI to perform financial analysis through task planning, data collection, and investment report generation.

## Development Commands

### Setup and Installation
```bash
# Install from source (recommended for development)
uv sync

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running the Application
```bash
# CLI mode
uv run gems-agent

# Web interface
./start-web.sh
# or
uv run python server.py
```

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v --tb=short

# Run specific test file
pytest tests/test_core_modules.py
```

### Code Quality
```bash
# Type checking
mypy src/

# Code formatting
black src/ tests/

# Linting
ruff check src/ tests/

# Import sorting
isort src/ tests/
```

## Architecture Overview

### Core Components

1. **Data Source Abstraction Layer** (`src/gems/data_sources/`)
   - `DataSourceManager` automatically selects optimal data sources based on stock type
   - A-shares: Primary uses configured source (TDX/AkShare), fallback to AkShare
   - Hong Kong stocks: Primary uses yfinance, fallback to AkShare
   - Financial data: Always uses AkShare for both markets

2. **AI Agent System** (`src/gems/agent.py`)
   - Uses LangChain for task planning and execution
   - Supports DeepSeek (default) and Qwen models
   - Implements value investment framework: "good business + good price"

3. **Tool System** (`src/gems/tools/`)
   - LangChain tools for financial data retrieval and analysis
   - `financials.py`: Core financial data tools
   - `analysis.py`: Investment analysis tools
   - `tdx_api.py`: Tongdaxin real-time data integration

4. **Unified API** (`src/gems/api.py`)
   - Single entry point for all data operations
   - Handles data source selection and error management
   - Provides consistent interface regardless of underlying source

### Key Design Patterns

- **Error Handling**: Custom exception hierarchy (`GemsError` → specific errors like `DataSourceError`, `FinancialDataError`)
- **Logging**: Structured logging with `get_logger()` providing consistent format and context
- **Configuration**: Environment-based config with validation in `config.py`
- **Caching**: Hybrid cache system for performance optimization

### Environment Configuration

Required environment variables (copy from `env.example` to `.env`):
```bash
# For DeepSeek (default)
DEEPSEEK_API_KEY=your-key

# For Qwen (alternative)
USE_QWEN=true
DASHSCOPE_API_KEY=your-key

# Optional configurations
PREFERRED_DATA_SOURCE=tdx  # or akshare
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

### Adding New Features

1. **New Data Source**: Implement `DataSource` abstract base class in `data_sources/`, register in `manager.py`
2. **New Analysis Tool**: Create LangChain tool in `tools/`, follow existing patterns for error handling and logging
3. **New Model Support**: Add model configuration in `model.py`, update `agent.py` if needed

### Testing Guidelines

- Unit tests go in `tests/test_*.py`
- Use `mock_model.py` for testing without API calls
- Test files should follow `test_<module_name>.py` naming
- Focus on testing core business logic and error handling

### Common Development Tasks

When modifying data source logic:
1. Check `DataSourceManager` selection strategy
2. Test with both A-share and Hong Kong stock symbols
3. Verify fallback mechanisms work correctly

When updating analysis tools:
1. Ensure proper error handling with custom exceptions
2. Add structured logging for debugging
3. Test integration with the agent system

When working with the web interface:
1. Web files are in `web/` directory
2. FastAPI server entry point is `server.py`
3. WebSocket communication for real-time updates