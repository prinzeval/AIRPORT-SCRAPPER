FROM python:3.9

# Copy the entire project directory to /app
COPY . /app

# Set /app as the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    wget \
    unzip \
    curl \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3-dev \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libgbm1 \
    xdg-utils

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app runs on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
