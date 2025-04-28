# python
FROM python:3.13-slim
# install dependencies
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# copy source code
COPY . .
# run the app
CMD ["python", "-m", "DevilCV.main"]
