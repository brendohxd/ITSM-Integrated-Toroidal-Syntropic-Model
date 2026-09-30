FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Native toolchain for the modified CAMB solver plus manuscript compilation.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        git-lfs \
        pkg-config \
        latexmk \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-publishers \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install --system

ENV MPLBACKEND=Agg \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
