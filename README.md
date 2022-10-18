# tar-to-bids
A tar2bids fork

Build container
```bash
docker build -t tar-to-bids .
```

## Example usage

Check subject and session information for a tar file <tar-file> (requires a directory <mapping-directory> containing a manually generated tar_mappings.csv)
```bash
docker run -it -v <mapping-directory>:/mappings tar-to-bids --check_tar_mappings <tar-file>
```

Check available heuristics (heuristics are manually generated)
```bash
docker run -it tar-to-bids --check_available_heuristics
```

Run tar-to-bids:
 - `mapping-directory`: directory with the tar_mappings.csv file (manually generated)
 - `tar-directory`: directory with the tar files (generated using cfmm2tar)
 - `bids-directory`: output directory for outputted bids-ified data
 - `--tar`: input tar file
 - `--subject`: input subject id (cross-reference with --check-tar-mappings flag)
 - `--session`: input session id (cross-reference with --check-tar-mappings flag)
 - `--heuristic`: heuristic used to bids-ify the tar files (manually generated and stored in /src/heuristics)
```
docker run --rm -it -v <mapping-directory>:/mappings -v <tar-directory>:/tar -v <bids-directory>:/bids tar-to-bids --tar /tar/<tar-file> --subject <subject-id> --session <session-id> --heuristic <heuristic> --output_dir /bids
```

Optionally perform additional bids post-processing:
 - `--task-mappings`: input csv file with task mapping information 
   - Manually generate (1) csv file (2) an additional heuristic file stored in /src/heuristics_post with a function named heudiconv_post_process())
```
docker run --rm -it -v <mapping-directory>:/mappings -v <tar-directory>:/tar -v <bids-directory>:/bids tar-to-bids --tar /tar/<tar-file> --subject <subject-id> --session <session-id> --heuristic <heuristic> --output_dir /bids --task-mappings <task-mapping>
```
 - an additional `--post-process` flag can be used if the additional post-processing scripts does not require a task-mapping csv file.

## Building a singularity image from a local docker image
https://github.com/apptainer/singularity/issues/1537

```bash
# Start a docker registry
docker run -d -p 5000:5000 --restart=always --name registry registry:2
# Build docker image
docker build -t tar-to-bids .
# Push local docker container to the registry
docker tag tar-to-bids localhost:5000/tar-to-bids
docker push localhost:5000/tar-to-bids
# Create a singularity image
SINGULARITY_NOHTTPS=1 singularity build tar-to-bids.simg docker://localhost:5000/tar-to-bids:latest
```


