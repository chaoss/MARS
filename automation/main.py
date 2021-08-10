import os
import helper
import metrics_release

##### Global Vars #####

translations = {"repo-link": "https://github.com/chaoss/translations", "repo-branch": "main", "repo-name": "translations" }
master_file_path = "master.tex"
test_dir = "test_env"
output_dir = "output"



def language_input():

    print(helper.color.YELLOW)
    print("="*60,helper.color.CYAN)
    print('''\nPlease select your language preference for M.A.R.S. :

    PRESS 1 for English
    PRESS 2 for other languages''')

    print(helper.color.YELLOW)
    choice = input("Your preference (1/2): ")

    # sanity check
    while choice != '1' and choice != '2':
        print(helper.color.RED,"Invalid choice! Please select again...")
        print(helper.color.YELLOW)
        choice = input("Your preference (1/2): ")

    return choice


def main():

    global master_file_path
    global test_dir

    # select language
    language = language_input()
    print(helper.color.END)
    
    # Clean the test_dir for residual files
    helper.clean_directory(test_dir)

    # Make test_env dir if not already, and switch to it
    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)
        os.chdir(test_dir)
    else:
        os.chdir(test_dir)

    # Make output directory if not already
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    print(f"\nSwitching to {test_dir}")


    # Copy the scripts
    helper.copy_dir_files("../active_user_input", "./")
    helper.copy_dir_files("../passive_user_input", "./")

    if language == '1':
        print(helper.color.GREEN)
        print("English selected!")
        print("Moving on to the next phase...")
        print(helper.color.END)

        # main over - switch to new script
        # english_release.english_main(english_yml_filename)
        metrics_release.release_main("english")

    else:
        print(helper.color.GREEN)
        print("Translations selected!")
        print(helper.color.END)

        # clone translation repo and auto-detect langauge
        helper.clone_repo(translations["repo-link"], translations["repo-name"],translations["repo-branch"])
        detected_languages = [dir for dir in sorted(os.listdir(translations["repo-name"])) if os.path.isdir(os.path.join(translations["repo-name"], dir)) and dir[0] != "."]
        print(helper.color.YELLOW)
        print("="*60)
        print(helper.color.CYAN)
        print("The following langauges have been autodetected:\n")

        for i in range(len(detected_languages)):
            print(f"PRESS {i+1} for {detected_languages[i]}")

        print(helper.color.YELLOW)
        user_inp = int(input("Your preference: ")) - 1

        # sanity check
        while user_inp < 0 or user_inp >= len(detected_languages):
            print(helper.color.RED,"Invalid choice! Please select again...")
            print(helper.color.YELLOW)
            user_inp = int(input("Your preference: ")) - 1

        helper.color.END

        # main over - call translation scripts
        # translations_release.translations_main(detected_languages[user_inp])
        metrics_release.release_main(detected_languages[user_inp])

if __name__ == "__main__":
    main()
