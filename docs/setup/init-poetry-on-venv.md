# Init Poetry on Venv

- venv가 활성화된 상태에서 peotry download & install

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

- Poetry가 venv를 사용하도록 설정

```bash
poetry config virtualenvs.prefer-active-python true
```

- 현재 프로젝트에서 Poetry 초기화(pyproject.toml 생성)

```bash
poetry init
```

- install package

```bash
poetry install
```

- update package

```bash
poetry update
```

## check project setting

```bash
# 현재 환경 정보 확인
poetry env info

# 설치된 패키지 확인
poetry show
```
