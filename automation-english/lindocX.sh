#!/bin/bash
# This script is to automate the Docker instance for M.A.R.S. on Linux(debian-based) & Max OS/X

# GLOBAL VARS
MARS_LINK='https://github.com/chaoss/MARS'
CUR_DIR='automation-english'
DOCKERHUB_IMG_NAME='ritikmalik/mars-image:latest'
DOCKER_IMG_NAME='chaoss-mars'
DOCKER_CONTAINER_NAME='mars-container'

# Define colors
RED='\033[0;91m'
GREEN='\033[0;92m'
BLUE='\033[0;94m'
CYAN='\033[0;96m'
YELLOW='\033[1;93m'
NC='\033[0m' # No Color

greetings(){
  echo -e "${YELLOW}"
  echo -e "------------------------------"
  echo -e "CHAOSS M.A.R.S. on Linux/Mac"
  echo -e "${MARS_LINK}" 
  echo -e "------------------------------"
  echo
}

check_1(){
  # check if Docker is installed
  if [[ $(which docker) && $(docker --version) ]]; then
    echo -e "${CYAN}[Check 1/5]: Checking if Docker is installed...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Docker not found, please install Docker."
    echo
    echo -e "${CYAN}Refer to official doc: https://docs.docker.com/engine/install/${NC}"
    echo
    exit 1
  fi
}

check_2(){
  # check if user is in Docker group
  if [ $(grep /etc/group -e "docker" | awk -F ':' '{ print $4 }') = $USER ]; then
    echo -e "${CYAN}[Check 2/5]: Checking if ${USER} is in Docker group...${GREEN}Yes"
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

check_3(){
  # check if docker is running
if docker info >/dev/null 2>&1; then
    echo -e "${CYAN}[Check 3/5]: Checking if Docker is running...${GREEN}Yes"
else
    echo -e "${RED}[Error]: Docker does not seem to be running, run it first and retry${NC}"
    echo
    exit 1
fi
}

check_4(){
  # check if current directory == ${CUR_DIR}
  if [ "$(pwd | awk -F '/' '{ print $NF }')" = "${CUR_DIR}" ]; then
    echo -e "${CYAN}[Check 4/5]: Checking for correct directory...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Please run this script in '${CUR_DIR}' directory${NC}"
    echo
    exit 1
  fi
}

check_5(){
  # check if Dockerfile exist
  FILE=Dockerfile
  if [[ -f "$FILE" ]]; then
    echo -e "${CYAN}[Check 5/5]: Checking for Dockerfile...${GREEN}Yes"
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

### function definations over

# main()
greetings
check_1
check_2
check_3
check_4
check_5

echo
echo -e "${GREEN}Passed all checks successfully..."
echo

# Checks over, start main stuff

# build the docker image -> ${DOCKER_IMG_NAME}, pass the UID and GID of system
echo -e "${CYAN}Building the '${DOCKER_IMG_NAME}' image"
echo -e "--------------------------------${NC}"
echo

docker build -t ${DOCKER_IMG_NAME} \
--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .

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
