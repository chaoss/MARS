# Official Dockerfile for CHAOSS M.A.R.S.
# The mars-image is hosted here: https://hub.docker.com/r/ritikmalik/mars-image
#
# pull size = 842.35 MB (compressed)
# size after uncompression = 2.2 GB (actual image size)

# pull the latest image
FROM ritikmalik/mars-image:latest

# add new non-root user with UID and GID same as system
ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user

# switch to non-root user
USER user

# set working directory
WORKDIR /MARS

# copy M.A.R.S. scripts
COPY . .

# main command to be run
CMD ["/bin/bash", "-c", "python3 -u main.py | tee logs.txt"]

