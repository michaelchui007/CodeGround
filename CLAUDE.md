# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CodeGround is a PySide6 (Qt for Python) playground project containing various UI demos, templates, and utilities. It is NOT a single application — each subdirectory is an independent demo or module.

## Tech Stack

- Python 3.11+, PySide6 (Qt6 bindings)
- Virtual environment: `.venv311/`
- Dependencies: `requirements.txt` (PySide6, protobuf, python-dotenv, clipboard)
- Environment variables loaded via `python-dotenv` from `debug.env` (gitignored)

## Project Structure

- **`templetes/`** — Collection of standalone PySide6 demo applications (each has its own `main.py` or entry point). Includes: BOM manager, checkable combo box, loading dialogs, drill manager, HTML-to-PDF export, table view demos, icon menu buttons, etc.
- **`r_model_view_delegate/`** — A complete Model-View-Delegate (MVD) implementation for a book library management system. Demonstrates custom `QAbstractTableModel`, `QAbstractItemModel` (tree), custom delegates (combo, checkbox, date, color), and lazy-loading with scroll-based pagination. Entry: `r_mainwindow.py`
- **`QTableViewMoveAction/`** — Table view with row move/reorder functionality using `QStandardItemModel` and custom `QAbstractTableModel`
- **`AI_Ground/`** — Google Gemini API integration demo
- **`utils/`** — Utility scripts (list comparison, UUID clipboard generator)
- **`ui/`** — Qt Designer `.ui` files
- **Top-level `.py` files** — Standalone study/experiment scripts

## Running Demos

Each demo is self-contained. Run directly:
```bash
python templetes/bom_manager_demo/main.py
python r_model_view_delegate/r_mainwindow.py
```

## Architecture Patterns

- **Model-View-Delegate (MVD)**: Core pattern used throughout. Models (`*_model.py`) hold data, Views (`*_view.py`) display it, Delegates (`*_delegate.py`) control editing widgets.
- **DelegateFactory**: In `r_model_view_delegate/`, a factory class with `DelegateType` enum creates delegates declaratively for batch column assignment.
- **Lazy loading**: Large datasets use scroll-position-triggered batch loading (scroll past 80% → load next batch) rather than loading all rows upfront.
- **Service layer**: Some demos (e.g., `bom_manager_demo/bom_service.py`) separate data transformation logic from the model.

## Conventions

- Language: Python, UI strings in Chinese
- IDE: PyCharm (`.idea/` committed)
- Git branch naming: `feat-<feature-name>`
- The `templetes/` directory name is intentionally misspelled (historical)