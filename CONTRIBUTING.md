# Contributing to Cars360

Thank you for your interest in contributing to Cars360! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, browser, versions)
   - Screenshots or error logs if applicable

### Submitting Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow the coding standards** outlined below
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

## 🛠 Development Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+ and pip
- PostgreSQL 12+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/muhsinmuhammad/Cars360.git
cd Cars360

# Install dependencies
npm run setup

# Start development servers
npm run dev
```

## 📝 Coding Standards

### Frontend (TypeScript/React)

- Use TypeScript for all new code
- Follow React best practices and hooks patterns
- Use Tailwind CSS for styling
- Implement responsive design
- Add proper error handling

### Backend (Python/FastAPI)

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Implement proper error handling
- Add input validation

### Smart Contracts (Clarity)

- Follow Clarity best practices
- Add comprehensive comments
- Implement proper error handling
- Write thorough tests

## 🧪 Testing

### Running Tests

```bash
# Frontend tests
cd frontend && npm test

# Backend tests
cd backend && pytest

# Smart contract tests
cd blockchain && clarinet test
```

### Test Requirements

- Write unit tests for new functions
- Add integration tests for API endpoints
- Include end-to-end tests for user flows
- Maintain test coverage above 80%

## 📚 Documentation

### Code Documentation

- Add JSDoc comments for TypeScript functions
- Write docstrings for Python functions
- Comment complex logic and algorithms
- Update README.md for new features

### API Documentation

- Document all API endpoints
- Include request/response examples
- Update OpenAPI specifications
- Add error code documentation

## 🔄 Pull Request Process

1. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Test thoroughly** and ensure all tests pass

4. **Update documentation** as needed

5. **Commit with clear messages**
   ```bash
   git commit -m "feat: add dataset filtering functionality"
   ```

6. **Push to your fork** and create a pull request

7. **Respond to feedback** and make requested changes

## 📋 Commit Message Guidelines

Use conventional commit format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

Examples:
```
feat: add user authentication system
fix: resolve dataset upload validation issue
docs: update API documentation
```

## 🏷 Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `priority: high` - High priority issues

## 🌟 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

## 📞 Getting Help

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Email** - muhammad.m1601550@st.futminna.edu.ng

## 📄 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at muhammad.m1601550@st.futminna.edu.ng.

## 📜 License

By contributing to Cars360, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Cars360! 🚗💎
