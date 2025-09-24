# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```bash
# Install dependencies (uses uv for dependency management)
uv sync

# Install with development dependencies
uv sync --group dev
```

### Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=nilai_py --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_server.py

# Run specific test class
uv run pytest tests/test_server.py::TestDelegationTokenServer -v

# Run specific test method
uv run pytest tests/test_server.py::TestDelegationTokenServer::test_create_delegation_token_success -v
```

### Code Quality
```bash
# Run linter and formatter
uv run ruff check
uv run ruff format
```

### Running Examples
```bash
# Examples are located in the examples/ directory
python examples/0-api_key_mode.py
python examples/1-delegation_token_mode.py
python examples/2-streaming_mode.py
python examples/3-advanced_streaming.py
```

## Architecture

### Core Components

**Client (`src/nilai_py/client.py`)**
- OpenAI-compatible client extending `openai.Client`
- Supports two authentication modes: API_KEY and DELEGATION_TOKEN
- Handles NUC token creation and Nilai-specific authentication headers
- Manages root tokens (API key mode) and delegation tokens automatically

**DelegationTokenServer (`src/nilai_py/server.py`)**
- Server-side component for creating delegation tokens
- Manages root token lifecycle with automatic refresh on expiration
- Creates time-limited delegation tokens with configurable usage limits
- Handles NilAuth integration for secure token generation

**NilDB Prompt Manager (`src/nilai_py/nildb/__init__.py`)**
- Document management system for handling prompts in NilDB
- User setup and key management with SecretVaults integration
- CRUD operations for documents with delegation token authentication

### Authentication Flow

1. **API Key Mode**: Direct authentication using API key from nilpay.vercel.app
   - Client initializes with API key, creates root token via NilAuth
   - Root token is cached and auto-refreshed when expired
   - Invocation tokens created from root token for each request

2. **Delegation Token Mode**: Server-side token generation for enhanced security
   - Client generates temporary keypair and requests delegation
   - Server creates delegation token using its root token
   - Client uses delegation token to create invocation tokens for requests

### Key Dependencies

- `nuc`: NUC token creation and envelope handling
- `openai`: Base OpenAI client functionality
- `secretvaults`: Secure key storage for NilDB operations
- `httpx`: HTTP client for Nilai API communication
- `pydantic`: Data validation and serialization

### Configuration

**Environment Variables**
- `API_KEY`: API key for direct authentication mode
- `PRIVATE_KEY`: Server private key for delegation token creation

**NilAuth Instances**
- `SANDBOX`: https://nilauth.sandbox.app-cluster.sandbox.nilogy.xyz
- `PRODUCTION`: https://nilauth-cf7f.nillion.network/

### Testing Structure

- `tests/unit/`: Unit tests for individual components
- `tests/e2e/`: End-to-end integration tests
- Test coverage focused on DelegationTokenServer (100% coverage) and core functionality