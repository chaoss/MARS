import os
import shutil
import main
import helper
import sys

def check_is_yml_file(language, yml_filename):

    print("Check: Searching for YML file")
    if os.path.isfile(yml_filename):
        print(f"Found YML file successfully: {yml_filename}\n")
        return True
    else:
        print(helper.Color.RED,f"Error: Unable to detect YML file for {language}.")
        print(f"Specify/check if the filename is: {yml_filename}",helper.Color.END)
        return False
        sys.exit(1)

def check_is_cover_file(language, cover_filename):

    print("Check: Searching for cover page file")
    if os.path.isfile(cover_filename):
        print(f"Found cover page file successfully: {cover_filename}\n")
    else:
        print(helper.Color.RED,f"Error: Unable to detect cover page file for {language}.")
        print(f"Specify/check if the filename is: {cover_filename}",helper.Color.END)
        sys.exit(1)

def release_main(language):

    included_wgs = []
    focus_area_count = 0
    metric_count = 0
    wg_config_yml_filename = language + "_working-groups-config.yml"
    cover_filename = language + "_cover.tex"
    word_translation_yml_filename = "word-translations.yml"
    table_fa_top_filename = "table-focus-areas-top.tex"
    table_metric_top_filename = "table-metrics-top.tex"
    table_end_filename = "table-end.tex"

    print()
    check_is_yml_file(language, wg_config_yml_filename)
    check_is_cover_file(language, cover_filename)
    # check_is_class_exist(language, class_name)
    print(helper.Color.GREEN, "Passed all checks successfully", helper.Color.END)


    # Read the yml file
    print("\nReading the YML files:\n")
    print(f"Reading: {wg_config_yml_filename}\n")
    wg_config_yaml_data = helper.load_yaml(wg_config_yml_filename)
    print(f"\nReading: {word_translation_yml_filename}\n")
    word_translation_yaml_data = helper.load_yaml(word_translation_yml_filename)

    # add front and end matter
    helper.add_front_matter(wg_config_yaml_data)
    helper.add_end_matter(wg_config_yaml_data)

    # delete front and end matter from yml
    helper.delete_dictkey("front-matter", wg_config_yaml_data)
    helper.delete_dictkey("end-matter", wg_config_yaml_data)

    # LOOP #1: For Working Groups
    for wg_name in wg_config_yaml_data.keys():
        if wg_config_yaml_data[wg_name]['include-wg']:

            if helper.is_url(wg_config_yaml_data[wg_name]['repo-link']):
                # clone repo with specified branch in yaml data
                print(f"\nCloning from URL: {wg_config_yaml_data[wg_name]['repo-link']}\nBranch: {wg_config_yaml_data[wg_name]['repo-branch']}\n")
                helper.clone_repo(wg_config_yaml_data[wg_name]['repo-link'], wg_name, wg_config_yaml_data[wg_name]['repo-branch'])

            else:
                print(helper.Color.RED, f"Warning: In {wg_config_yaml_data[wg_name]['wg-fullname']}, {wg_config_yaml_data[wg_name]['repo-link']} is not a valid URL ")
                print("Check the repository details in the YAML file", helper.Color.END)

            included_wgs.append(wg_name)
            included_focus_areas = []
            focus_area_README_list = []

            # LOOP #2: For Focus Areas
            for focus_area, metrics in wg_config_yaml_data[wg_name]["focus-areas"].items():
                converted_tex_files = []
                if metrics is not None:

                    # LOOP #3: For Metrics
                    for metric in metrics:
                        metric_path = os.path.join(wg_config_yaml_data[wg_name]["focus-areas-location"], focus_area, metric)

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
                        os.path.join(wg_config_yaml_data[wg_name]["focus-areas-location"], focus_area, "images"),
                        os.path.join("./", "images"))

                    focus_area_README = os.path.join(wg_config_yaml_data[wg_name]["focus-areas-location"], focus_area, "README.md")

                    # to be used in focus-areas table for WG.tex
                    focus_area_README_list.append([focus_area, focus_area_README])

                    # Read the metric table template and replace keywords requiring translations
                    table_metric_head = helper.read_file(table_metric_top_filename)
                    table_metric_head = helper.replace_metric_table_keywords(table_metric_head, focus_area_README, word_translation_yaml_data, language)

                    # Create focus area latex file to include metric table
                    focus_area_filename = wg_name + "_" + focus_area + ".tex"
                    table_metric_tail = helper.read_file(table_end_filename)
                    helper.generate_metric_table(table_metric_head, table_metric_tail, focus_area_filename, metrics)

                    included_focus_areas.append(focus_area_filename)

                    # Add inclusion commands for metric files
                    with open(focus_area_filename, "a") as fa_tex_file:
                        fa_tex_file.write("\n")
                        for metric_tex_file in converted_tex_files:
                            fa_tex_file.write(f"\input{{{os.path.splitext(metric_tex_file)[0]}}} \n")

                        metric_count += len(converted_tex_files)

            # Read the focus area table template and replace keywords requiring translations
            table_fa_head = helper.read_file(table_fa_top_filename)
            table_fa_head = helper.replace_fa_table_keywords(table_fa_head, wg_config_yaml_data[wg_name]['wg-fullname'], word_translation_yaml_data, language)

            # Create working group latex file to include focus area table
            wg_filename = wg_name + ".tex"
            table_fa_tail = helper.read_file(table_end_filename)
            helper.generate_fa_table(table_fa_head, table_fa_tail, wg_filename, focus_area_README_list)

            # Add inclusion commands for focus area latex file
            with open(wg_filename, "a") as wg_file:
                wg_file.write("\n\clearpage\n")
                for fa in included_focus_areas:
                    wg_file.write(f"\input{{{os.path.splitext(fa)[0]}}} \n")

            focus_area_count += len(included_focus_areas)

    # create master file to include WG.tex files
    with open(main.master_file_path, "a") as master_file:
        master_file.write("\n")

        for wg in included_wgs:
            master_file.write(f"\include{{{wg}}} \n")

        master_file.write("\n\end{document}\n")

    # create final PDF
    # pdf_filename = language_template.convert_tex2pdf(main.master_file_path)
    pdf_filename = helper.convert_tex2pdf(main.master_file_path, word_translation_yaml_data, language, cover_filename)
    helper.copy_file(pdf_filename, "../output")

    helper.print_summary(len(included_wgs), focus_area_count, metric_count)
    helper.print_final_msg(pdf_filename)

