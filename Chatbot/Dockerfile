FROM python:3.9-slim

# 2.The WORKDIR instruction sets the working directory 
WORKDIR /app

COPY . .

# 5.Install your app’s Python dependencies
RUN pip3 install -r requirements.txt

# 6.Export Port
EXPOSE 8501

# 7.
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

#8.
ENTRYPOINT ["streamlit", "run", "scratch_app.py", "--server.port=8501", "--server.address=0.0.0.0"]