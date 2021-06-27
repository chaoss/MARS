import os
import shutil
import pypandoc
import re
import yaml, subprocess
from pprint import pprint
import helper

# TODO: Implement error handling & check shutil.copy functions

def copy_file(source_filepath, dest_path):

    # TODO: provide support for optional replace flag
    if os.path.isfile(dest_path):
        print(f"File with same name already exists at destination: {source_filepath}")
    else:
        print(f"Copying: {source_filepath}")
        shutil.copy2(source_filepath, dest_path)
        print(f"Copied Successfully")

def copy_dir_files(source_folder_path, dest_folder_path):

    # TODO: provide support for optional replace flag
    try:
        files = os.listdir(source_folder_path)
    except NotADirectoryError:
        print(f"Source path is not a directory :{source_folder_path}")
    except:
        print(f"Unable to list files in :{source_folder_path}")

    for fname in files:
        print(os.path.join(dest_folder_path, fname))
        if os.path.isfile(os.path.join(dest_folder_path,fname)):
            print(f"File with same name already exists at destination: {os.path.join(source_folder_path, fname)}")
        else:
            try:
                print(f"Copying: {os.path.join(source_folder_path, fname)}")
                shutil.copy2(os.path.join(source_folder_path, fname), dest_folder_path)
                print(f"Copied Successfully")
            except shutil.SameFileError:
                print("Source and destination represents the same file.")
            except PermissionError:
                print("Permission denied.")
            except:
                print("Error occurred while copying file.")

def convert_md2tex(md_filename, latex_filename):

    try:
        print(f"Converting {md_filename} file to LaTeX")
        output = pypandoc.convert_file(md_filename, 'latex', outputfile=latex_filename, extra_args=['-f', 'gfm'])
        assert output == ""
        print(f"Created successfully: {latex_filename}")
    except:
        print(f"Unable to convert to LaTeX: {md_filename}")

def convert_tex2pdf(tex_filename, pdf_filename):

    print(f"Converting {tex_filename} file to PDF")
    output = pypandoc.convert_file(tex_filename, 'pdf', outputfile=pdf_filename, extra_args=['-f', 'latex',
                                                                                                '--pdf-engine=xelatex',
                                                                                                 '-H', 'header_1.tex',
                                                                                                 '--highlight-style', 'zenburn',
                                                                                                 '-V', 'geometry:margin=0.8in',
                                                                                                 '-V', 'monofont:DejaVuSansMono.ttf',
                                                                                                 '-V', 'mathfont:texgyredejavu-math.otf',
                                                                                                 '-V', 'geometry:a4paper',
                                                                                                 '-V', 'colorlinks=true',
                                                                                                 '-V', 'linkcolour:blue',
                                                                                                 '-V', 'fontsize=12pt',
                                                                                                 '--toc', '--toc-depth= 3',
                                                                                                 '--include-before-body', 'cover.tex'
                                                                                                ])
    assert output == ""
    print(f"Conversion process successful: {pdf_filename}")

def delete_files(file_path_arr):

    for file_path in file_path_arr:
        try:
            if os.path.isfile(file_path):
                print(f"Deleting: {file_path}")
                os.remove(file_path)
                print(f"Deleted Successfully")
        except:
            print(f"Unable to delete {file_path}")

def delete_folder(folder_path):

    try:
        if os.path.isdir(folder_path):
            print(f"Deleting folder: {folder_path}")
            shutil.rmtree(folder_path)
            print("Deleted Successfully")
    except:
        print(f"Unable to delete folder: {folder_path}")

def load_yaml(file_path):

    try:
        with open(file_path) as stream:
            data = yaml.safe_load(stream)
            pprint(data)
            return data
    except yaml.YAMLError as exc:
        print(exc)

def decrease_level(metric_path):

    print(f"Decreasing heading levels by 2 in metric: {metric_path}")
    cmd = 'sed -i "s/^\#/###/g" ' + metric_path
    os.system(cmd)

if __name__ == "__main__":

    included_wgs = []
    yml_filename = "working-groups-config.yml"
    master_file_path = "master.tex"
    test_dir = "test_env"
    current_dir = "./"
    delete_folder(test_dir)
    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)
        os.chdir(test_dir)
    else:
        os.chdir(test_dir)

    copy_dir_files("../active_user_input", current_dir)
    copy_dir_files("../passive_user_input", current_dir)

    yaml_data = load_yaml(yml_filename)
    if "focus-areas" in yaml_data:
        del yaml_data["focus-areas"]

    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg']:

            # clone repo with specified branch in yaml data
            ## TODO: Create new function for cloning repo
            subprocess.check_call(['git', 'clone', '-b', yaml_data[wg_name]['github-branch'], yaml_data[wg_name]['github-link'], wg_name])

            included_wgs.append(wg_name)
            included_focus_areas = []
            for focus_area, metrics in yaml_data[wg_name]["focus-areas"].items():
                converted_tex_files = []
                if metrics is not None:
                    for metric in metrics:
                        metric_path = os.path.join(wg_name, "focus-areas", focus_area, metric)
                        '''
                        While copying the file
                        if we specify metric path then file doesn't get replaced
                        specifying only the dir replaces the file automatically
                        needs more investigation
                        '''
                        # copy_file(metric_path, os.path.join(current_dir,metric))
                        copy_file(metric_path, current_dir)

                        decrease_level(metric)
                        tex_filename = re.sub(".md", ".tex",metric)
                        tex_file_path = os.path.join(current_dir, tex_filename)
                        convert_md2tex(metric, tex_file_path)
                        converted_tex_files.append(tex_filename)
                    included_focus_areas.append(focus_area)
                    print(converted_tex_files)
                    focus_area_tex_file_path = os.path.join(current_dir, focus_area+".tex")

                    # copy images of particular focus-area
                    if not os.path.isdir("images"):
                        os.makedirs("images")
                    copy_dir_files(os.path.join(wg_name, "focus-areas", focus_area, "images"), os.path.join(current_dir, "images"))

                    focus_area_README = os.path.join(wg_name, "focus-areas", focus_area, "README.md")
                    # create focus_area.tex file and add table
                    helper.generate_focus_areas(focus_area, focus_area_README, metrics)

                    # Add inclusion commands for metrics
                    with open(focus_area_tex_file_path, "a") as fa_tex_file:
                        fa_tex_file.write("\n")
                        for metric_tex_file in converted_tex_files:
                            metric_file_inclusion = re.sub(".tex", "", metric_tex_file)
                            fa_tex_file.write(f"\input{{{metric_file_inclusion}}} \n")

            # create WG.tex file
            wg_tex_file_path=os.path.join(current_dir, wg_name+".tex")
            with open(wg_tex_file_path, "w") as wg_tex_file:
                wg_tex_file.write("\n")
                wg_tex_file.write(f"\section{{{yaml_data[wg_name]['wg-fullname']}}}\n\clearpage\n")
                ## TODO: Add content for WG.tex file here
                for fa in included_focus_areas:
                    wg_tex_file.write(f"\input{{{fa}}} \n")

    # create master file to include WG.tex files
    with open(master_file_path, "a") as master_file:
        master_file.write("\n")
        for wg in included_wgs:
            master_file.write(f"\include{{{wg}}} \n")
        master_file.write("\n\end{document}")
    convert_tex2pdf(master_file_path, "Output.pdf")
    copy_file("Output.pdf", "../")
