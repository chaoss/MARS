# Add support for a new language to MARS

The MARS project can be extended to provide support for many languages. 

The steps to configure MARS for a new language are given below:

## Step 1: Create YAML and cover file

Please follow the naming convention given below:

| File | Naming Convention |
| --- | --- | 
| YAML file | `<language-dir-name>_working-groups-config.yml` |
| Cover file | `<language-dir-name>_cover.tex`

The MARS project automatically detects the language directories present in the translations repository. 

**Make sure the language directory names are the same as in the translations repository.**

Refer to this [README](./active_user_input/README.md) for more info. 

## Step 2: Add new language class to [`table_templates.py`](table_templates.py)

Create a new language class in the format `<language-dir-name>` in [`table_templates.py`](table_templates.py)

Copy the variables defined in the `English` class and add them to the newly created class.

In the variables `template_working_group` and `template_focus_areas`, replace `Focus Area`, `Goal`, `Metric` and `Question` with appropriate translations. These variables are used to dynamically generate focus area tables.

In the function `convert_tex2pdf`

- Change the PDF filename depending on the language
- Replace `english_cover.tex` with cover filename made in the previous step
- Change table of contents title as given in the `toc-title:` parameter with appropriate translation 
  
## Step 3: Add language package to the header file

**Note:-** By default, MARS provides support for the languages using English, Chinese, Japanese and Korean characters. Follow this step only if the writing characters are different than these languages. Make sure to use the [Python virtual environment method](./README.md#method-2-the-not-so-easy-way---python-virtual-env) to run MARS in this case.

The MARS project uses LaTeX format as the intermediate between markdown and PDF. 

It is necessary to include the correct LaTeX language package to make sure the characters are displayed correctly in the PDF.

Add the required LaTeX package to the [`header_1.tex`](./passive_user_input/header_1.tex) file. Optionally, you can specify a new header file and edit the `convert_tex2pdf` function accordingly.

You are now ready to run MARS in the desired language!


