# Use an official base image for Raspberry Pi with Python
FROM balenalib/raspberrypi4-64-debian-python:3.9.14

# Install system dependencies
RUN apt-get update && apt-get install -y libpcap-dev python3-libcamera python3-picamera2

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
# RUN python3 -m venv --system-site-packages venv
# RUN . venv/bin/activate && 
RUN pip install --upgrade pip && pip install -r requirements.txt

# Clone the project from GitHub
RUN apt-get install -y git
RUN mkdir /app/Documents
RUN cd /app/Documents && git clone https://github.com/FabianBraun121/HouseKeeper.git

# Set the working directory
WORKDIR /app/Documents/HouseKeeper

