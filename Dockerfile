FROM public.ecr.aws/lambda/python:3.8
RUN pip install -U --no-cache-dir pip wheel setuptools
COPY KleeOne-Regular.ttf ./KleeOne-Regular.ttf
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
CMD ["app.handler"]