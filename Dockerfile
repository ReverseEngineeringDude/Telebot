# Use a base Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY r.txt .
RUN pip install -r r.txt

# Install the python-dotenv package
RUN pip install python-dotenv

# Copy your Python code into the container
COPY main.py .

# Set any necessary environment variables (if required)
# ENV VARIABLE_NAME=VALUE

# Define the command to run your Python script
CMD ["python", "main.py"]
