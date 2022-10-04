# tar-to-bids
A tar2bids Fork

Build container
```bash
docker build -t tar-to-bids .
```

Sample run
```bash
docker run -it -v <output-directory>:/bids -v <tar-directory>:/tar tar-to-bids --tar /tar/<tar-file> --subject <subject-id> --session <session-id> --heuristic <heuristic> --output_dir /bids
```
