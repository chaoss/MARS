#!/bin/bash
# This script is to automate the Docker instance for M.A.R.S. on Linux
# Run it as ROOT

### Global Vars ###
MARS_link='https://github.com/chaoss/MARS'
cur_dir='automation-english'
docker_image_name='chaoss-mars'
docker_container_name='mars-container'

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

greetings(){
  echo -e "${YELLOW}"
  echo -e "------------------------------"
  echo -e "CHAOSS M.A.R.S. on Linux"
  echo -e "${MARS_link}" 
  echo -e "------------------------------\n"
}

check_1(){
  # check if root
  if [ "$EUID" = 0 ]; then
    echo -e "${CYAN}[Check 1/4]: Checking for root permission...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Please run as root\n"
    exit
  fi
}

check_2(){
  # Check if Docker is installed
  if [[ $(which docker) && $(docker --version) ]]; then
    echo -e "${CYAN}[Check 2/4]: Checking for Docker...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Docker not found, please install Docker.\n"
    echo -e "${CYAN}Run the following 3 commands to install Docker on Linux:\n"
    echo -e '1. curl -fsSL https://get.docker.com -o get-docker.sh'
    echo -e '2. chmod +x get-docker.sh'
    echo -e '3. sudo sh get-docker.sh'
    echo -e
    echo -e 'Or refer to official doc: https://docs.docker.com/engine/install/ \n'
    exit
  fi
}

check_3(){
  # check if current directory == ${cur_dir}
  if [ "$(pwd | awk -F '/' '{ print $NF }')" = "${cur_dir}" ]; then
    echo -e "${CYAN}[Check 3/4]: Checking for correct directory...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Please run this script in '${cur_dir}' directory\n"
    exit
  fi
}

check_4(){
  # check if Dockerfile exist
  FILE=Dockerfile
  if [[ -f "$FILE" ]]; then
    echo -e "${CYAN}[Check 4/4]: Checking for Dockerfile...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: $FILE not found in $(pwd)"
    exit
  fi
}

###

# main()
greetings
check_1
check_2
check_3
check_4

echo -e "\nPassed all checks successfully..."

# Checks over, start main stuff
# build the docker image -> ${docker_image_name}
echo -e "${CYAN}"
echo -e "Building the '${docker_image_name}' image"
echo -e "--------------------------------${NC}\n"
docker build . -t ${docker_image_name}

echo -e "\n${GREEN}Done"

# remove dangling images (if any)
echo -e "\n${CYAN}Removing dangling images (if any)"
echo -e "---------------------------------${NC}\n"
docker rmi $(docker images | grep none | awk '{  print $3 }')
echo -e "\n${GREEN}Done"

# remove mars-container if already exist
docker rm -f ${docker_container_name} &>/dev/null && echo 'Removed old container'

# run docker image with bind mount
echo -e "${CYAN}"
echo -e "Running the ${docker_container_name}"
echo -e "--------------------------${NC}\n"

docker run --name ${docker_container_name} -it --mount type=bind,source=`pwd`,target=/MARS ${docker_image_name}

echo -e "\n${GREEN}Done"
echo -e "${GREEN}Process completed with exit code 0"

# remove container
echo -e "${CYAN}"
echo -e "Removing the ${docker_container_name}"
echo -e "---------------------------${NC}\n"

docker rm ${docker_container_name}

echo -e "${CYAN}"
echo -e "Changing permissions from root user to ${SUDO_USER}"
chown -R ${SUDO_USER} .
echo -e "${GREEN}Done"

# Display output
echo -e "\n${YELLOW}Unless you plan to rerun the script in future, you can safetly delete the images -> ${docker_image_name} and ritikmalik/mars-image"
echo -e "\n${GREEN}Logs are saved in logs.txt"
echo -e "Ouput PDF is saved in output directory with format: 'Output-YYYY-MM-DD.pdf'\n"
