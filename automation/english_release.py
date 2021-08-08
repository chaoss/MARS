import os
import main
import helper
import table_templates

def english_main(english_yml_filename):
    
    focus_area_count = 0
    metric_count = 0

    # Read the yml file
    print("\nReading the YML file:\n")
    yaml_data = helper.load_yaml(english_yml_filename)

    # add front and end matter
    helper.add_front_matter(yaml_data)
    helper.add_end_matter(yaml_data)

    # delete front and end matter from yml
    helper.delete_dictkey("front-matter", yaml_data)
    helper.delete_dictkey("end-matter", yaml_data)

    # create object of english class from table templates
    # to be used for:
    # 1. focus-areas table generation
    # 2. WG table generation
    # 3. PDF generation
    english_template = table_templates.english()

    # LOOP #1: For Working Groups
    for wg_name in yaml_data.keys():
        if yaml_data[wg_name]['include-wg']:

            # clone repo with specified branch in yaml data
            print(f"\nCloning from URL: {yaml_data[wg_name]['repo-link']}\nBranch: {yaml_data[wg_name]['repo-branch']}\n")
            helper.clone_repo(yaml_data[wg_name]['repo-link'], wg_name, yaml_data[wg_name]['repo-branch'])

            main.included_wgs.append(wg_name)
            included_focus_areas = []
            focus_area_list = []

            # LOOP #2: For Focus Areas
            for focus_area, metrics in yaml_data[wg_name]["focus-areas"].items():
                converted_tex_files = []
                if metrics is not None:

                    # LOOP #3: For Metrics
                    for metric in metrics:
                        metric_path = os.path.join(wg_name, "focus-areas", focus_area, metric)

                        helper.copy_file(metric_path, main.current_dir)
                        helper.decrease_level(metric)
                        tex_filename = os.path.splitext((metric))[0] + ".tex"                        
                        
                        helper.convert_md2tex(metric, tex_filename)
                        converted_tex_files.append(tex_filename)

                    # copy images of particular focus-area
                    if not os.path.isdir("images"):
                        print(f"\nMaking images directory")
                        os.makedirs("images")
                    helper.copy_dir_files(os.path.join(wg_name, "focus-areas", focus_area, "images"), os.path.join(main.current_dir, "images"))

                    focus_area_README = os.path.join(wg_name, "focus-areas", focus_area, "README.md")

                    # to be used in focus-areas table for WG.tex
                    focus_area_list.append([focus_area, focus_area_README])

                    # create focus_area.tex file and add table
                    focus_area_filename = wg_name+"_"+focus_area+".tex"
                    helper.generate_focus_areas(focus_area_filename, focus_area_README, metrics, english_template)
                    included_focus_areas.append(focus_area_filename)

                    # Add inclusion commands for metrics
                    with open(focus_area_filename, "a") as fa_tex_file:
                        fa_tex_file.write("\n")
                        for metric_tex_file in converted_tex_files:
                            fa_tex_file.write(f"\input{{{os.path.splitext(metric_tex_file)[0]}}} \n")

                        metric_count += len(converted_tex_files)

            # create WG.tex file
            wg_tex_file_path = os.path.join(main.current_dir, wg_name+".tex")

            with open(wg_tex_file_path, "w") as wg_tex_file:
                wg_tex_file.write("\n")

                # add focus areas table to WG.tex
                helper.focus_areas_table(wg_tex_file, yaml_data[wg_name]['wg-fullname'], focus_area_list, english_template)
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
    pdf_filename = english_template.convert_tex2pdf(main.master_file_path)
    helper.copy_file(pdf_filename, "../output")

    helper.print_summary(len(main.included_wgs), focus_area_count, metric_count)
    helper.print_final_msg(pdf_filename)
