#!/bin/bash
# This script is to automate the Docker instance for M.A.R.S. on Linux(debian-based) & Max OS/X

# GLOBAL VARS
MARS_LINK='https://github.com/chaoss/MARS'
CUR_DIR='automation'
DOCKERHUB_IMG_NAME='ritikmalik/mars-image:latest'
DOCKER_IMG_NAME='chaoss-mars'
DOCKER_CONTAINER_NAME='mars-container'
OS_type=''

# Define colors
RED='\033[0;91m'
GREEN='\033[0;92m'
BLUE='\033[0;94m'
CYAN='\033[0;96m'
YELLOW='\033[0;93m'
NC='\033[0m' # No Color

### function definations begins

greetings(){

  echo -e "${RED}"
  echo -e '              ___---___          '
  echo -e '           .--         --.       '
  echo -e '         ./   ()   *  .-. \.     '
  echo -e '        /   o    .   (   )  \    '
  echo -e '       / .            "-"    \   '
  echo -e '      | () .    °   o   .   * |  '
  echo -e '     |    ╔╦╗  ╔═╗  ╦═╗  ╔═╗   | '
  echo -e '     |  o ║║║  ╠═╣  ╠╦╝  ╚═╗  .| '
  echo -e '     |    ╩ ╩  ╩ ╩  ╩╚═  ╚═╝   | '
  echo -e '      | .    .--.   O      °  |  '
  echo -e '       \  ° |    |    o   .  /   '
  echo -e '        \   `.__.`     .    /    '
  echo -e '         `\  o    ()      /`     '
  echo -e '           `--___   ___--`       '
  echo -e '                 ---             '
  echo -e '   Metrics Automated Release System'
  echo -e "${YELLOW}======================================"
  echo -e "${CYAN}"
  echo -e "Latest Release: <DATE>"
  echo -e "Current Version: v1.0"
  echo -e "GitHub: https://github.com/chaoss/MARS\n"
  echo -e "${YELLOW}======================================"
  echo -e
}

# set -x
check_platform(){

  # OS detections step
  platform="$(uname -s)"

  case "${platform}" in
    Linux*)     machine='Linux';;
    Darwin*)    machine='Mac OS/X';;
    CYGWIN*)    machine='Cygwin';;
    MINGW*)     machine='MinGw';;
    *)          machine="UNKNOWN:${platform}"
  esac

  if [ "${machine}" = "Linux" ]; then
    echo -e "${CYAN}[Check 0/5]: Checking user platform...${GREEN}${machine}"
  elif [ "${machine}" = "Mac OS/X" ]; then
    echo -e "${CYAN}[Check 0/4]: Checking user platform...${GREEN}${machine}"
  else
    echo -e "${RED}[Error]: ${machine} is not yet supported on M.A.R.S."
    exit 1
  fi

  # return the machine type as param - OS_type
  eval $1=${machine}
}

check_docker_installed(){
  # check if Docker is installed
  if [[ $(which docker) && $(docker --version) ]]; then
    echo -e "${CYAN}[Check ${1}/${2}]: Checking if Docker is installed...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Docker not found, please install Docker."
    echo
    echo -e "${CYAN}Refer to official doc: https://docs.docker.com/engine/install/${NC}"
    echo
    exit 1
  fi
}

check_user_docker_grp(){
  # check if user is in Docker group
  if [ $(grep /etc/group -e "docker" | awk -F ':' '{ print $4 }') = $USER ]; then
    echo -e "${CYAN}[Check ${1}/${2}]: Checking if ${USER} is in Docker group...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Please add your user to Docker group${NC}"
    echo
    echo -e "Run the following commands:\n"
    echo -e "$ sudo usermod -a -G docker $USER"
    echo -e "$ reboot"
    echo
    exit 1
  fi
}

check_docker_running(){
  # check if docker is running
if docker info >/dev/null 2>&1; then
    echo -e "${CYAN}[Check ${1}/${2}]: Checking if Docker is running...${GREEN}Yes"
else
    echo -e "${RED}[Error]: Docker does not seem to be running, run it first and retry${NC}"
    echo
    exit 1
fi
}

check_cur_dir(){
  # check if current directory == ${CUR_DIR}
  if [ "$(pwd | awk -F '/' '{ print $NF }')" = "${CUR_DIR}" ]; then
    echo -e "${CYAN}[Check ${1}/${2}]: Checking for correct directory...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Please run this script in '${CUR_DIR}' directory${NC}"
    echo
    exit 1
  fi
}

check_dockerfile(){
  # check if Dockerfile exist
  FILE=Dockerfile
  if [[ -f "$FILE" ]]; then
    echo -e "${CYAN}[Check ${1}/${2}]: Checking for Dockerfile...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: $FILE not found in $(pwd)${NC}"
    echo
    exit 1
  fi
}

check_exit(){
  # check exit code of command, exit if non 0
  echo
  if [ $1 -eq 0 ]; then
    echo -e "${GREEN}[+] Command executed with exit code $1"
  else
    echo -e "${RED}[Error]: Process stopped with exit code $1${NC}"
    echo
    exit 1
  fi
}

### function definations ends

# main()
greetings
check_platform "OS_type"

# The number of checks are dynamic to OS type,
# 1 extra check for linux - "user should be in Docker grp"
# Pass the current check number and total checks as params
if [ "${OS_type}" = "Linux" ]; then
  check_docker_installed "1" "5"
  check_user_docker_grp "2" "5"
  check_docker_running "3" "5"
  check_cur_dir "4" "5"
  check_dockerfile "5" "5"
else
  check_docker_installed "1" "4"
  check_docker_running "2" "4"
  check_cur_dir "3" "4"
  check_dockerfile "4" "4"
fi

echo
echo -e "${GREEN}Passed all checks successfully..."
echo

# Checks over, start main stuff

# build the docker image -> ${DOCKER_IMG_NAME}
echo -e "${CYAN}Building the '${DOCKER_IMG_NAME}' image"
echo -e "--------------------------------${NC}"
echo

docker build -t ${DOCKER_IMG_NAME} .

check_exit $?

# remove dangling images (if any)
echo
echo -e "${CYAN}Removing dangling images (if any)"
echo -e "---------------------------------${NC}"
echo
docker rmi $(docker images | grep none | awk '{  print $3 }') 2> /dev/null

echo
echo -e "${GREEN}Done"
echo

# remove mars-container if already exist
echo -e "${CYAN}Removing ${DOCKER_CONTAINER_NAME} (if already exist)...${NC}"
docker rm -f ${DOCKER_CONTAINER_NAME} &>/dev/null && echo 'Removed old container'

echo
echo -e "${GREEN}Done"
echo

# run docker image with bind mount
echo
echo -e "${CYAN}Running the ${DOCKER_CONTAINER_NAME}"
echo -e "--------------------------${NC}"
echo

docker run --name ${DOCKER_CONTAINER_NAME} -it \
--mount type=bind,source=`pwd`,target=/MARS ${DOCKER_IMG_NAME}

# remove container
echo
echo -e "${CYAN}Removing the ${DOCKER_CONTAINER_NAME}"
echo -e "---------------------------${NC}"
echo

docker rm ${DOCKER_CONTAINER_NAME}

check_exit $?

# echo -e "\n${CYAN}Changing permissions from root user to ${YELLOW}${SUDO_USER}"
# chown -R ${SUDO_USER}:${SUDO_USER} .

# Display output
echo
echo -e "${NC}Unless you plan to rerun the script in future, you can safetly delete the images by using the commands:${CYAN}"
echo
echo -e "$ docker rmi ${DOCKER_IMG_NAME}"
echo -e "$ docker rmi ${DOCKERHUB_IMG_NAME}"
echo

# echo -e "${GREEN}Logs are saved in ${YELLOW}logs.txt"
# echo -e "${GREEN}Ouput PDF is saved in ${YELLOW}output/${GREEN} directory with format: ${YELLOW}'Output-YYYY-MM-DD.pdf'\n"
