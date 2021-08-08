# General helping functions used throughout the project
import os
import shutil
import sys
import subprocess
from pprint import pprint
import pypandoc
import yaml
import validators
import main

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def copy_file(source_filepath, dest_path):
    """Copies file from source path to destination.
    Replaces the file if it already exists
    """

    if os.path.isfile(dest_path):
        print(color.RED,f"Warning: File with same name already exists at destination: {source_filepath}",color.END)
    else:
        try:
            print(f"\nCopying: {source_filepath}")
            shutil.copy2(source_filepath, dest_path)
            print(f"Copied Successfully")
        except PermissionError:
            print(color.RED,"Error: Permission denied.",color.END)
            sys.exit(1)
        except:
            print(color.RED,"Error: Unable to copy file.",color.END)
            sys.exit(1)

def copy_dir_files(source_folder_path, dest_folder_path):
    """Copies all files from source directory to destination directory
    Replaces the files if they already exist
    """

    try:
        if os.path.isdir(source_folder_path):
            files = os.listdir(source_folder_path)
            for fname in files:
                if os.path.isfile(os.path.join(dest_folder_path, fname)):
                    print(color.RED,f"File with same name already exists at destination: {os.path.join(source_folder_path, fname)}",color.END)
                else:
                    copy_file(os.path.join(source_folder_path, fname), dest_folder_path)
        else:
            print(color.RED,f"Warning: Source directory does not exist: {source_folder_path}",color.END)
    except NotADirectoryError:
        print(color.RED,f"Error: Source path is not a directory :{source_folder_path}",color.END)
        sys.exit(1)
    except:
        print(color.RED,f"Error: Unable to list files in :{source_folder_path}",color.END)
        sys.exit(1)

def convert_md2tex(md_filename, latex_filename):
    """Converts specified markdown file to LaTeX"""

    print(f"Converting {md_filename} file to LaTeX")
    output = pypandoc.convert_file(md_filename, 'latex', outputfile=latex_filename, extra_args=['-f', 'gfm'])
    assert output == ""
    print(f"Created successfully: {latex_filename}")

def clean_directory(folder_path):
    """Deletes the specified directory"""

    try:
        if os.path.isdir(folder_path):
            print(f"\nCleaning directory: {folder_path}")
            shutil.rmtree(folder_path)
            print("Directory cleaned Successfully")
    except:
        print(color.RED,f"\nWarning: Unable to clean directory: {folder_path}",color.END)

def load_yaml(file_path):
    """Loads data from given YAML file in the form of dictionary"""

    try:
        with open(file_path) as stream:
            data = yaml.safe_load(stream)
            pprint(data)
            return data
    except yaml.YAMLError as exc:
        print(exc)
        print(color.RED,"Error: Unable to load data from YAML file.",color.RED)
        sys.exit(1)

def decrease_level(metric_path):
    """Replaces '# ' with '### ' anywhere in the file"""

    try:
        print(f"\nDecreasing heading levels by 2 in metric: {metric_path}")
        cmd = 'sed -i "s/^\#/###/g" ' + metric_path
        os.system(cmd)
    except:
        print(color.RED,f"Error: Unable to decrease heading levels in metric: {metric_path}.\nMake sure the metric follows the template.",color.END)
        sys.exit(1)

def delete_dictkey(key, dictionary):
    """Deletes given key from given dictionary"""

    if key in dictionary:
        del dictionary[key]
    else:
        print(color.RED,f"Warning: Key- {key} not found in {dictionary}",color.RED)

def is_url(string):
    """Checks if the given string is a valid URL"""

    if validators.url(string):
        return True
    else:
        return False

def clone_repo(url, name, branch):
    """Clones repository and checkout the given branch"""

    try:
        subprocess.check_call(['git', 'clone', '-b', branch, url, name])
    except subprocess.CalledProcessError:
        print(color.RED,f"Error: Repository with name: {name} already exists")
        print("Please ensure only one link is present in the YAML file")

    except:
        print(color.RED,f"Error: Unable to clone/checkout repository from {url}")
        print("Verify the repository details specified in YAML file.",color.END)
        sys.exit(1)

def add_front_matter(yaml_data):
    """Creates the latex file to add content just after
    the table of contents in PDF
    """

    # Create and include front matter files
    with open("front-matter.tex", "w") as front_matter:
        if yaml_data["front-matter"] is not None:
            for page in yaml_data["front-matter"]:
                if is_url(page):
                    print(f"\nDownloading file: {page}")
                    os.system(f"wget {page}")
                    filename = os.path.basename(page)
                    name, extension = os.path.splitext(filename)
                    if extension == ".md":
                        convert_md2tex(filename, name+".tex")
                        front_matter.write(f"\input{{{name}}} \n")
                    elif extension == ".tex":
                        front_matter.write(f"\input{{{name}}} \n")
                    else:
                        print(color.RED,f"Error: Could not incorporate {page} in front-matter.\nPlease make sure that the URL is valid. Only Markdown/LaTeX file format is supported.",color.END)
                        sys.exit(1)
                elif os.path.splitext(page)[1] == ".md":
                    convert_md2tex(page, os.path.splitext(page)[0]+".tex")
                    front_matter.write(f"\input{{{os.path.splitext(page)[0]}}} \n")
                elif os.path.splitext(page)[1] == ".tex":
                    front_matter.write(f"\input{{{os.path.splitext(page)[0]}}}"+"\n")
                else:
                    print(color.RED,f"Error: Could not incorporate {page} in front-matter.\nPlease make sure that the filename is valid. Only Markdown/LaTeX file format is supported.",color.END)
                    sys.exit(1)
        else:
            print(color.RED,"Warning: No documents detected for the front-matter",color.END)

    with open(main.master_file_path, "a") as master_file:
        master_file.write("\n\include{front-matter}")

def add_end_matter(yaml_data):
    """Creates latex file to add content at the end of PDF"""

    # Create and include end matter files
    with open("end-matter.tex", "w") as end_matter:
        if yaml_data["end-matter"] is not None:
            for page in yaml_data["end-matter"]:
                if is_url(page):
                    print(f"\nDownloading file: {page}")
                    os.system(f"wget {page}")
                    filename = os.path.basename(page)
                    name, extension = os.path.splitext(filename)
                    if name == "LICENSE":
                        os.rename("LICENSE", "LICENSE.md")
                        convert_md2tex("LICENSE.md", "LICENSE.tex")
                        end_matter.write("\clearpage\n\section{LICENSE}\n\input{LICENSE}\n")
                    elif extension == ".md":
                        convert_md2tex(filename, name+".tex")
                        end_matter.write(f"\input{{{name}}} \n")
                    elif extension == ".tex":
                        end_matter.write(f"\input{{{name}}} \n")
                    else:
                        print(color.RED,f"Error: Could not incorporate {page} in end matter.\nPlease make sure that the URL is valid. Only Markdown/LaTeX file format is supported.",color.END)
                        sys.exit(1)

                elif os.path.splitext(page)[1] == ".md":
                    convert_md2tex(page, os.path.splitext(page)[0]+".tex")
                    end_matter.write(f"\input{{{os.path.splitext(page)[0]}}} \n")
                elif os.path.splitext(page)[1] == ".tex":
                    end_matter.write(f"\input{{{os.path.splitext(page)[0]}}}"+"\n")
                elif os.path.splitext(page)[0] == "LICENSE" and os.path.splitext(page)[1] == "":
                    os.rename("LICENSE", "LICENSE.md")
                    convert_md2tex("LICENSE.md", "LICENSE.tex")
                    end_matter.write("\clearpage\n\section{LICENSE}\n\input{LICENSE}\n")
                else:
                    print(color.RED,f"Error: Could not incorporate {page} in end matter.")
                    print(f"Please make sure that the filename is valid. Only Markdown/LaTeX file format is supported.",color.END)
                    sys.exit(1)

        else:
            print(color.RED,"Warning: No documents detected for the end-matter",color.END)


def spilt_by_colon(string):
    """Splits the string in two using priority list of colon delimiters.
    Returns only the latter half
    """

    colon_list = [":**", "：**", ":", "：", "ː", "˸", "᠄", "⍠", "꞉", "︓", " "]
    i=0
    while (i<len(colon_list)):
        try:
            a, b = string.split(colon_list[i], maxsplit=1)
            return b.strip()
        except ValueError:
            i+=1
        except:
            print(color.RED,f"Error: Unexpected error while extracting data from string - {string}",color.END)
            break
    print(color.RED,"Error: No colon delimiter found. Please make sure that metric/focus_area README follow the template.",color.END)
    sys.exit(1)

def extract_question(metric):
    """Extracts the name and question from the given metric"""

    with open(metric) as f:
        data = f.readlines()
    data = [x.strip() for x in data]

    # filter out empty strings
    data = list(filter(None, data))

    # data[0] = '# Technical Fork'
    metric_name = data[0].split(maxsplit=1)[1]

    # data[1] = 'Question: question part of the metric'
    metric_question = spilt_by_colon(data[1])

    return metric_name, metric_question

def extract_goal(focus_area_README):
    """Extracts the name and goal from given focus area README"""

    with open(focus_area_README) as f:
        data = f.readlines()
    data = [x.strip() for x in data]

    # filter out empty strings
    data = list(filter(None, data))

    focus_area_name = data[0].split(maxsplit=1)[1]
    focus_area_goal = spilt_by_colon(data[1])

    return focus_area_name, focus_area_goal

def generate_focus_areas(focus_area_filename, focus_area_README, metrics, english_template):
    """Dynamically creates the table of metrics"""

    table_head = english_template.template_focus_areas
    table_tail = english_template.template_end

    focus_area_name, focus_area_goal = extract_goal(focus_area_README)

    table_head = table_head.replace("$FOCUS_AREA_NAME$", focus_area_name)
    table_head = table_head.replace("$FOCUS_AREA_GOAL$", focus_area_goal)

    for metric in metrics:
        metric_name, metric_question = extract_question(metric)
        table_head += '\t\t' + metric_name + ' & ' + metric_question + ' \\\\ \n\t\t\hline\n'

    table_head += table_tail

    ## TODO: add the name of metrics files
    # \input{techical-fork} 
    # .... metrics...

    # file_name = focus_area_name + '.tex'
    with open(focus_area_filename, 'w') as f:
        f.write(table_head)

    print(f"\nGenerating focus-area file = {focus_area_filename}")

def focus_areas_table(wg_tex_file, section_name, focus_areas_list, language_template):
    """Dynamically creates tables of focus areas in a working group"""

    table_head = language_template.template_working_group
    table_tail = language_template.template_end

    table_head = table_head.replace("$SECTION_NAME$", section_name)

    for FA in focus_areas_list:

        # FA[0] = focus_area_name
        # FA[1] = focus_area_README.md

        focus_area_name, focus_area_goal = extract_goal(FA[1])
        table_head += '\t\t' + focus_area_name + ' & ' + focus_area_goal + ' \\\\ \n\t\t\hline\n'

    table_head += table_tail
    wg_tex_file.write(table_head)

def print_summary(wg_count, focus_area_count, metric_count):

    print()
    print(color.CYAN + "\n" + "="*10 + color.YELLOW + " SUMMARY " + color.CYAN + "="*10 + color.GREEN)
    print(f"Total working groups: {wg_count}")
    print(f"Total focus areas: {focus_area_count}")
    print(f"Total metrics: {metric_count}",color.CYAN)
    print("="*29,color.END)

def print_final_msg(pdf_filename):

    print(color.CYAN)
    print("Created the final PDF ->",color.GREEN,pdf_filename)
    print(color.CYAN)

    final_path = "./output/" + pdf_filename
    print("\nLogs are saved in", color.GREEN, "logs.txt", color.CYAN)
    print("Output PDF is saved in", color.GREEN, final_path, color.END)
