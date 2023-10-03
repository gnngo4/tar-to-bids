rm tar-to-bids.simg
docker build -t tar-to-bids .
docker tag tar-to-bids localhost:5000/tar-to-bids
docker push localhost:5000/tar-to-bids
SINGULARITY_NOHTTPS=1 singularity build tar-to-bids.simg docker://localhost:5000/tar-to-bids
