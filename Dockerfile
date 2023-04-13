FROM python:3

WORKDIR /app

COPY tcptee.py ./

CMD ["sh", "-c", "python tcptee.py $PORT $DEST1 $DEST2"]