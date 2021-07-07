# Official Dockerfile for CHAOSS M.A.R.S.
# The mars-image is hosted here: https://hub.docker.com/repository/docker/ritikmalik/mars-image
#
# This file pulls the mars-image from above url, set Working Dir, copy scripts and command

FROM ritikmalik/mars-image:beta
# pull size = 437 MB
# size after uncompression = 1.32 GB

# set working directory
WORKDIR /MARS

# copy M.A.R.S. scripts
COPY . .

CMD ["/bin/bash", "-c", "python3 -u main.py | tee logs.txt"]

