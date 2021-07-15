# Run M.A.R.S. using CLI 

Currently, M.A.R.S only supports Linux (Debian based) and MacOS based systems.

Follow the steps given below to run M.A.R.S. from the command line.

## Install a LaTeX distribution 

- Debian-based : `$ sudo apt-get install texlive-full`
- MacOS : <https://tug.org/mactex/>

Alternatively, you can install [Miketex](https://miktex.org/download) to download only the required packages during PDF generation.

Make sure to set the package installation settings to install missing packages automatically if using MikeTeX.

## Install Pandoc 

Follow the instructions on the links given below to install Pandoc

- Debian-based: <https://pandoc.org/installing.html#linux>
- MacOS: <https://pandoc.org/installing.html#macos>

## Create a new virtual environment 

Switch to the directory of your choice and create a new Python virtual environment.
  
```commandline
$ python3 -m venv MARS_venv
```
  
Activate the environment
```commandline
$ source MARS_venv/bin/activate
```

## Clone the M.A.R.S. repo

```commandline
$ git clone https://github.com/chaoss/MARS
$ cd MARS/automation-english
```

## Update the YAML file and cover page

The YAML file is located in the 

## Output







