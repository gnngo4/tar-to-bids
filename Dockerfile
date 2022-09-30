FROM nipy/heudiconv:v0.11.3


# Install tar-to-bids
RUN mkdir -p /opt/tar-to-bids
COPY . /opt/tar-to-bids 

ENTRYPOINT ["python","/opt/tar-to-bids/main.py"]