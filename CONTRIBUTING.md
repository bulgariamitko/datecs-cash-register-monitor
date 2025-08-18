# Contributing to Datecs Cash Register Monitor

Thank you for your interest in contributing to the Datecs Cash Register Monitor! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Windows 10/11 (for full functionality)
- Git

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/datecs-cash-register-monitor.git
   cd datecs-cash-register-monitor
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install development dependencies:
   ```bash
   pip install pytest black flake8 pyinstaller
   ```

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/dimitarklaturov/datecs-cash-register-monitor/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (Windows version, Python version)
   - Screenshots if applicable

### Suggesting Features

1. Check existing [Issues](https://github.com/dimitarklaturov/datecs-cash-register-monitor/issues) for similar requests
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

1. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes**:
   ```bash
   python cash_register_monitor/main.py --test-connection
   ```

4. **Format your code**:
   ```bash
   black .
   flake8 .
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Code Organization
- Keep functions focused and small
- Use descriptive variable and function names
- Add docstrings for classes and functions
- Follow the existing project structure

### Example:
```python
def test_connection(ip: str, port: int, timeout: int = 3) -> bool:
    """Test TCP connection to specified address.
    
    Args:
        ip: Target IP address
        port: Target port number
        timeout: Connection timeout in seconds
        
    Returns:
        True if connection successful, False otherwise
    """
    # Implementation here
```

## Testing

### Manual Testing
- Test on Windows 10/11
- Verify system tray functionality
- Test settings persistence
- Check startup integration

### Adding Tests
- Add unit tests for new functions
- Test error handling scenarios
- Verify configuration validation

## Documentation

- Update README.md for new features
- Add inline comments for complex logic
- Update docstrings for API changes

## Areas for Contribution

### High Priority
- **Multi-language support** (internationalization)
- **Dark mode** support
- **Connection logging** and history
- **Multiple cash register** monitoring
- **Sound notifications** for connection status changes

### Medium Priority
- **Configuration backup/restore**
- **Portable version** (no installation required)
- **Custom tray icon** upload
- **Connection statistics** dashboard

### Low Priority
- **Email notifications** for extended downtime
- **REST API** for external monitoring
- **Plugin system** for extensibility

## Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive

### PR Description Should Include
- Summary of changes
- Related issue number (if applicable)
- Testing performed
- Screenshots (for UI changes)

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Getting Help

- Create an issue for questions
- Check existing documentation
- Review similar projects for patterns

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help maintain a welcoming environment

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make Datecs Cash Register Monitor better for everyone!