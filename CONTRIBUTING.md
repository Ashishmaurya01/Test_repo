# Contributing to Deployment Agent

Thank you for your interest in contributing to the Deployment Agent project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/deployment-agent.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Install the package in development mode: `pip install -e .`

## Development Workflow

1. Create a new branch for your feature/fix: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Commit your changes with a descriptive message
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a pull request

## Code Style

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Use pytest fixtures for common test setup
- Mock external dependencies in tests

## Documentation

- Update documentation for any new features or changes
- Include examples in docstrings
- Update README.md if necessary

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation
3. Describe your changes in the PR description
4. Reference any related issues
5. Wait for review and address any feedback

## Questions?

If you have any questions, please open an issue or reach out to the maintainers. 