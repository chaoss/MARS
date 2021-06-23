import os, subprocess
import helper
from sys import argv, exit
import yaml
from pprint import pprint
from shutil import copyfile

paths = []

def help_message():
    print("\nUsage: python3 main.py active_user_input/WG_conf.yml")
    print("Make sure WG_conf.yml is configured properly")
    exit(1)

def main():

    global paths

    # read the YML file
    try:
        with open(argv[1]) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except:
        help_message()

    print("\nLoading the YML file...")
    print("YML file structure: \n")
    pprint(data)

    # change_env()
    os.chdir("test_env")

    for wg_name, values in data.items():

        if values['include-wg-flag']:

            print(f'\nwg_name = {wg_name}')
            print(f'\nvalues = {values}')

            for focus_area_name, metrics in values['focus-areas'].items():

                print(f'\nfocus_area = {focus_area_name}')

                focus_area_README = wg_name + '/focus-areas/' + focus_area_name + '/README.md'
                print("\nRelative path to the focus-area README (extract goal from here) = ",focus_area_README)
                print(f'\nmetrics = {metrics}')

                if metrics == None:
                    print(f"No metrics found, skipping {focus_area_name}")
                else:
                    helper.generate_focus_areas(focus_area_name, focus_area_README, metrics)

        else:
            print('\n[WARNING]: Flag off for {}, ignoring this WG'.format(wg_name))


if __name__ == '__main__':
    main()
