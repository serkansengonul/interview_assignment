# Use the official Python 3.9 image as the base image.
FROM python:3.9

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy the current directory content into the container at /app.
COPY . /app

# Copy the requirements file into the container at /app.
COPY requirements.txt requirements.txt

# Install the Python dependencies from requirements.txt.
RUN pip install -r requirements.txt

# Command to run when the container starts.
# 1. Sleep for 10 seconds to ensure the database is ready.
# 2. Initialize the database.
# 3. Run the ETL process.
# 4. Start the Flask application.
CMD sleep 10 && python /app/src/init_db.py && python /app/src/etl.py && python /app/src/app.py
