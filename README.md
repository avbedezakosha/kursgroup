# CS:GO Match Tracker

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt-5.15.9-green.svg)](https://pypi.org/project/PyQt5/)

## Приложение для анализа и управления статистикой матчей CS:GO с графическим интерфейсом.

---

## 🛠 Установка

### 1. Создание виртуального окружения

#### Windows
```cmd
python -m venv .venv
.venv\Scripts\activate
```
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Установка зависимостей

```cmd
pip install -r requirements.txt
```
---
## Конвертирование *.ui в *.py
#### Windows
```cmd
python scripts/converter_ui.py
```
#### Linux/macOS
```bash
python3 scripts/converter_ui.py
```
---
## Запуск приложения
#### Windows
```cmd
python main.py
```
#### Linux/macOS
```bash
python3 main.py
```