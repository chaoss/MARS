# Official Dockerfile for CHAOSS M.A.R.S.
# The mars-image is hosted here: https://hub.docker.com/repository/docker/ritikmalik/mars-image
# pull size = 437 MB
# size after uncompression = 1.32 GB
#
# This Dockerfile file pulls the mars-image from above url,
# set a non-root user, set Working Dir, copy scripts and command

# pull the beta image
FROM ritikmalik/mars-image:beta

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
