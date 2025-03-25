FROM bringauto/python-environment:latest

WORKDIR /home/bringauto

COPY ./requirements.txt /home/bringauto
RUN "$PYTHON_ENVIRONMENT_PYTHON3" -m pip install --no-cache-dir -r requirements.txt

# Install Playwright
RUN "$PYTHON_ENVIRONMENT_PYTHON3" -m playwright install
RUN "$PYTHON_ENVIRONMENT_PYTHON3" -m playwright install-deps

# Copy the Python script into the container
COPY config /home/bringauto/config
COPY test_login.py /home/bringauto/test_login.py

ENTRYPOINT ["bash", "-c", "$PYTHON_ENVIRONMENT_PYTHON3 test_login.py $0 $@"]