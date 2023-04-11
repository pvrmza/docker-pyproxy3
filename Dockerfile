FROM python:3

WORKDIR /app

COPY pyproxy3.py ./

CMD ["sh", "-c", "python pyproxy3.py $PORT $DEST1 $DEST2"]