FROM python:3.9

# set working directory
WORKDIR /app

# copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the app code to the container
COPY . .

# expose the port that the Flask app runs on
EXPOSE 5000

# start the Flask app
CMD ["python3", "app.py"]

