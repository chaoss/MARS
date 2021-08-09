import os
import shutil
import main
import helper
import table_templates
import inspect
import sys
from pydoc import locate

def check_is_yml_file(language, yml_filename):

    print("Check: Searching for YML file")
    if os.path.isfile(yml_filename):
        print(f"Found YML file successfully: {yml_filename}\n")
        return True
    else:
        print(helper.color.RED,f"Error: Unable to detect YML file for {language}.")
        print(f"Specify/check if the filename is: {yml_filename}",helper.color.END)
        return False
        sys.exit(1)

def check_is_cover_file(language, cover_filename):

    print("Check: Searching for cover page file")
    if os.path.isfile(cover_filename):
        print(f"Found cover page file successfully: {cover_filename}\n")
    else:
        print(helper.color.RED,f"Error: Unable to detect cover page file for {language}.")
        print(f"Specify/check if the filename is: {cover_filename}",helper.color.END)
        sys.exit(1)

def check_is_class_exist(language, class_name):

    print("Check: Finding language class in templates")

    if bool(class_name in [class_tuple[0] for class_tuple in inspect.getmembers(table_templates)]):
        print(f"Class found successfully: {class_name}\n")
    else:
        print(helper.color.RED,f"Error: Unable to detect language class - '{class_name}' for language {language}")
        print("Make sure that class for language exists or create one in 'table_templates.py' ",helper.color.END)
        sys.exit(1)


def release_main(language):

    included_wgs = []
    focus_area_count = 0
    metric_count = 0
    yml_filename = language + "_working-groups-config.yml"
    cover_filename = language + "_cover.tex"
    class_name = language.title()

    print()
    check_is_yml_file(language, yml_filename)
    check_is_cover_file(language, cover_filename)
    check_is_class_exist(language, class_name)
    print(helper.color.GREEN, "Passed all checks successfully", helper.color.END)


    # Read the yml file
    print("\nReading the YML file:\n")
    yaml_data = helper.load_yaml(yml_filename)

    # add front and end matter
    helper.add_front_matter(yaml_data)
    helper.add_end_matter(yaml_data)

    # delete front and end matter from yml
    helper.delete_dictkey("front-matter", yaml_data)
    helper.delete_dictkey("end-matter", yaml_data)


    language_class = locate('table_templates.' + class_name)
    language_template = language_class()

    # LOOP #1: For Working Groups
    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg']:

            if helper.is_url(yaml_data[wg_name]['repo-link']):
                # clone repo with specified branch in yaml data
                print(f"\nCloning from URL: {yaml_data[wg_name]['repo-link']}\nBranch: {yaml_data[wg_name]['repo-branch']}\n")
                helper.clone_repo(yaml_data[wg_name]['repo-link'], wg_name, yaml_data[wg_name]['repo-branch'])

            else:
                print(helper.color.RED, f"Warning: In {yaml_data[wg_name]['wg-fullname']}, {yaml_data[wg_name]['repo-link']} is not a valid URL ")
                print("Check the repository details in the YAML file", helper.color.END)

            included_wgs.append(wg_name)
            included_focus_areas = []
            focus_area_README_list = []

            # LOOP #2: For Focus Areas
            for focus_area, metrics in yaml_data[wg_name]["focus-areas"].items():
                converted_tex_files = []
                if metrics is not None:

                    # LOOP #3: For Metrics
                    for metric in metrics:
                        metric_path = os.path.join(yaml_data[wg_name]["focus-areas-location"], focus_area, metric)

                        shutil.copy2(metric_path, "./")
                        # helper.copy_file(metric_path, "./")
                        helper.decrease_level(metric)
                        tex_filename = os.path.splitext((metric))[0] + ".tex"

                        helper.convert_md2tex(metric, tex_filename)
                        converted_tex_files.append(tex_filename)

                    # copy images of particular focus-area
                    if not os.path.isdir("images"):
                        print(f"\nMaking images directory")
                        os.makedirs("images")
                    helper.copy_dir_files(
                        os.path.join(yaml_data[wg_name]["focus-areas-location"], focus_area, "images"),
                        os.path.join("./", "images"))

                    focus_area_README = os.path.join(yaml_data[wg_name]["focus-areas-location"], focus_area, "README.md")

                    # to be used in focus-areas table for WG.tex
                    focus_area_README_list.append([focus_area, focus_area_README])

                    # create focus_area.tex file and add table
                    focus_area_filename = wg_name + "_" + focus_area + ".tex"
                    helper.generate_focus_areas(focus_area_filename, focus_area_README, metrics,
                                                language_template)
                    included_focus_areas.append(focus_area_filename)

                    # Add inclusion commands for metrics
                    with open(focus_area_filename, "a") as fa_tex_file:
                        fa_tex_file.write("\n")
                        for metric_tex_file in converted_tex_files:
                            fa_tex_file.write(f"\input{{{os.path.splitext(metric_tex_file)[0]}}} \n")

                        metric_count += len(converted_tex_files)

            # create WG.tex file
            wg_tex_file_path = os.path.join("./", wg_name + ".tex")

            with open(wg_tex_file_path, "w") as wg_tex_file:
                wg_tex_file.write("\n")

                # add focus areas table to WG.tex
                helper.focus_areas_table(wg_tex_file, yaml_data[wg_name]['wg-fullname'], focus_area_README_list,
                                         language_template)
                wg_tex_file.write("\n\clearpage\n")

                for fa in included_focus_areas:
                    wg_tex_file.write(f"\input{{{os.path.splitext(fa)[0]}}} \n")

                focus_area_count += len(included_focus_areas)

    # create master file to include WG.tex files
    with open(main.master_file_path, "a") as master_file:
        master_file.write("\n")

        for wg in included_wgs:
            master_file.write(f"\include{{{wg}}} \n")

        master_file.write("\n\end{document}\n")

    # create final PDF
    pdf_filename = language_template.convert_tex2pdf(main.master_file_path)
    helper.copy_file(pdf_filename, "../output")

    helper.print_summary(len(included_wgs), focus_area_count, metric_count)
    helper.print_final_msg(pdf_filename)

