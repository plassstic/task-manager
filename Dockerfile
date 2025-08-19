FROM python:slim AS allreps
LABEL authors="plassstic"

ARG YOUR_ENV

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV YOUR_ENV=${YOUR_ENV} \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    DOCKER_MODE=true
RUN apt-get -y update; apt-get -y install build-essential curl cmake;
WORKDIR /deploy
COPY . ./
RUN --mount=type=cache,target=/root/.cache/uv \
  uv lock \
  && uv sync --frozen