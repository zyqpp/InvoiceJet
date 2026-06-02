FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml README.md requirements.txt ./
COPY oracle_invoicejet ./oracle_invoicejet

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -e .

EXPOSE 8502

CMD ["python", "-m", "oracle_invoicejet.cli_serve", "--port", "8502"]
