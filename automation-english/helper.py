from string import punctuation

template_start = r'''
\subsection{Focus Area - $FOCUS_AREA_NAME$}
\textbf{Goal:} $FOCUS_AREA_GOAL$
\begin{table}[ht!]
    \centering
    \begin{tabular}{|p{0.35\linewidth} | p{0.6\linewidth}|}
        \hline
        \hfil \textbf{Metric}  & \hfil \textbf{Question} \\
        \hline
'''

template_end = r'''    \end{tabular}
\end{table}
'''

def extract_goal(focus_area_README):

    with open(focus_area_README) as f:
        data = f.readlines()
    data = [x.strip() for x in data]

    # filter out empty strings
    data = list(filter(None, data))

    # data[1] = '**Goal:** The goal to be extracted...'
    # 1) Split into list
    # 2) Remove the first word
    # 3) Join the list and return
    return ' '.join(data[1].split()[1:])


def extract_question(metric):

    with open(metric) as f:
        data = f.readlines()
    data = [x.strip() for x in data]

    # filter out empty strings
    data = list(filter(None, data))

    # data[0] = '# Technical Fork'
    metric_name = ' '.join(data[0].split()[1:])

    # data[1] = 'Question: question part of the metric'
    metric_question = ' '.join(data[1].split()[1:])

    return metric_name, metric_question


def generate_focus_areas(focus_area_name, focus_area_filename, focus_area_README, metrics):

    table_head = template_start
    table_tail = template_end

    focus_area_goal = extract_goal(focus_area_README)

    table_head = table_head.replace("$FOCUS_AREA_NAME$", focus_area_name.title().replace('-', ' '))
    table_head = table_head.replace("$FOCUS_AREA_GOAL$", focus_area_goal)

    for metric in metrics:
        metric_name, metric_question = extract_question(metric)
        table_head += '\t\t' + metric_name + ' & ' + metric_question + ' \\\\ \n\t\t\hline\n'

    table_head += table_tail

    ## TODO: add the name of metrics files
    # \input{techical-fork} 
    # .... metrics...

    # file_name = focus_area_name + '.tex'
    with open(focus_area_filename, 'w') as f:
        f.write(table_head)

    print(f"Written data to file = {focus_area_filename}")


