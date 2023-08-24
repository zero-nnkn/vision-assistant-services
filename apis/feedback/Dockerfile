FROM public.ecr.aws/lambda/python:3.8

ARG AWS_REGION
ARG TABLE_NAME

ENV AWS_REGION=${AWS_REGION} \
    TABLE_NAME=${TABLE_NAME}

COPY requirements.txt  .
RUN  python3.8 -m pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" --no-cache-dir

COPY main.py ${LAMBDA_TASK_ROOT}

CMD ["main.lambda_handler"]