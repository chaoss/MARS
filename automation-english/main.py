import os
import shutil
import sys
import subprocess
from pprint import pprint
from datetime import datetime
import pypandoc
import yaml
import validators
import helper

##### Global Vars #####

included_wgs = []
yml_filename = "working-groups-config.yml"
master_file_path = "master.tex"
test_dir = "test_env"
current_dir = "./"

def copy_file(source_filepath, dest_path):

    if os.path.isfile(dest_path):
        print(f"Warning: File with same name already exists at destination: {source_filepath}")
    else:
        try:
            print(f"\nCopying: {source_filepath}")
            shutil.copy2(source_filepath, dest_path)
            print(f"Copied Successfully")
        except PermissionError:
            print("Error: Permission denied.")
            sys.exit(1)
        except:
            print("Error: Unable to copy file.")
            sys.exit(1)

def copy_dir_files(source_folder_path, dest_folder_path):

    try:
        files = os.listdir(source_folder_path)
        for fname in files:
            if os.path.isfile(os.path.join(dest_folder_path, fname)):
                print(f"File with same name already exists at destination: {os.path.join(source_folder_path, fname)}")
            else:
                copy_file(os.path.join(source_folder_path, fname), dest_folder_path)
    except NotADirectoryError:
        print(f"Error: Source path is not a directory :{source_folder_path}")
        sys.exit(1)
    except:
        print(f"Error: Unable to list files in :{source_folder_path}")
        sys.exit(1)

def convert_md2tex(md_filename, latex_filename):

    print(f"Converting {md_filename} file to LaTeX")
    output = pypandoc.convert_file(md_filename, 'latex', outputfile=latex_filename, extra_args=['-f', 'gfm'])
    assert output == ""
    print(f"Created successfully: {latex_filename}")

def convert_tex2pdf(tex_filename, pdf_filename):

    print(f"\nConverting {tex_filename} file to PDF")
    output = pypandoc.convert_file(tex_filename, 'pdf', outputfile=pdf_filename, extra_args=['-f', 'latex',
                                                                                                 '--pdf-engine=xelatex',
                                                                                                 '--include-in-header', 'header_1.tex',
                                                                                                 '--highlight-style', 'zenburn',
                                                                                                 '-V', 'geometry:margin=0.8in',
                                                                                                 '-V', 'monofont:DejaVuSansMono.ttf',
                                                                                                 '-V', 'mathfont:texgyredejavu-math.otf',
                                                                                                 '-V', 'geometry:a4paper',
                                                                                                 '-V', 'colorlinks=true',
                                                                                                 '-V', 'linkcolour:blue',
                                                                                                 '-V', 'fontsize=12pt',
                                                                                                 '--toc', '--toc-depth= 3',
                                                                                                 '--include-before-body', 'cover.tex',
                                                                                                 '--include-after-body', 'end-matter.tex'])
    assert output == ""
    print(f"Conversion process successful: {pdf_filename}")

def clean_directory(folder_path):
    try:
        if os.path.isdir(folder_path):
            print(f"\nCleaning directory: {folder_path}")
            shutil.rmtree(folder_path)
            print("Directory cleaned Successfully")
    except:
        print(f"\nWarning: Unable to clean directory: {folder_path}")

def load_yaml(file_path):

    try:
        with open(file_path) as stream:
            data = yaml.safe_load(stream)
            pprint(data)
            return data
    except yaml.YAMLError as exc:
        print(exc)
        print("Error: Unable to load data from YAML file.")
        sys.exit(1)

def decrease_level(metric_path):

    try:
        print(f"\nDecreasing heading levels by 2 in metric: {metric_path}")
        cmd = 'sed -i "s/^\#/###/g" ' + metric_path
        os.system(cmd)
    except:
        print(f"Error: Unable to decrease heading levels in metric: {metric_path}.\nMake sure the metric follows the template.")
        sys.exit(1)

def delete_dictkey(key, dictionary):

    if key in dictionary:
        del dictionary[key]
    else:
        print(f"Warning: Key- {key} not found in {dictionary}")

def is_url(string):

    if validators.url(string):
        return True
    else:
        return False

def clone_repo(url, name, branch):

    try:
        subprocess.check_call(['git', 'clone', '-b', branch, url, name])
    except:
        print(f"Error: Unable to clone/checkout repository from {url}")
        print("Verify the repository details specified in YAML file.")
        sys.exit(1)


def main():

    global included_wgs
    global yml_filename
    global master_file_path
    global test_dir
    global current_dir

    # Clean the test_dir for residual files
    clean_directory(test_dir)

    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)
        os.chdir(test_dir)
    else:
        os.chdir(test_dir)
    
    print(f"\nSwitching to {test_dir}")

    # Copy the scripts
    copy_dir_files("../active_user_input", current_dir)
    copy_dir_files("../passive_user_input", current_dir)


    # Read the yml file
    print("\nReading the YML file:\n")
    yaml_data = load_yaml(yml_filename)

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
                        print(f"Error: Could not incorporate {page} in front-matter.\nPlease make sure that the URL is valid. Only Markdown/LaTeX file format is supported.")
                        sys.exit(1)
                elif os.path.splitext(page)[1] == ".md":
                    convert_md2tex(page, os.path.splitext(page)[0]+".tex")
                    front_matter.write(f"\input{{{os.path.splitext(page)[0]}}} \n")
                elif os.path.splitext(page)[1] == ".tex":
                    front_matter.write(f"\input{{{os.path.splitext(page)[0]}}}"+"\n")
                else:
                    print(f"Error: Could not incorporate {page} in front-matter.\nPlease make sure that the filename is valid. Only Markdown/LaTeX file format is supported.")
                    sys.exit(1)
        else:
            print("Warning: No documents detected for the front-matter")

    with open(master_file_path, "a") as master_file:
        master_file.write("\n \include{front-matter}")

    # Create and include end-matter pages
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
                        print(f"Error: Could not incorporate {page} in end matter.\nPlease make sure that the URL is valid. Only Markdown/LaTeX file format is supported.")
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
                    print(f"Error: Could not incorporate {page} in end matter.\nPlease make sure that the filename is valid. Only Markdown/LaTeX file format is supported.")
                    sys.exit(1)

        else:
            print("Warning: No documents detected for the end-matter")

    delete_dictkey("front-matter", yaml_data)
    delete_dictkey("end-matter", yaml_data)


    # LOOP #1: For Working Groups
    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg']:

            # clone repo with specified branch in yaml data
            print(f"\nCloning from URL: {yaml_data[wg_name]['github-link']}\nBranch: {yaml_data[wg_name]['github-branch']}\n")
            clone_repo(yaml_data[wg_name]['github-link'], wg_name, yaml_data[wg_name]['github-branch'])

            included_wgs.append(wg_name)
            included_focus_areas = []
            focus_area_list = []

            # LOOP #2: For Focus Areas
            for focus_area, metrics in yaml_data[wg_name]["focus-areas"].items():
                converted_tex_files = []
                if metrics is not None:

                    # LOOP #3: For Metrics
                    for metric in metrics:
                        metric_path = os.path.join(wg_name, "focus-areas", focus_area, metric)

                        copy_file(metric_path, current_dir)
                        decrease_level(metric)
                        tex_filename = os.path.splitext((metric))[0] + ".tex"                        
                        
                        convert_md2tex(metric, tex_filename)
                        converted_tex_files.append(tex_filename)

                    # copy images of particular focus-area
                    if not os.path.isdir("images"):
                        print(f"\nMaking images directory")
                        os.makedirs("images")
                    copy_dir_files(os.path.join(wg_name, "focus-areas", focus_area, "images"), os.path.join(current_dir, "images"))

                    focus_area_README = os.path.join(wg_name, "focus-areas", focus_area, "README.md")

                    # to be used in focus-areas table for WG.tex
                    focus_area_list.append([focus_area, focus_area_README])

                    # create focus_area.tex file and add table
                    focus_area_filename = wg_name+"_"+focus_area+".tex"
                    helper.generate_focus_areas(focus_area, focus_area_filename, focus_area_README, metrics)
                    included_focus_areas.append(focus_area_filename)

                    # Add inclusion commands for metrics
                    with open(focus_area_filename, "a") as fa_tex_file:
                        fa_tex_file.write("\n")
                        for metric_tex_file in converted_tex_files:
                            fa_tex_file.write(f"\input{{{os.path.splitext(metric_tex_file)[0]}}} \n")

            # create WG.tex file
            wg_tex_file_path = os.path.join(current_dir, wg_name+".tex")

            with open(wg_tex_file_path, "w") as wg_tex_file:
                wg_tex_file.write("\n")

                # add focus areas table to WG.tex
                helper.focus_areas_table(wg_tex_file, yaml_data[wg_name]['wg-fullname'], focus_area_list)
                wg_tex_file.write("\n\clearpage\n")

                for fa in included_focus_areas:
                    wg_tex_file.write(f"\input{{{os.path.splitext(fa)[0]}}} \n")

    # create master file to include WG.tex files
    with open(master_file_path, "a") as master_file:
        master_file.write("\n")

        for wg in included_wgs:
            master_file.write(f"\include{{{wg}}} \n")

        master_file.write("\n\end{document}")
    
    # PDF name = output-YYYY-MM-DD.pdf
    output_filename = "Output-" + datetime.today().strftime('%Y-%m-%d') + ".pdf"

    convert_tex2pdf(master_file_path, output_filename)
    copy_file(output_filename, "../output")

if __name__ == "__main__":
    main()
