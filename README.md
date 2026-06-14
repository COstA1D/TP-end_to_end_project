# TP-End_To_End_Project

Учебный сквозной data-проект с поэтапной разработкой по неделям.

## Project structure

- `src/` — исходный код проекта
- `data/` — данные проекта
- `notebooks/` — исследовательские ноутбуки
- `docs/` — документация
- `configs/` — конфигурационные файлы
- `tests/` — тесты
- `scripts/` — служебные скрипты

## Windows setup
1. Install Anaconda or Miniconda.
2. Open **Anaconda Prompt**.
3. Go to the project folder:
   ```bat
   cd C:\Users\***\OneDrive\Desktop\е\end-to-end-project
   ```
4. Run:
   ```bat
   scripts\setup_env.bat
   ```

## Smoke test
The script `scripts\setup_env.bat` automatically:
- finds `conda`;
- creates the `tp_project_env` environment if it does not exist;
- installs dependencies from `requirements.txt`;
- runs `broken_env.py`.

Successful result:
- the path to the active Python interpreter is printed;
- the installed `pandas` version is printed;
- the final line is:
  ```text
  [OK] Environment is ready
  ```

## Progress by weeks 
- [x] Week 1 - Conda setup, repository structure, smoke test
- [ ] Week 2
- [ ] Week 3
- [ ] Week 4
- [ ] Week 5
- [ ] Week 6
- [ ] Week 7
- [ ] Week 8
- [ ] Week 9
- [ ] Week 10
- [ ] Week 11
- [ ] Week 12
- [ ] Week 13
- [ ] Week 14 
