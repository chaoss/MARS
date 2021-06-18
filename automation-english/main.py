import pathlib
import os
import shutil
import pypandoc
import re
import yaml, subprocess
from pprint import pprint

def check_subarray(subarr, arr):
    for element in subarr:
        if element not in arr:
            return False
    return True

def copy_file(source_filepath, dest_path):
    if os.path.isfile(dest_path):
        print(f"File with same name already exists at destination: {source_filepath}")
    else:
        print(f"Copying: {source_filepath}")
        shutil.copy2(source_filepath, dest_path)
        print(f"Copied Successfully")

def convert_md2tex(md_filename, latex_filename):
    print(f"Converting {md_filename} file to LaTeX")
    # using 'gfm' results in page overflow of tables hence 'markdown_github'  used
    output = pypandoc.convert_file(md_filename, 'latex', outputfile=latex_filename, extra_args=['-f', 'gfm'])

    assert output == ""
    print(f"Created successfully: {latex_filename}")

def convert_tex2pdf(tex_filename, pdf_filename):
    print(f"Converting {tex_filename} file to PDF")

    output = pypandoc.convert_file(tex_filename, 'pdf', outputfile=pdf_filename, extra_args=['-f', 'latex',
                                                                                            '--pdf-engine=xelatex',
                                                                                             '-H', 'header.tex',
                                                                                             '--highlight-style', 'zenburn',
                                                                                             '-V', 'geometry:margin=0.8in',
                                                                                             '-V', 'monofont:DejaVuSansMono.ttf',
                                                                                             '-V', 'mathfont:texgyredejavu-math.otf',
                                                                                             '-V', 'geometry:a4paper',
                                                                                             '-V', 'colorlinks=true',
                                                                                             '-V', 'linkcolour:blue',
                                                                                             '-V', 'fontsize=12pt',
                                                                                             '--toc', '--toc-depth= 1',
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
            shutil.rmtree("images")
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


def copy_images(yaml_data):
    # try using os.walk() to reduce time complexity
    del yaml_data['focus-areas']

    common_img_dir=os.path.join("test-env", "images")

    if not os.path.isdir(common_img_dir):
        os.makedirs(common_img_dir)

    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg-flag']:
            for focus_area in yaml_data[wg_name]["focus-areas"].keys():
                fa_image_dir = os.path.join(wg_name, "focus-areas", focus_area, "images")
                if os.path.isdir(fa_image_dir):
                    for image in os.listdir(fa_image_dir):
                        src_image_path=os.path.join(fa_image_dir, image)
                        des_image_path=os.path.join(common_img_dir, image)
                        # print(image_path)
                        copy_file(src_image_path, des_image_path)

def copy_metrics(yaml_data):
    # try using os.walk() to reduce time complexity
    del yaml_data["focus-areas"]
    test_dir = "test-env"
    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)

    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg-flag']:
            for focus_area in yaml_data[wg_name]["focus-areas"].keys():
                if yaml_data[wg_name]["focus-areas"][focus_area] is not None:
                    for metric in yaml_data[wg_name]["focus-areas"][focus_area]:
                        metric_path = os.path.join(wg_name, "focus-areas", focus_area, metric)
                        copy_file(metric_path, test_dir)


if __name__=="__main__":
    '''
    script_dir_path = pathlib.Path(__file__).parent.absolute()
    common_images_folder_path = os.path.join(script_dir_path, "images")
    repo_name = "wg-common"
    blacklisted_files_list = ["README.md"]
    root = os.path.join(script_dir_path, repo_name, "focus-areas")
    final_report_pdf = "test-release.pdf"
    converted_tex_files = []

    # code to copy all the images from each focus-area to a common images folder
    if not os.path.isdir("images"):
        os.mkdir("images")

    for folder, sub_folders, files in os.walk(root):
        for file in files:
            if folder.endswith("images"):
                source_filepath = os.path.join(script_dir_path, folder, file)
                dest_path = os.path.join(script_dir_path, "images", file)
                copy_file(source_filepath,dest_path)

    # copy required metric files and convert them to latex
    for folder, sub_folders, files in os.walk(root):

        # check for images folder or if all elements of files are blacklisted
        if folder.endswith("images") or check_subarray(files, blacklisted_files_list):
            continue
        copied_metric_md_list = []
        for file in files:
            if file not in blacklisted_files_list:
                source_filepath = os.path.join(script_dir_path, folder, file)
                dest_path = os.path.join(script_dir_path, file)
                copy_file(source_filepath, dest_path)
                copied_metric_md_list.append(file)
                print(os.path.relpath(folder))
                print(os.path.split(folder)[1])
                tex_filename = re.sub(".md",".tex",file)
                convert_md2tex(file,tex_filename)
                converted_tex_files.append(tex_filename)

        # once converted to latex, individual metric files are no longer required
        delete_files(copied_metric_md_list)

    # create required report
    repo_tex_filename = repo_name+".tex"
    convert_tex2pdf(repo_tex_filename,final_report_pdf)

    # code to remove inessential files
    delete_files(converted_tex_files)
    delete_folder("images")
    '''
    included_wgs = []
    load_yaml("repo-structure.yml")
    # copy_images(load_yaml("repo-structure.yml"))
    # copy_metrics(load_yaml("repo-structure.yml"))
    test_dir = "test-env"
    shutil.rmtree(test_dir)
    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)
    copy_file("master.tex", "test-env/master.tex")
    copy_file("header.tex", "test-env/header.tex")
    copy_file("cover.tex", "test-env/cover.tex")
    copy_images(load_yaml("repo-structure.yml"))
    copy_file("Chaoss_logo.png", "test-env/images/Chaoss_logo.png")
    yaml_data = load_yaml("repo-structure.yml")
    del yaml_data["focus-areas"]

    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)
    master_file_path = os.path.join(test_dir, "master.tex")

    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg-flag']:
            included_wgs.append(wg_name)
            focus_areas=[]
            for focus_area in yaml_data[wg_name]["focus-areas"].keys():
                converted_tex_files=[]
                if yaml_data[wg_name]["focus-areas"][focus_area] is not None:
                    for metric in yaml_data[wg_name]["focus-areas"][focus_area]:
                        metric_path = os.path.join(wg_name, "focus-areas", focus_area, metric)
                        # copy_file(metric_path, test_dir)

                        tex_filename = re.sub(".md", ".tex",metric)
                        tex_file_path=os.path.join(test_dir,tex_filename)
                        convert_md2tex(metric_path, tex_file_path)
                        # print(os.path.join(test_dir,tex_filename))
                        converted_tex_files.append(tex_filename)
                    focus_areas.append(focus_area)
                    # print(converted_tex_files)
                    # script to automatically create the focus area table with focus area name from yml file
                    focus_area_tex_file_path= os.path.join(test_dir, focus_area+".tex")
                    # print(focus_area_tex_file_path)
                    with open(focus_area_tex_file_path, "a") as fa_tex_file:
                        fa_tex_file.write("\n")
                        for metric_tex_file in converted_tex_files:
                            metric_file_inclusion = re.sub(".tex", "", metric_tex_file)
                            fa_tex_file.write(f"\input{{{metric_file_inclusion}}} \n")
            # print(focus_areas)
            wg_tex_file_path=os.path.join(test_dir, wg_name+".tex")
            with open(wg_tex_file_path, "a") as wg_tex_file:
                wg_tex_file.write("\n")
                for fa in focus_areas:
                    wg_tex_file.write(f"\input{{{fa}}} \n")

    with open(master_file_path, "a") as master_file:
        master_file.write("\n")
        for wg in included_wgs:
            master_file.write(f"\include{{{wg}}} \n")
        master_file.write("\n\end{document}")
    os.chdir("test-env/")
    convert_tex2pdf("master.tex", "Output.pdf")
    copy_file("Output.pdf", "../Output.pdf")

