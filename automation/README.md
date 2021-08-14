# Portal to M.A.R.S.

* **System Support:** Currently, M.A.R.S. supports Linux (Debian based) and Mac/OS X based systems. It has been tried and tested for the above mentioned platforms.

* **Language Support:** Currently, M.A.R.S. is capable of producing PDF release for English, Spanish and Chinese languages. For adding a new language refer to [this guide](./add-language_README.md).

All the commands listed below for Linux systems are assuming an installation of debian based system like Ubuntu, Mint, MX, AntiX, etc. However the same commands can used for different package managers and different flavours of linux like `yum`, `pacman` instead of `apt`; just be sure to select the right package name accordingly.

It is assumed that where ever we use the term Linux in the tutorial below, we are referring to a Debain based distro, more specifically **Ubuntu** (20.04), which was the actual system used.

## Launching to M.A.R.S.

There are 2 ways to run M.A.R.S.
1. [Using Docker image](#method-1-the-easy-way---docker-image) (recommended)
2. [Using Python virtual environment](#method-2-the-not-so-easy-way---python-virtual-env)

Each method has been described below in detail for both the platforms (Linux and Mac). You can choose according to your needs. We would recommend the Docker way, because of its simplicity. The py virtual environment way is more for development purposes.

### Method 1: The easy way - Docker image

This is an easy and recommended way to run MARS on your system. Some theory: \
We've already uploaded an image of MARS on docker hub, which contains an installation of all the required packages. We also have an automation script to pull that image, run the container instance and clean it afterwards. You just have to:
* Install docker on your system
* Configure the `yml` file and cover page
* Run the automated script

Our docker image on docker hub can be found [here](https://hub.docker.com/r/ritikmalik/mars-image).

Some stats:
* Docker image compressed size: `842.35 MB` (actual download size)
* Docker image decompressed size: `2.26GB` (actual size on system)

#### Step 1: Cloning MARS

This simple step requires you to ~~colonize~~ clone MARS and move to the appropriate directory:
```bash
git clone https://github.com/chaoss/MARS
cd MARS/automation
```

#### Step 2: Install Docker

* For Linux:
    * In Linux you can use the following 3 commands to install docker:
        ```bash
        curl -fsSL https://get.docker.com -o get-docker.sh
        chmod +x get-docker.sh
        sudo sh get-docker.sh
        ```
    * Or you can refer to the Official guide: https://docs.docker.com/engine/install/#server

* For Mac/OS X:
    * Installing docker for Mac is pretty straightforward
    * Refer to the official guide: https://docs.docker.com/docker-for-mac/install/

#### Step 3: Adding user to Docker group (Linux specific)

This is a Linux specific step, Mac users can ignore this and move on to next step.

Since Docker for Mac runs in a LinuxKit VM, it doesn't require sudo permissions. However, for Linux, in order to run Docker as rootless user, you should add your user to the docker group:
```bash
sudo usermod -a -G docker $USER
reboot
```

_NOTE: a reboot is preferred over log out and log in, in order to re-elevate the privileges_

You can confirm that your user is added to the docker group by running:
```bash
grep docker /etc/group
```

You should see your username in the output along with docker in the same line.

#### Step 4: Configuring the yml config file & Updating the cover page

The only inputs you are supposed to configure is the `yml` config file and the cover page file.

* The `yml` config is the most important piece of MARS as it describes the outline of all the working groups and metrics that need to be included and in which order.
* The cover page file is used to update the release month and year as well as the copyright year.

Both of them can be found in the [`active_user_input`](active_user_input) directory. \
Both the files have their own separate README to avoid congestion here. Refer to this [README](active_user_input) for configuring them.

Once you have confirmed the above changes you can proceed to the next and the final step.

#### Step 5: Docker Automation Script

This is the 5th and final step for MARS. You are required to run the [`generate-release-PDF.sh`](generate-release-PDF.sh) script to generate the PDF.

You should run this script from the current directory which is `automation` as it will look for MARS scripts.

```bash
./generate-release-PDF.sh
```

After running the script you'll be greeted with a simple language selection menu. \
Choosing the language is pretty intuitive.

The system will generate the PDF for the selected language accordingly. You'll find the release PDF in the [`output`](output/) directory with the format - \
`<Language>-Release-YYYY-MM-DD.pdf` \
Eg. `English-Release-2021-07-28.pdf`

You can refer to the GIF below for a quick demo of this last step:

* For English Release:

<img src="../assets/MARS_English.gif" width="750" height="850" />

* For translations release:

<img src="../assets/MARS_Chinese.gif" width="750" height="850" />

#### Behind the scenes on Step 5:

**A brief overview of what this automation script (`generate-release-PDF.sh`) does:**
* Perform OS detection: i.e. Linux or Mac OS/X
* Runs 5 sanity checks:
    1. Check if Docker is installed
    2. check if user is in Docker group (only for Linux)
    3. Check if Docker is running
    4. check if current directory is correct
    5. check if Dockerfile for detected platform exist
* Brings in the correct `Dockerfile` and build the Docker image: `chaoss-mars`
* Remove dangling images (if any)
* Remove `mars-container` if already exist
* Run the Docker image with bind mount in current diretory
* Spin up a container with the name: `mars-container`
* Display a langauge selection menu:
    * If user chooses English:
        * Generate English release PDF as per the config in English `yml` file and cover page
    * If user chooses other languages:
        * Clone translations repository and auto-detect the languages
        * Take user input for language and auto-select the `yml` file and generate PDF
* Remove the `mars-container`
* Display success message and paths to log files and output PDF, along with instructions to remove the Docker images
* Appropriate error handling and user input sanitization has been implemented
* A fresh color scheme has been used to make important text more distinguishable and visually appealing
* The log file will be stored in current directory as `logs.txt` while the output PDF can be found in the [`output`](output/) directory with the format - `<Language>-Release-YYYY-MM-DD.pdf`.

**Resolving the cross-platform issue**
* Here we are using 2 Dockerfiles, 1 for Linux and 1 for Mac. The idea of 2 Dockerfile is being used because in Linux the files created inside the Docker container are owned by root. So the normal user will face permission issue on the PDF and log files. However, in Mac, no such problem is encountered and the files are owned by the logged in user. This forced us to create a separate Dockerfile which is platform dependent. The automation script detects the platform and proceeds with the correct Dockerfile accordingly.

**How we bypass the root permissions in Docker (in Linux)**
* The Dockerfile for Linux creates a new user - `user`, with the userID and groupID of your current logged in user, so now the user inside Docker container has same previlages as your current user. Now there will not be any permission issues while accessing the files created inside the container while using bind mount (without this, the PDF owner will be the root user by default)

Both the Dockerfiles can be found in the [`passive_user_input`](passive_user_input) directory

**Resolving the multiple language issue**
* For Enlgish, the WGs have separate repositories while for the Spanish and Chinese, both of them have all the WGs in a single `transtions` repository. Still you might notice that the `yml` file structure for every language is the same. This is because we are treating English as just any other language. We are more interested in the paths to the focus-areas and metric markdowns in the WG rather than the location of the WGs itself, be it embedded in a single repository or across multiple. This gives us much flexibilty to add a new language or pull from some different repositories.


### Method 2: The not so easy way - Python virtual env

In this process, you are supposed to install packages and run the scripts manually in a python virtual environment.

#### Step 1: Install packages

We'll be using the `xelatex` engine and `pandoc` for converting the markdowns to PDF, so you need to install them along with other packages:

* For Linux:
    ```bash
    sudo apt install -y git wget texlive-xetex pandoc python3-pip python3-venv texlive-lang-chinese ttf-mscorefonts-installer 
    ```
* For Mac:
    ```bash
    sudo brew install git wget pandoc python3
    pip3 install virtualenv virtualenvwrapper
    ```
    * Install `xelatex`:
        * Refer to https://tug.org/mactex/
        * Alternatively, you can install [Miketex](https://miktex.org/download) to download only the required packages during PDF generation
    * Install Chinese langauge pack:
        * Refer to [_this link_](https://ports.macports.org/port/texlive-lang-cjk/)
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
cd MARS/automation
```

#### Step 4: Install other requirements

You need to install the python packages listed in [`requirements.txt`](requirements.txt):
```bash
pip3 install -r requirements.txt
```

#### Step 5: Configuring the yml config file & Updating the cover page

This step is same as [Step 4](#step-4-configuring-the-yml-config-file--updating-the-cover-page) in the Docker approach.

#### Step 6: Running the final scripts

The following command is used to generate the output PDF:
```bash
python3 main.py | tee logs.txt
```
The log file will be stored in current directory as `logs.txt` while the output PDF can be found in the [`output`](output/) directory with the format - `<Language>-Release-YYYY-MM-DD.pdf`.

To deactivate the virtual env you can use the deactivate command:
```bash
deactivate
```
