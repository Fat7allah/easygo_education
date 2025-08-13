# Contributing to EasyGo Education

Thank you for your interest in contributing to EasyGo Education! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and professional in all interactions.

## Development Setup

1. Set up Frappe development environment
2. Install the app in development mode
3. Run tests before submitting changes

## Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools

### Examples

```
feat(scolarite): add student transfer functionality
fix(portal): resolve parent authentication issue
docs: update installation instructions
chore: update dependencies
```

## Version Bump Rules

- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (0.x.0): New features, backwards compatible
- **PATCH** (0.0.x): Bug fixes, backwards compatible

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes following the coding standards
3. Add tests for new functionality
4. Update documentation as needed
5. Ensure all tests pass
6. Update CHANGELOG.md with your changes
7. Submit a pull request with a clear description

## Coding Standards

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Use `black` for code formatting
- Use `ruff` for linting
- Maintain test coverage above 80%

## Testing

Run the test suite before submitting:

```bash
make test
```

## Questions?

Feel free to open an issue for any questions or discussions.
