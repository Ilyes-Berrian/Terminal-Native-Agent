FROM ghcr.io/astral-sh/uv:python3.14-trixie

WORKDIR /Terminal-Native-Agent

COPY pyproject.toml README.md uv.lock ./
COPY src/ ./src/

RUN groupadd -r developers && \
    useradd -r -m -g developers dev1 && \
    uv sync --frozen && \
    chown -R dev1:developers ./

USER dev1

CMD [ "uv", "run", "./src/main.py" ]