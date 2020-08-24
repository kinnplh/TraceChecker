FROM python:3
WORKDIR /home/app
COPY ./requirements.txt /home/app
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5000
CMD ["python", "dev.py"]