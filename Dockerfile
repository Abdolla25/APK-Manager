FROM python:3.9

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apk_manager /code/

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "apk_manager.wsgi:application", "--reload"]
