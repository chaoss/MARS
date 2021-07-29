# This file defines the template for tables of Focus-areas and metrics for each langauge
# It also contains the pandoc function specific to the language
# In case you need to add another language you've to create a new function with it's name
# Currently it supports - English, Spanish and Chinese

import pypandoc
from datetime import datetime

class english:

    template_working_group = r'''
\section{$SECTION_NAME$}
\begin{table}[ht!]
    \centering
    \begin{tabular}{|p{0.35\linewidth} | p{0.6\linewidth}|}
        \hline
        \hfil \textbf{Focus Area}  & \hfil \textbf{Goal} \\
        \hline
    '''

    template_focus_areas = r'''
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

    @staticmethod
    def convert_tex2pdf(tex_filename):

        pdf_filename = "English-Release-" + datetime.today().strftime('%Y-%m-%d') + ".pdf"

        print(f"\nConverting {tex_filename} file to PDF")
        output = pypandoc.convert_file(tex_filename, 'pdf', outputfile=pdf_filename, extra_args=['-f', 'latex',
                                                                                                    '--pdf-engine=xelatex',
                                                                                                    '--include-in-header', 'header_1.tex',
                                                                                                    '--highlight-style', 'zenburn',
                                                                                                    '-V', 'geometry:margin=0.8in',
                                                                                                    '-V', 'monofont:DejaVuSansMono.ttf',
                                                                                                    '-V', 'mathfont:texgyredejavu-math.otf',
                                                                                                    '-V', 'geometry:a4paper',
                                                                                                    '-V', 'colorlinks=true',
                                                                                                    '-V', 'linkcolour:blue',
                                                                                                    '-V', 'fontsize=12pt',
                                                                                                    '--toc', '--toc-depth= 3',
                                                                                                    '--include-before-body', 'english_cover.tex',
                                                                                                    '--include-after-body', 'end-matter.tex']) 

        return pdf_filename


class Spanish:
    pass


class Chinese:

    template_working_group = r'''
    \section{$SECTION_NAME$}
    \begin{table}[ht!]
        \centering
        \begin{tabular}{|p{0.35\linewidth} | p{0.6\linewidth}|}
            \hline
            \hfil \textbf{关注领域}  & \hfil \textbf{目标} \\
            \hline
        '''

    template_focus_areas = r'''
    \subsection{关注领域 - $FOCUS_AREA_NAME$}
    \textbf{目标:} $FOCUS_AREA_GOAL$
    \begin{table}[ht!]
        \centering
        \begin{tabular}{|p{0.35\linewidth} | p{0.6\linewidth}|}
            \hline
            \hfil \textbf{度量指标}  & \hfil \textbf{问题} \\
            \hline
        '''

    template_end = r'''    \end{tabular}
    \end{table}
        '''

    @staticmethod
    def convert_tex2pdf(tex_filename):
        pdf_filename = "Chinese-Release-" + datetime.today().strftime('%Y-%m-%d') + ".pdf"

        print(f"\nConverting {tex_filename} file to PDF")
        output = pypandoc.convert_file(tex_filename, 'pdf', outputfile=pdf_filename, extra_args=['-f', 'latex',
                                                                                                 '--pdf-engine=xelatex',
                                                                                                 '--include-in-header', 'header_1.tex',
                                                                                                 '--highlight-style', 'zenburn',
                                                                                                 '-V', 'geometry:margin=0.8in',
                                                                                                 '-V', 'monofont:DejaVuSansMono.ttf',
                                                                                                 '-V', 'mathfont:texgyredejavu-math.otf',
                                                                                                 '-V', 'geometry:a4paper',
                                                                                                 '-V', 'colorlinks=true',
                                                                                                 '-V', 'linkcolour:blue',
                                                                                                 '-V', 'fontsize=12pt',
                                                                                                 '-V', 'toc-title:内容',
                                                                                                 '--toc', '--toc-depth= 3',
                                                                                                 '--include-before-body', 'chinese_cover.tex',
                                                                                                 '--include-after-body', 'end-matter.tex'])

        return pdf_filename


