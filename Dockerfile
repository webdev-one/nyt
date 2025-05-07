FROM python:slim AS build
WORKDIR /nyt

# Install the application dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src/ src/

# Setup an app user so the container doesn't run as the root user
RUN useradd dockeruser
USER dockeruser

VOLUME /nyt

CMD ["python3", "/nyt/src/main.py"]