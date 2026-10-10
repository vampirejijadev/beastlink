# Contributing to Beastlink

Thanks for your interest in improving Beastlink! This guide will help you get started.

## Reporting Bugs

Before opening an issue:

1. Check the [existing issues](https://github.com/vampirejjjadev/beastlink/issues) to avoid duplicates.
2. Update to the latest version: `pip install --upgrade beastlink`
3. Confirm the bug still exists.

When you open an issue, include:

- Beastlink version (`pip show beastlink`)
- Python version (`python --version`)
- Operating system
- Full traceback
- Minimal reproduction steps
- Expected vs actual behavior

## Suggesting Features

Open an issue with the `enhancement` label. Describe:

- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

## Development Setup

```bash
git clone https://github.com/vampirejjjadev/beastlink.git
cd beastlink
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -e ".[dev]"