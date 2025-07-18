# Contributing to AspireHR

We love your input! We want to make contributing to AspireHR as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a new branch** for your feature or fix
4. **Make your changes** with clear commit messages
5. **Test your changes** thoroughly
6. **Submit a pull request** with a detailed description

## 📋 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Request Process

1. **Fork the repo** and create your branch from `main`
2. **Install dependencies** and set up development environment
3. **Make your changes** following our coding standards
4. **Add tests** for any new functionality
5. **Ensure all tests pass**
6. **Update documentation** if needed
7. **Submit a pull request**

### Branch Naming Convention

- **Features**: `feature/description-of-feature`
- **Bug fixes**: `fix/description-of-bug`
- **Documentation**: `docs/description-of-change`
- **Refactoring**: `refactor/description-of-refactor`

Example:
```bash
git checkout -b feature/employee-skill-matrix
git checkout -b fix/leave-allocation-bug
git checkout -b docs/api-documentation
```

## 🏗️ Development Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- Frappe Framework v14+
- Git

### Setup Steps

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/AspireHR.git
   cd AspireHR
   ```

2. **Set up development environment**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install in development mode
   pip install -e .
   ```

3. **Set up pre-commit hooks** (recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/
   ```

## 📝 Coding Standards

### Python Code Style

- Follow **PEP 8** guidelines
- Use **type hints** where appropriate
- Write **docstrings** for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

Example:
```python
def allocate_employee_leaves(
    employee: str,
    leave_type: str,
    allocation_date: str,
    new_leaves_allocated: float,
    carry_forward: bool = False
) -> dict:
    """
    Allocate leaves to an employee for a specific period.
    
    Args:
        employee: Employee ID
        leave_type: Type of leave to allocate
        allocation_date: Date from which allocation is effective
        new_leaves_allocated: Number of leaves to allocate
        carry_forward: Whether to carry forward unused leaves
    
    Returns:
        Dictionary containing allocation details
    """
    # Implementation here
    pass
```

### JavaScript Code Style

- Use **ES6+** syntax
- Follow **consistent indentation** (2 spaces)
- Use **camelCase** for variables and functions
- Write **JSDoc comments** for functions
- Use **const/let** instead of var

Example:
```javascript
/**
 * Show leave allocation dialog
 * @param {string} employee - Employee ID
 * @param {string} leaveType - Type of leave
 */
function showLeaveAllocationDialog(employee, leaveType) {
    // Implementation here
}
```

### File Organization

```
aspirehr/
├── api/              # API endpoints
├── human_resources/  # HR module
├── payroll/         # Payroll module
├── public/          # Frontend assets
├── tests/           # Test files
├── docs/            # Documentation
└── utils/           # Utility functions
```

## 🧪 Testing

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both positive and negative scenarios
- Include edge cases

Example:
```python
def test_leave_allocation_success():
    """Test successful leave allocation"""
    result = allocate_employee_leaves(
        employee="EMP-001",
        leave_type="Annual Leave",
        allocation_date="2024-01-01",
        new_leaves_allocated=21
    )
    assert result["status"] == "success"
    assert result["leaves_allocated"] == 21

def test_leave_allocation_invalid_employee():
    """Test leave allocation with invalid employee"""
    with pytest.raises(ValueError, match="Employee not found"):
        allocate_employee_leaves(
            employee="INVALID",
            leave_type="Annual Leave",
            allocation_date="2024-01-01",
            new_leaves_allocated=21
        )
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_leave_allocation.py

# Run with coverage
python -m pytest --cov=aspirehr

# Run integration tests
python -m pytest tests/integration/
```

## 📚 Documentation

### Code Documentation

- Write clear **docstrings** for all public functions
- Include **parameter descriptions** and **return types**
- Add **usage examples** for complex functions
- Document **exceptions** that may be raised

### API Documentation

- Document all **API endpoints**
- Include **request/response examples**
- Specify **authentication requirements**
- Document **error codes** and responses

### User Documentation

- Update **README.md** for new features
- Add **usage examples** and **screenshots**
- Update **API documentation** when needed
- Create **migration guides** for breaking changes

## 🐛 Bug Reports

We use GitHub Issues to track bugs. When reporting a bug:

### Before Submitting

1. **Check existing issues** to avoid duplicates
2. **Search the documentation** for solutions
3. **Test with the latest version**

### Bug Report Template

```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 91]
- AspireHR Version: [e.g. 1.0.0]
- Frappe Version: [e.g. 14.0.0]

## Additional Context
Any other context about the problem.
```

## 💡 Feature Requests

We welcome feature requests! Use GitHub Issues with the "feature request" label.

### Feature Request Template

```markdown
## Feature Summary
Brief description of the feature.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How would you like this feature to work?

## Alternatives Considered
Any alternative solutions you've considered.

## Additional Context
Any other context or screenshots.
```

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** and inclusive
- **Be patient** with newcomers
- **Be constructive** in feedback
- **Be collaborative** in discussions

### Communication

- Use **clear and concise** language
- Provide **context** for your contributions
- **Ask questions** when unsure
- **Help others** when possible

## 🏆 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Special mentions** in announcements

## 📞 Getting Help

If you need help:

1. **Check the documentation** first
2. **Search existing issues** on GitHub
3. **Ask in discussions** for general questions
4. **Create an issue** for bugs or feature requests
5. **Contact maintainers** for urgent matters

### Contact Information

- **Email**: suresh@innopay.com
- **GitHub Issues**: https://github.com/innopay-suresh/AspireHR/issues
- **Discussions**: https://github.com/innopay-suresh/AspireHR/discussions

## 📄 License

By contributing to AspireHR, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AspireHR! 🎉
