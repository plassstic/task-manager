# taskmgr

## Запуск

1. Создайте `.env` файл и добавьте в него несколько необходимых переменных: **REDIS\_PASSWORD** и **POSTGRES\_PASSWORD**. Остальные переменные изменяются по желанию, см. [config.py](src/utility/config.py)

2. `make docker-up`

3. При изменении незамаунченых файлов: `make docker-rebuild`

## Тестирования

### deps: gauge, uv

**Важно**: для тестирования необходимо заранее запустить сам менеджер через `docker-compose` (см. выше)

1. `uv lock && uv sync`

2. `gauge run tests/specs`
