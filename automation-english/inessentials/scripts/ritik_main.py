import yaml, os, subprocess
from sys import argv, exit
from pprint import pprint
import helper

def generate_PDF(paths):

    print("\nGenerating the PDF now...\n")
    
    cmd = ('pandoc -f gfm'
            ' -H template.tex'
            ' -o output.pdf'
            ' --pdf-engine xelatex'
            ' -V mainfont="DejaVu Serif"'
            ' -V monofont="DejaVu Sans Mono"'
            ' -V linkcolor:blue'
            ' -V fontsize=12pt'
            ' --include-before-body cover.tex'
            ' --highlight-style pygments.theme'
            ' --toc'
            ' --toc-depth 3'
            ' -V toc-title="Table of Contents" -s ') + ' '.join(paths)

    os.system(cmd)
    os.system('cp output.pdf ../../output')

    print("Generated the PDF!\n")


def generate_paths(values, paths):

    print("\nGenerating relative paths to the metric markdowns...\n")

    for focus, metrics in values['focus-areas'].items():
        
        cmd = 'cp ' + values['wg-name'] + '/focus-areas/' + focus + '/images/* images'
        os.system(cmd)

        # append focus-areas markdown to path
        if metrics is not None:
            paths.append(focus+'.md')

            # append metrics markdown to path
            for metric in metrics:
                paths.append(values['wg-name'] + '/focus-areas/' + focus + '/' + metric)
        
    pprint(paths)
    return paths


def main():

    helper.greetings()

    try:
        with open(argv[1]) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except:
        print("Usage: python3 main.py repo-structure.yml")
        exit(1)

    print("Loading the YML file...")
    print("YML file structure: \n")
    pprint(data)

    print("\nMoving to test-env-prev dir...")
    print("Removing files and folders [if any]...")
    print("Bringing side scripts...")

    os.chdir('test-env-prev')
    os.system('rm -rf *')
    os.mkdir('images')
    os.system('cp ../side-scripts/* .')

    paths = []

    # Download and generate focus-areas markdowns from bash script
    for key, values in data['focus-areas'].items():
        # os.system("ls -l")
        # print(key, values)

        subprocess.check_call(['./get_focus_areas.sh', key, values])
        # cmd = './get_focus_areas.sh ' + key + ' ' + values
        # os.system(cmd)

    del data['focus-areas']

    for key, values in data.items():

        if values['include-wg-flag']:

            print("\nCloning '{}' from '{}' branch\n".format(key, values['github-branch']))
            subprocess.check_call(['git', 'clone', '-b', values['github-branch'], values['github-link'], key])

            # generate markdown for WG names
            paths = helper.generate_WG_md(values['wg-name'], 1, paths)

            paths = generate_paths(values, paths)

        else:
            print('[WARNING]: Flag off for {}, ignoring this WG'.format(key))

    helper.decrease_level(paths)
    generate_PDF(paths)

if __name__ == '__main__':
    main()