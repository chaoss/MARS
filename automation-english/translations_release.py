import os
import pprint
import shutil
import main
import helper
import table_templates
import inspect
import sys
from pydoc import locate

def check_1(language, yml_filename):

    print("Check[1/3]: Searching for YML file")
    if os.path.isfile(yml_filename):
        print(f"Found YML file successfully: {yml_filename}\n")
    else:
        print(f"Error: Unable to detect YML file for {language}.")
        print(f"Specify/check if the filename is: {yml_filename}")
        sys.exit(1)

def check_2(language, cover_filename):

    print("Check[2/3]: Searching for cover page file")
    if os.path.isfile(cover_filename):
        print(f"Found cover page file successfully: {cover_filename}\n")
    else:
        print(f"Error: Unable to detect cover page file for {language}.")
        print(f"Specify/check if the filename is: {cover_filename}")
        sys.exit(1)

def check_3(language, class_name):

    print("Check[3/3]: Finding language class in templates")

    if bool(class_name in [class_tuple[0] for class_tuple in inspect.getmembers(table_templates)]):
        print(f"Class found successfully: {class_name}\n")
    else:
        print(f"Error: Unable to detect language class - '{class_name}' for language {language}")
        print("Make sure that class for language exists or create one in 'table_templates.py' ")
        sys.exit(1)


def translations_main(language):

    focus_area_count = 0
    metric_count = 0
    yml_filename = language + "_working-groups-config.yml"
    cover_filename = language + "_cover.tex"
    class_name = language.capitalize()

    print()
    check_1(language, yml_filename)
    check_2(language, cover_filename)
    check_3(language, class_name)
    print("Passed all checks successfully")

    # Read the yml file
    print("\nReading the YML file:\n")
    yaml_data = helper.load_yaml(yml_filename)


    # add front and end matter
    helper.add_front_matter(yaml_data)
    helper.add_end_matter(yaml_data)

    # delete front and end matter from yml
    helper.delete_dictkey("front-matter", yaml_data)
    helper.delete_dictkey("end-matter", yaml_data)

    # create object of language class specified in input
    # from table templates to be used for:
    # 1. focus-areas table generation
    # 2. WG table generation
    # 3. PDF generation

    language_class = locate('table_templates.' + class_name)
    language_template = language_class()
    print(type(language_template))

    # print("Switching to translations repository")
    print(main.translations["repo-name"])

    # LOOP #1: For Working Groups
    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg']:
            
            main.included_wgs.append(wg_name)
            included_focus_areas = []
            focus_area_list = []

            # LOOP #2: For Focus Areas
            for focus_area, metrics in yaml_data[wg_name]["focus-areas"].items():
                converted_tex_files = []
                if metrics is not None:

                    # LOOP #3: For Metrics
                    for metric in metrics:
                        metric_path = os.path.join(main.translations["repo-name"], language, wg_name, "focus-areas", focus_area, metric)

                        shutil.copy2(metric_path, "./")
                        # helper.copy_file(metric_path, main.current_dir)
                        helper.decrease_level(metric)
                        tex_filename = os.path.splitext((metric))[0] + ".tex"

                        helper.convert_md2tex(metric, tex_filename)
                        converted_tex_files.append(tex_filename)

                    # copy images of particular focus-area
                    if not os.path.isdir("images"):
                        print(f"\nMaking images directory")
                        os.makedirs("images")
                    helper.copy_dir_files(os.path.join(main.translations["repo-name"], language, wg_name, "focus-areas", focus_area, "images"),
                                          os.path.join(main.current_dir, "images"))

                    focus_area_README = os.path.join(main.translations["repo-name"], language, wg_name, "focus-areas", focus_area, "README.md")

                    # to be used in focus-areas table for WG.tex
                    focus_area_list.append([focus_area, focus_area_README])

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
            wg_tex_file_path = os.path.join(main.current_dir, wg_name + ".tex")

            with open(wg_tex_file_path, "w") as wg_tex_file:
                wg_tex_file.write("\n")

                # add focus areas table to WG.tex
                helper.focus_areas_table(wg_tex_file, yaml_data[wg_name]['wg-fullname'], focus_area_list,
                                         language_template)
                wg_tex_file.write("\n\clearpage\n")

                for fa in included_focus_areas:
                    wg_tex_file.write(f"\input{{{os.path.splitext(fa)[0]}}} \n")

                focus_area_count += len(included_focus_areas)

    # create master file to include WG.tex files
    with open(main.master_file_path, "a") as master_file:
        master_file.write("\n")

        for wg in main.included_wgs:
            master_file.write(f"\include{{{wg}}} \n")

        master_file.write("\n\end{document}\n")

    # create final PDF
    pdf_filename = language_template.convert_tex2pdf(main.master_file_path)
    helper.copy_file(pdf_filename, "../output")

    helper.print_summary(len(main.included_wgs), focus_area_count, metric_count)
