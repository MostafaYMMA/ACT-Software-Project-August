# 1. Base image — slim Python, enough for FastAPI/uvicorn, small image size
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy only requirements first — this layer gets cached by Docker,
#    so re-builds after code changes (not dependency changes) are fast
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now copy the rest of the backend source
COPY . .

# 6. Document the port the app listens on (informational — doesn't publish it)
EXPOSE 8000

# 7. Start the server, bound to 0.0.0.0 so it's reachable from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]