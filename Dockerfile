FROM ghcr.io/astral-sh/uv:python3.14-alpine

WORKDIR /Terminal-Native-Agent/

COPY pyproject.toml README.md uv.lock ./
COPY src/ ./src/

RUN uv sync --frozen

CMD [ "uv", "run", "./src/main.py" ]