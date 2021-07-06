#!/bin/bash
# This script is to automate the Docker instance for M.A.R.S. on Linux/Windows
# Run it as ROOT

### Global Vars ###
MARS_link='https://github.com/chaoss/MARS'
cur_dir='automation-english'
docker_hub_image_name='ritikmalik/mars-image:beta'
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
    echo -e "${CYAN}[Check 1/5]: Checking for root permission...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Please run as root\n${NC}"
    exit 1
  fi
}

check_2(){
  # Check if Docker is installed
  if [[ $(which docker) && $(docker --version) ]]; then
    echo -e "${CYAN}[Check 2/5]: Checking if Docker is installed...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Docker not found, please install Docker.\n"
    echo -e "${CYAN}Run the following 3 commands to install Docker on Linux:\n"
    echo -e '1. curl -fsSL https://get.docker.com -o get-docker.sh'
    echo -e '2. chmod +x get-docker.sh'
    echo -e '3. sudo sh get-docker.sh'
    echo -e
    echo -e "Or refer to official doc: https://docs.docker.com/engine/install/ \n${NC}"
    exit 1
  fi
}

check_3(){
  # Check if docker is running
if docker info >/dev/null 2>&1; then
    echo -e "${CYAN}[Check 3/5]: Checking if Docker is running...${GREEN}Yes"
else
    echo -e "${RED}[Error]: Docker does not seem to be running, run it first and retry\n${NC}"
    exit 1
fi

}

check_4(){
  # check if current directory == ${cur_dir}
  if [ "$(pwd | awk -F '/' '{ print $NF }')" = "${cur_dir}" ]; then
    echo -e "${CYAN}[Check 4/5]: Checking for correct directory...${GREEN}Yes"
  else
    echo -e "${RED}[Error]: Please run this script in '${cur_dir}' directory\n${NC}"
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
    exit 1
  fi
}

check_exit(){
  # check exit code of command
  if [ $1 -eq 0 ]; then
    echo -e "\n${GREEN}[+] Command executed with exit code $1"
  else
    echo -e "\n${RED}[Error]: Process stopped with exit code $1\n${NC}"
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

echo -e "\n${GREEN}Passed all checks successfully..."

# Checks over, start main stuff
# build the docker image -> ${docker_image_name}
echo -e "\n${CYAN}Building the '${docker_image_name}' image"
echo -e "--------------------------------${NC}\n"
docker build . -t ${docker_image_name}

check_exit $?

# remove dangling images (if any)
echo -e "\n${CYAN}Removing dangling images (if any)"
echo -e "---------------------------------${NC}\n"
docker rmi $(docker images | grep none | awk '{  print $3 }') 2> /dev/null

echo -e "\n${GREEN}Done"

# remove mars-container if already exist
echo -e "\n${CYAN}Removing ${docker_container_name} (if already exist)...${NC}"
docker rm -f ${docker_container_name} &>/dev/null && echo 'Removed old container'

echo -e "\n${GREEN}Done"

# run docker image with bind mount
echo -e "\n${CYAN}Running the ${docker_container_name}"
echo -e "--------------------------${NC}\n"

docker run --name ${docker_container_name} -it --mount type=bind,source=`pwd`,target=/MARS ${docker_image_name}

check_exit $?

# remove container
echo -e "\n${CYAN}Removing the ${docker_container_name}"
echo -e "---------------------------${NC}\n"

docker rm ${docker_container_name}

check_exit $?

echo -e "\n${CYAN}Changing permissions from root user to ${YELLOW}${SUDO_USER}"
chown -R ${SUDO_USER}:${SUDO_USER} .

check_exit $?
echo -e "\n${GREEN}Done!\nIf you are seeing this message it means the script ran successfully!"

# Display output
echo -e "\n${YELLOW}Unless you plan to rerun the script in future, you can safetly delete the images -> ${docker_image_name} and ${docker_hub_image_name}"
echo -e "\n${GREEN}Logs are saved in ${YELLOW}logs.txt"
echo -e "${GREEN}Ouput PDF is saved in ${YELLOW}output/${GREEN} directory with format: ${YELLOW}'Output-YYYY-MM-DD.pdf'\n"
