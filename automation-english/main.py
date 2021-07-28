import os
# import shutil
import sys
import english_release
import helper

##### Global Vars #####

english_yml_filename = "english_working-groups-config.yml"
spanish_yml_filename = "spanish_working-groups-config.yml"
chinese_yml_filename = "chinese_working-groups-config.yml"
master_file_path = "master.tex"
test_dir = "test_env"
current_dir = "./"
included_wgs = []


def language_input():

    print()
    print("="*60)
    print('''\nPlease select your language preference for M.A.R.S. :
    PRESS 1 for English
    PRESS 2 for other languages
    ''')

    choice = input("Your preference (1/2): ")

    while choice != '1' and choice != '2':
        print("Invalid choice! Please select again...\n")
        choice = input("Your preference (1/2): ")

    return choice


def main():

    global included_wgs
    global english_yml_filename
    global master_file_path
    global test_dir
    global current_dir

    # Clean the test_dir for residual files
    helper.clean_directory(test_dir)

    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)
        os.chdir(test_dir)
    else:
        os.chdir(test_dir)
    
    print(f"\nSwitching to {test_dir}")

    # Copy the scripts
    helper.copy_dir_files("../active_user_input", current_dir)
    helper.copy_dir_files("../passive_user_input", current_dir)

    # select language
    language = language_input()

    if language == '1':
        print("English selected!")
        print("Moving on to the next phase...")

        # main over - switch to new script
        english_release.english_main(english_yml_filename)

    else:
        print("Work in progress")
    sys.exit()

if __name__ == "__main__":
    main()
