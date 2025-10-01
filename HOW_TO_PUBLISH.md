# Publishing to PyPI

This guide explains how to publish the `camels-attrs` package to PyPI.

## Prerequisites

1. Create accounts on:
   - PyPI: https://pypi.org/account/register/
   - TestPyPI: https://test.pypi.org/account/register/

2. Install build tools:
   ```bash
   pip install build twine
   ```

## Step 1: Update Version

Edit `pyproject.toml` and update the version number:
```toml
version = "0.1.1"  # Increment as needed
```

Also update in `camels_attributes/__init__.py`:
```python
__version__ = "0.1.1"
```

## Step 2: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel and source distribution
python -m build
```

This creates:
- `dist/camels_attributes-0.1.0.tar.gz` (source distribution)
- `dist/camels_attributes-0.1.0-py3-none-any.whl` (wheel)

## Step 3: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple camels-attributes
```

## Step 4: Publish to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Enter your PyPI credentials when prompted
```

## Step 5: Verify Installation

```bash
# Install from PyPI
pip install camels-attrs

# Test
python -c "from camels_attributes import CamelsExtractor; print('Success!')"
```

## Automation with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Version Numbering

Follow semantic versioning (semver):
- **0.1.0**: Initial release
- **0.1.1**: Bug fixes
- **0.2.0**: New features (backward compatible)
- **1.0.0**: Stable API, production ready

## Checklist Before Publishing

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated
- [ ] Version numbers are incremented
- [ ] README.md is clear and complete
- [ ] LICENSE file is included
- [ ] Example usage works correctly
- [ ] Dependencies are correctly specified
- [ ] Build succeeds without errors
- [ ] Test installation works on clean environment
