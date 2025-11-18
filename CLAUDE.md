# CLAUDE.md - AI Assistant Guide for BDO-T5

**Last Updated:** 2025-11-18
**Repository:** LoadGalax/BDO-T5
**Current State:** Initial setup phase

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Development Workflow](#development-workflow)
4. [Git Conventions](#git-conventions)
5. [Code Conventions](#code-conventions)
6. [AI Assistant Guidelines](#ai-assistant-guidelines)
7. [Testing Strategy](#testing-strategy)
8. [Deployment](#deployment)
9. [Common Tasks](#common-tasks)

---

## Project Overview

### What is BDO-T5?

BDO-T5 appears to be a project related to Black Desert Online (BDO), potentially involving T5 model architecture for image processing, text generation, or game-related assistance.

### Current Project State

- **Status:** Initial setup/scaffolding phase
- **Primary Language:** To be determined
- **Framework/Stack:** To be determined
- **Dependencies:** None yet configured

### Project Goals

*To be documented as the project develops*

---

## Repository Structure

```
BDO-T5/
├── .git/                  # Git version control
├── init.txt              # Initial repository marker
└── CLAUDE.md            # This file - AI assistant guide
```

### Expected Future Structure

As the project develops, the following structure is recommended:

```
BDO-T5/
├── src/                  # Source code
│   ├── models/          # Model definitions (T5, etc.)
│   ├── data/            # Data processing utilities
│   ├── utils/           # Helper functions
│   └── main.py/js/ts    # Entry point
├── tests/               # Test files
├── docs/                # Additional documentation
├── data/                # Data files (gitignored)
├── config/              # Configuration files
├── scripts/             # Utility scripts
├── requirements.txt     # Python dependencies (if Python)
├── package.json         # Node dependencies (if Node.js)
├── README.md           # Project overview and setup
├── CLAUDE.md           # This file
└── .gitignore          # Git ignore rules
```

---

## Development Workflow

### Branch Strategy

This repository uses feature branches with the `claude/` prefix:

- **Branch naming:** `claude/<feature-description>-<session-id>`
- **Current branch:** `claude/claude-md-mi4618d3oigvdms2-01Wo4GXG7zc7js6MyoQJ1d2a`
- **Previous branches:**
  - `claude/black-desert-image-assistant-018uLdrjPMCQEqJrKbngYWse`

### Development Process

1. **Branch Creation:** Create feature branches from the main branch
2. **Development:** Make changes on the feature branch
3. **Commit:** Use descriptive commit messages
4. **Push:** Push to origin with `git push -u origin <branch-name>`
5. **PR Creation:** Create pull request when feature is complete
6. **Code Review:** (If applicable) Review before merging
7. **Merge:** Merge to main branch after approval

---

## Git Conventions

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**
```
feat(model): add T5 model integration
fix(data): resolve data loading issue
docs(readme): update installation instructions
```

### Branch Naming

- Feature branches: `claude/<feature-description>-<session-id>`
- All development branches must start with `claude/` prefix
- Use kebab-case for descriptions
- Session IDs are automatically appended

### Git Operations Best Practices

**Pushing:**
```bash
git push -u origin <branch-name>
```
- Always use `-u` flag for first push
- Retry up to 4 times with exponential backoff on network errors (2s, 4s, 8s, 16s)
- Branch must start with `claude/` or push will fail with 403

**Fetching:**
```bash
git fetch origin <branch-name>
git pull origin <branch-name>
```
- Prefer fetching specific branches
- Retry up to 4 times on network failures

---

## Code Conventions

### General Principles

1. **Readability:** Code should be self-documenting
2. **Modularity:** Keep functions/classes focused and single-purpose
3. **DRY:** Don't Repeat Yourself
4. **KISS:** Keep It Simple, Stupid
5. **Security:** Always consider security implications (avoid XSS, SQL injection, command injection, etc.)

### Python Conventions (if applicable)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 88 characters (Black formatter)
- Use docstrings for functions and classes
- Use `snake_case` for variables and functions
- Use `PascalCase` for classes

### JavaScript/TypeScript Conventions (if applicable)

- Follow Airbnb style guide or similar
- Use ESLint and Prettier
- Use `camelCase` for variables and functions
- Use `PascalCase` for classes and components
- Use `UPPER_CASE` for constants
- Prefer `const` over `let`, avoid `var`

### File Naming

- Use lowercase with hyphens for file names: `model-loader.py`
- Test files: `test_<module_name>.py` or `<module_name>.test.js`
- Config files: Clear, descriptive names

---

## AI Assistant Guidelines

### When Working on This Repository

1. **Always Check Current State:**
   - Run `git status` before making changes
   - Check current branch with `git branch`
   - Verify you're on the correct feature branch

2. **Use Todo Lists:**
   - For multi-step tasks, use the TodoWrite tool
   - Break down complex tasks into smaller steps
   - Mark tasks as completed immediately after finishing

3. **Code Quality:**
   - Never introduce security vulnerabilities
   - Write clean, maintainable code
   - Add comments for complex logic
   - Follow established conventions

4. **Git Operations:**
   - Commit related changes together
   - Write descriptive commit messages
   - Push to the correct branch
   - Never force push without explicit user permission

5. **Documentation:**
   - Update CLAUDE.md when project structure changes
   - Keep README.md current
   - Document new features and APIs
   - Add inline comments for complex code

6. **Testing:**
   - Write tests for new features
   - Run existing tests before committing
   - Fix failing tests immediately

### Common Pitfalls to Avoid

- ❌ Don't commit without clear commit messages
- ❌ Don't push to wrong branches
- ❌ Don't create files unnecessarily (prefer editing existing)
- ❌ Don't ignore security vulnerabilities
- ❌ Don't use emojis unless explicitly requested
- ❌ Don't create documentation files unless necessary
- ❌ Don't skip the TodoWrite tool for complex tasks

### Helpful Commands

```bash
# Check repository status
git status
git log --oneline --graph | head -20

# Branch management
git branch -a
git checkout -b <branch-name>

# View changes
git diff
git diff --staged

# Explore codebase (use appropriate tools)
# For file search: Use Glob tool
# For content search: Use Grep tool
# For reading files: Use Read tool
# For editing files: Use Edit tool
```

---

## Testing Strategy

### Test Framework

*To be determined based on project language and requirements*

### Test Coverage

- Aim for >80% code coverage
- Focus on critical paths and edge cases
- Test both success and failure scenarios

### Running Tests

```bash
# To be documented when test framework is set up
# Example: pytest tests/
# Example: npm test
```

### Test Organization

- Unit tests: Test individual functions/methods
- Integration tests: Test component interactions
- E2E tests: Test complete workflows (if applicable)

---

## Deployment

### Environment Setup

*To be documented as deployment strategy is established*

### Build Process

*To be documented when build process is configured*

### Deployment Steps

*To be documented when deployment pipeline is set up*

---

## Common Tasks

### Adding a New Feature

1. Create feature branch: `git checkout -b claude/<feature-name>-<session-id>`
2. Use TodoWrite to plan implementation steps
3. Implement feature following code conventions
4. Write/update tests
5. Update documentation
6. Commit changes with descriptive message
7. Push to remote: `git push -u origin <branch-name>`
8. Create pull request (if applicable)

### Fixing a Bug

1. Ensure on correct branch
2. Identify root cause
3. Write test that reproduces bug (if applicable)
4. Fix the bug
5. Verify fix with tests
6. Commit and push

### Updating Documentation

1. Make changes to relevant .md files
2. Update CLAUDE.md if structure changes
3. Commit with `docs:` prefix
4. Push changes

### Refactoring Code

1. Use TodoWrite to plan refactoring steps
2. Ensure tests exist and pass
3. Refactor incrementally
4. Run tests after each change
5. Commit with `refactor:` prefix

---

## Project-Specific Notes

### BDO (Black Desert Online) Context

This project appears to be related to Black Desert Online. When working with BDO-related features:

- Understand the game context if implementing game-specific features
- Be aware of game terminology and mechanics
- Consider user experience for BDO players

### T5 Model Architecture

If using T5 (Text-to-Text Transfer Transformer):

- Document model versions used
- Track training data and parameters
- Consider model size and performance trade-offs
- Document inference requirements

### Image Processing

Based on branch history mentioning "image-assistant":

- Follow best practices for image handling
- Consider memory usage for large images
- Document supported image formats
- Implement proper error handling for corrupted images

---

## Questions or Issues?

When encountering unclear requirements or ambiguities:

1. **Check existing documentation** in README.md and this file
2. **Ask the user** for clarification using the AskUserQuestion tool
3. **Document assumptions** if proceeding without full clarity
4. **Update this file** when conventions are established

---

## Maintenance

### Updating This Document

This CLAUDE.md file should be updated when:

- Project structure changes significantly
- New conventions are established
- New tools or frameworks are added
- Deployment process is defined
- Testing strategy is implemented

**Responsibility:** Any AI assistant or developer making structural changes should update this file accordingly.

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-18 | 1.0.0 | Initial CLAUDE.md creation |

---

## Additional Resources

*To be added as project develops:*

- Project documentation links
- External API documentation
- Related projects
- Research papers (if applicable)
- Community resources

---

**End of CLAUDE.md**
