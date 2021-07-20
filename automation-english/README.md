# Portal to M.A.R.S.

Currently, M.A.R.S. supports Linux (Debian based) and Mac/OS X based systems. It has been tried and tested for the above mentioned platforms.

All the commands listed below for Linux systems are assuming an installation of debian based system like Ubuntu, Mint, MX, AntiX, etc. However the same commands can used for different package managers and different flavours of linux like `yum`, `pacman` instead of `apt`; just be sure to select the right package name accordingly.

It is assumed that where ever we use the term Linux in the tutorial below, we are referring to a Debain based distro, more specifically **Ubuntu**, which was the actual system used.

## Launching to M.A.R.S.

There are 2 ways to run M.A.R.S.
1. Using Docker image (recommended)
2. Using Python virtual environment

Each method has been described below in detail. You can choose according to your needs.

### Method 1: The easy way - Docker image

This is an easy and recommended way to run MARS on your system. Some theory: \
We've already uploaded an image of MARS on docker hub, which contains an installation of all the required packges. We also have an automation script to pull that image, run the container instance and clean it afterwards. You just have to install docker in your system, confirm the structure of `yml` config file and run the automated script.

Our docker image on docker hub can be found [here](https://hub.docker.com/r/ritikmalik/mars-image).

#### Step 1: Cloning MARS

This simple step requires you to ~~colonize~~ clone MARS and move to appropriate directory:
```bash
git clone https://github.com/chaoss/MARS
cd MARS/automation-english
```

#### Step 2: Install Docker

* For Linux:
    * In Linux you can use the following 3 commands to install docker:
        ```bash
        curl -fsSL https://get.docker.com -o get-docker.sh
        chmod +x get-docker.sh
        sudo sh get-docker.sh
        ```
    * Official guide: https://docs.docker.com/engine/install/#server

* For Mac/OS X:
    * Installing docker for Mac is pretty straightforward
    * Refer to the official guide: https://docs.docker.com/docker-for-mac/install/

#### Step 3: Adding user to Docker group

In order to run Docker as rootless user, you should add your user to the docker group:
```bash
sudo usermod -a -G docker $USER
reboot
```

_NOTE: a reboot is preferred over log out and log in, in order to re-elevate the privileges_

You can confirm that your user is added to the docker group by running:
```bash
grep docker /etc/group
```

You should see your username in the output along with docker.

#### Step 4: Configuring the yml config file & Updating the cover page

The yml config is the most important piece of MARS as it describes the outline of working groups and metrics that need to be included and in which order. The yml file has it own separate README to avoid congestion here. Refer to this [yml README](active_user_input) for configuring it.

Make sure to also update the release month and year as well as the copyright year in the [cover page](active_user_input/cover.tex) 

Once you have confirmed the above changes you can proceed to the next and the final step.

#### Step 5: Docker Automation Script

This is the 5th and final step for MARS. You are required to run the [`lindocX.sh`](lindocX.sh) script to generate the PDF.

You should run this script from the current directory which is `automation-english` as it will look for the `Dockerfile` and other MARS scripts.

```bash
./lindocX.sh
```
You'll find the output PDF in the [`output`](output/) directory with the format - `Output-YYYY-MM-DD.pdf`

##### Extra stuff on Step 5:

A brief overview of what this automation script does:
* Run 5 sanity checks:
    1. Check if Docker is installed
    2. check if user is in Docker group
    3. Check if Docker is running
    4. check if current directory is correct
    5. check if Dockerfile exist
* Looks for `Dockerfile` and build the Docker image: `chaoss-mars`
* Remove dangling images (if any)
* Remove `mars-container` if already exist
* Run the Docker image with bind mount. Container name: `mars-container`
* Remove the `mars-container`
* Display success message and paths to log files and output PDF

The script creates a new user with your userID and groupID so there is no permission issues while accessing the files created inside the container while using bind mount.

The log file will be stored in current directory as `logs.txt` while the output PDF can be found in the [`output`](output/) directory with the format - `Output-YYYY-MM-DD.pdf`.

### Method 2: The not so easy way - Python virtual env

In this process, you are supposed to install packages and run the scripts manually in a python virtual environment.

#### Step 1: Install packages

We'll be using the `xelatex` engine and `pandoc` for converting the markdowns to PDF, so you need to install them along with other packages:

* For Linux:
    ```bash
    sudo apt install -y git wget texlive-xetex pandoc python3-pip python3-venv ttf-mscorefonts-installer
    ```
* For Mac:
    ```bash
    sudo brew install git wget pandoc python3
    pip3 install virtualenv virtualenvwrapper
    ```
    * Install `xelatex`:
        * Refer to https://tug.org/mactex/
        * Alternatively, you can install [Miketex](https://miktex.org/download) to download only the required packages during PDF generation
    * Install fonts:
        * Refer to [_this link_](https://www.linickx.com/osx-how-to-install-the-microsoft-fonts)

#### Step 2: Create a virtual environment

Switch to the directory of your choice and create a new Python virtual environment:

```bash
python3 -m venv MARS_venv

# activate the env
source MARS_venv/bin/activate
```

#### Step 3: Cloning MARS

You can now clone the MARS repo in this env:
```bash
git clone https://github.com/chaoss/MARS
cd MARS/automation-english
```

#### Step 4: Install other requirements

You need to install the python packages listed in [`requirements.txt`](requirements.txt):
```bash
pip3 install -r requirements.txt
```

#### Step 5: Configuring the yml config file

This step is same as [Step 4](#step-4-configuring-the-yml-config-file) in the Docker approach.

#### Step 6: Running the final scripts

The following command is used to generate the output PDF:
```bash
python3 main.py | tee logs.txt
```
The log file will be stored in current directory as `logs.txt` while the output PDF can be found in the [`output`](output/) directory with the format - `Output-YYYY-MM-DD.pdf`.

To deactivate the virtual env you can use the deactivate command:
```bash
deactivate
```
