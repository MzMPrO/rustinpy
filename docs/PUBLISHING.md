# Публикация rustinpy: чек-лист

Публикует только мейнтейнер, вручную, по шагам ниже. Claude Code ничего не загружает на
PyPI / TestPyPI сам (AC-20). Токены не пишутся ни в файлы, ни в коммиты, ни в логи.

Схема: GitHub Actions + **Trusted Publishing** (OIDC). `.github/workflows/publish.yml`:
- ручной запуск (Actions → Publish → Run workflow) → сборка, тесты → **TestPyPI**, environment `testpypi`;
- push тега `v*` (например `v0.1.0`) → сборка, тесты, проверка «тег = `__version__`» → **PyPI**, environment `pypi`.

Ниже `<nick>` — ваш логин на GitHub.

## 0. Перед началом (локально)

```bash
.venv/Scripts/python.exe -m pytest                     # все тесты зелёные
.venv/Scripts/ruff.exe check . && .venv/Scripts/ruff.exe format --check .
.venv/Scripts/mypy.exe
.venv/Scripts/python.exe scripts/gen_catalog.py --check
.venv/Scripts/python.exe -m build && .venv/Scripts/python.exe -m twine check --strict dist/*
```

`dist/` в git не попадает (`.gitignore`), после проверки его можно удалить.

## 1. Репозиторий на GitHub

1. github.com → New repository → имя `rustinpy`, **Public**, без README / .gitignore / лицензии
   (они уже есть).
2. Сообщите `<nick>` Claude Code: он добавит в `pyproject.toml` блок `[project.urls]`
   (Homepage, Source, Issues, Changelog) и сделает ссылки README абсолютными: на странице PyPI
   относительные ссылки (`docs/CATALOG.md`) не открываются. Это отдельный коммит.
3. Отправка кода:
   ```bash
   git remote add origin https://github.com/<nick>/rustinpy.git
   git push -u origin main
   ```
4. Actions → CI: дождаться зелёного прогона на 3.9–3.13 и Windows (**AC-18**).

## 2. Окружения GitHub

Settings → Environments → New environment:
- `testpypi`: без ограничений;
- `pypi`: включите **Required reviewers** (вы сами) и в «Deployment branches and tags» разрешите
  только теги `v*`. Тогда публикация на PyPI ждёт вашего подтверждения.

## 3. TestPyPI

1. Аккаунт на https://test.pypi.org (отдельный от PyPI), подтвердите email, включите 2FA.
2. Your account → Publishing → **Add a new pending publisher** → GitHub:
   - PyPI Project Name: `rustinpy`
   - Owner: `<nick>`
   - Repository name: `rustinpy`
   - Workflow name: `publish.yml`
   - Environment name: `testpypi`
3. GitHub → Actions → **Publish** → Run workflow (ветка `main`). Задание `testpypi` должно
   завершиться зелёным; проект появится на https://test.pypi.org/project/rustinpy/.
4. Проверка в чистом окружении (**AC-19**). У пакета нет зависимостей, поэтому хватает одного
   индекса:
   ```bash
   python -m venv testenv
   testenv/Scripts/python.exe -m pip install -i https://test.pypi.org/simple/ rustinpy
   testenv/Scripts/rustinpy.exe --version
   testenv/Scripts/rustinpy.exe show dijkstra
   ```
   Тесты из sdist: скачать `rustinpy-0.1.0.tar.gz` со страницы TestPyPI, распаковать, внутри
   `pip install pytest` и `python -m pytest` (сам пакет уже установлен из TestPyPI).
   Этот шаг можно поручить Claude Code (этап 6): он только скачивает и запускает тесты.

Повторно загрузить ту же версию на TestPyPI нельзя. Если нужна вторая попытка, поднимите версию
(например `0.1.0.post1` только для TestPyPI) или удалите релиз на test.pypi.org вручную.

## 4. PyPI

1. Аккаунт на https://pypi.org, email, 2FA.
2. Your account → Publishing → **Add a new pending publisher** → GitHub: те же поля, что в 3.2,
   но Environment name: `pypi`.
3. Перед тегом:
   - в `CHANGELOG.md` раздел `[Unreleased]` переименовать в `[0.1.0] - ГГГГ-ММ-ДД`;
   - `__version__` в `src/rustinpy/__init__.py` = `0.1.0`;
   - закоммитить и запушить `main`, CI зелёный.
4. Тег:
   ```bash
   git tag -a v0.1.0 -m "rustinpy 0.1.0"
   git push origin v0.1.0
   ```
5. Actions → Publish: задание `pypi` ждёт подтверждения (Review deployments → Approve).
6. Проверка: https://pypi.org/project/rustinpy/ и `pip install rustinpy` в чистом venv.

Pending publisher не резервирует имя: пока первой загрузки нет, имя `rustinpy` может занять
кто-то другой. Если шаг 4 откладывается, перед тегом проверьте, что https://pypi.org/project/rustinpy/
всё ещё 404.

## 5. Запасной вариант: API-токен (только если Trusted Publishing недоступен)

1. pypi.org → Account settings → API tokens → Add API token. Для первой загрузки область
   «Entire account», после неё создайте токен с областью только `rustinpy`, а первый удалите.
2. Токен кладётся **только в переменную окружения** текущей сессии, не в файлы и не в историю
   команд. PowerShell:
   ```powershell
   $env:PYPI_API_TOKEN = Read-Host "PyPI token"     # вставить токен, он не попадёт в файлы
   $env:TWINE_USERNAME = "__token__"
   $env:TWINE_PASSWORD = $env:PYPI_API_TOKEN
   python -m build
   python -m twine upload dist/*                      # для TestPyPI: --repository testpypi
   Remove-Item Env:PYPI_API_TOKEN, Env:TWINE_PASSWORD, Env:TWINE_USERNAME
   ```
3. Для GitHub Actions токен хранится только как секрет репозитория (Settings → Secrets and
   variables → Actions → `PYPI_API_TOKEN`). Тогда в `publish.yml` шагу
   `pypa/gh-action-pypi-publish` добавляется `with: password: ${{ secrets.PYPI_API_TOKEN }}`.
   Это изменение workflow делается отдельным коммитом только по вашей команде.

## Что уже сделано

- `pyproject.toml`: hatchling, версия из `__init__.py`, MIT, `requires-python >= 3.9`, без
  зависимостей, `[project.scripts] rustinpy`, `py.typed`.
- `python -m build` и `twine check --strict` проходят (тест `test_ac_17`, маркер `slow`).
- CI (`ci.yml`): ruff, mypy, pytest на 3.9–3.13 + Windows, сборка и установка wheel в чистый venv.
- `publish.yml`: Trusted Publishing, `id-token: write` только в заданиях публикации.
