% ibetest.cls -- layout for the Thermo-S1 Part 1 practice tests.
% Mirrors the layout of the IBE3 "Test 1 -- Elec-S1" paper: title block,
% squared answer frames, tick boxes and a "Marking" column in the margin.
%
% One source builds two documents:
%   pdflatex progress-1A.tex                                   -> blank paper
%   pdflatex -jobname=progress-1A-key "\def\KEY{}\input{progress-1A}" -> answer key
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ibetest}[2026/09/27 Thermo-S1 practice tests]
\LoadClass[11pt,a4paper]{article}

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{lmodern}
\RequirePackage[scaled=0.92]{helvet}
\RequirePackage{amsmath,amssymb}
\RequirePackage[a4paper,left=22mm,right=20mm,top=16mm,bottom=20mm,footskip=10mm]{geometry}
\RequirePackage[dvipsnames]{xcolor}
\RequirePackage{tikz}
\usetikzlibrary{calc,arrows.meta,positioning,decorations.pathreplacing}
\RequirePackage[european,americanvoltages]{circuitikz}
\RequirePackage{siunitx}
\RequirePackage[most]{tcolorbox}
\RequirePackage{enumitem}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{etoolbox}
\RequirePackage{array}
\RequirePackage{needspace}
\RequirePackage{microtype}

% ---------------------------------------------------------------- mode --
\newif\ifkey \keyfalse
\ifdefined\KEY \keytrue \fi

% -------------------------------------------------------------- colours --
\definecolor{keyblue}{RGB}{18,62,168}
\definecolor{tipred}{RGB}{186,32,48}
\definecolor{gridgray}{gray}{0.84}
\definecolor{framegray}{gray}{0.42}
\definecolor{markdark}{gray}{0.22}

% ------------------------------------------------------------- settings --
\sisetup{exponent-product=\times, output-decimal-marker={.}, group-digits=integer,
         group-minimum-digits=5, per-mode=power}
\ctikzset{bipoles/length=0.95cm, bipoles/lamp/height=0.42, bipoles/lamp/width=0.42, nodes width=0.055}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\frenchspacing
\setlist{nosep, leftmargin=*}

\newlength{\framewidth}   \setlength{\framewidth}{0.835\textwidth}
\newlength{\markcolwidth} \setlength{\markcolwidth}{0.14\textwidth}

% ------------------------------------------------------ page decoration --
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[C]{\small\thepage\,/\,\pageref{LastPage}}
\AddToHook{shipout/background}{%
  \put(\dimexpr\paperwidth-9mm\relax,-\dimexpr\paperheight-22mm\relax){%
    \rotatebox{90}{\sffamily\fontsize{6.5}{7}\selectfont\color{black!45}%
      Unofficial practice material written from the Thermo-S1 Part~1 lecture notes
      \,$\cdot$\, not an official examination paper}}}

% ------------------------------------------------------------ title block --
\newcommand{\testheader}{%
  \noindent
  \begin{minipage}[b]{0.62\textwidth}
    {\sffamily\bfseries\LARGE IBE\textsuperscript{3}}\\[2pt]
    {\sffamily\bfseries\Large Physics for Engineers}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.36\textwidth}\raggedleft
    {\sffamily\small\color{black!70} Practice test\\ Module: Thermodynamics \,$\cdot$\, Part 1}
  \end{minipage}\par
  \vspace{3pt}\noindent\rule{\textwidth}{0.9pt}\par}

% \maketest{title}{sections line}{duration}{total marks}
\newcommand{\totalmarks}{}
\newcommand{\maketest}[4]{%
  \renewcommand{\totalmarks}{#4}%
  \testheader
  \vspace{7mm}
  \begin{center}
    {\LARGE\bfseries #1}\\[5pt]
    {\large #2}\\[5pt]
    {\normalsize Semester 1 \,$\cdot$\, Academic Year 2026--2027}
  \end{center}
  \vspace{3mm}
  \ifkey
    \begin{center}
      \colorbox{tipred}{\strut\hspace{4mm}\sffamily\bfseries\color{white}%
        ANSWER KEY \,$\cdot$\, MODEL ANSWERS AND MARKING SCHEME\hspace{4mm}}
    \end{center}
  \else
    {\sffamily\color{black!55}Family name:}\ \makebox[58mm]{\color{black!40}\dotfill}\hfill
    {\sffamily\color{black!55}Given name:}\ \makebox[58mm]{\color{black!40}\dotfill}\par
  \fi
  \vspace{4mm}
  \begin{center}
    \begin{minipage}{0.88\textwidth}\centering
      Duration: #3. \emph{No documents. Calculator not allowed.} Answer inside the
      printed frames only; the margin boxes are for the marker.
      \textbf{Total: #4 marks.}
    \end{minipage}
  \end{center}
  \vspace{1mm}}

% -------------------------------------------------------------- exercises --
\newcounter{exo}
% \exercise[sections]{title}{marks}   (optional: lecture sections covered)
\NewDocumentCommand{\exercise}{o m m}{%
  \par\addvspace{4.5mm}\needspace{12\baselineskip}%
  \refstepcounter{exo}%
  \noindent{\sffamily\bfseries Exercise \theexo.\ \ #2}%
  \IfValueT{#1}{\ \ {\sffamily\scriptsize\color{black!55}[#1]}}\hfill(#3)\par\nobreak
  \vspace{1pt}\nobreak}

% circled number (for marking items)
\newcommand{\circnum}[1]{\tikz[baseline=(c.base)]\node[circle,draw,inner sep=0.4pt,
  minimum size=1.15em,font=\sffamily\scriptsize](c){#1};}

% one marking item: #1 = item number, #2 = maximum points
\newcommand{\markitem}[2]{%
  \begin{tikzpicture}[x=4.2mm,y=3.5mm,font=\sffamily\scriptsize]
    \pgfmathtruncatemacro{\nb}{#2+1}
    \fill[markdark] (0,0) rectangle (\nb,0.95);
    \node[circle,draw=white,text=white,inner sep=0pt,minimum size=2.8mm,
          font=\sffamily\tiny] at (\nb/2,0.475) {#1};
    \draw[markdark,line width=0.4pt] (0,-1.95) rectangle (\nb,0.95);
    \draw[markdark,line width=0.3pt] (0,-0.95) -- (\nb,-0.95);
    \foreach \j in {0,...,#2} {
      \node[font=\sffamily\scriptsize\bfseries] at (\j+0.5,-0.475) {\j};
      \draw[black!85,line width=0.4pt] (\j+0.16,-1.79) rectangle (\j+0.84,-1.11);
    }
    \foreach \j in {1,...,#2} {\draw[markdark,line width=0.3pt] (\j,0) -- (\j,-0.95);}
  \end{tikzpicture}}

% marking column: #1 = first item number, #2 = comma list of maxima
\newcommand{\markingcolumn}[2]{%
  {\sffamily\small Marking}\par\vspace{-3pt}
  {\color{black!60}\rule{\linewidth}{0.4pt}}\par\vspace{2pt}
  \foreach \m [count=\k from #1] in {#2} {\markitem{\k}{\m}\par\vspace{2pt}}}

% squared answer frame
\tcbset{gridframe/.style={enhanced, sharp corners, colframe=framegray, boxrule=0.5pt,
  left=2.5mm, right=2.5mm, top=2mm, bottom=2mm, before skip=0pt, after skip=0pt,
  interior code={%
    \path[fill=white] (interior.south west) rectangle (interior.north east);
    \begin{scope}
      \clip (interior.south west) rectangle (interior.north east);
      \draw[gridgray,line width=0.3pt,step=5mm,shift={(interior.north west)}]
        (0,0) grid (22cm,-60cm);
    \end{scope}}}}

% \answer[first item]{maxima}{height}{model answer}
% Paper: empty squared frame of the given height + marking boxes.
% Key:   the same frame (at least that tall) with the model answer in blue.
\NewDocumentCommand{\answer}{O{1} m m +m}{%
  \par\vspace{2pt}\noindent
  \begin{minipage}[t]{\framewidth}\vspace{0pt}%
    \ifkey
      \begin{tcolorbox}[gridframe, height from=#3 to 60cm,
                        fontupper=\color{keyblue}\raggedright]#4\end{tcolorbox}%
    \else
      \begin{tcolorbox}[gridframe, height=#3]\end{tcolorbox}%
    \fi
  \end{minipage}\hfill
  \begin{minipage}[t]{\markcolwidth}\vspace{0pt}\centering
    \ifstrempty{#2}{}{\markingcolumn{#1}{#2}}%
  \end{minipage}\par\vspace{2pt}}

% given data, framed on one line
\newcommand{\data}[1]{%
  \par\vspace{2pt}\noindent
  \begin{tcolorbox}[enhanced, sharp corners, colback=white, colframe=framegray,
     boxrule=0.5pt, width=\framewidth, left=2mm, right=2mm, top=1mm, bottom=1mm,
     before skip=2pt, after skip=2pt]%
     \makebox[\linewidth][c]{\begin{tabular}{@{}c@{}}#1\end{tabular}}\end{tcolorbox}}

% ------------------------------------------------------------------- MCQ --
% \tick{1} = correct box (crossed in the key), \tick{0} = distractor
\newcommand{\tick}[1]{%
  \tikz[baseline=-0.62ex]{%
    \draw[black!85,line width=0.5pt] (-1.65mm,-1.65mm) rectangle (1.65mm,1.65mm);
    \ifkey\ifnum#1=1
      \draw[keyblue,line width=1.3pt] (-1.25mm,-1.25mm) -- (1.25mm,1.25mm)
                                      (-1.25mm,1.25mm) -- (1.25mm,-1.25mm);
    \fi\fi}}
\newcommand{\question}[1]{\par\vspace{3pt}\noindent\hspace*{1mm}#1\par\nobreak\vspace{3pt}\nobreak}
% four short options on one line: \opts{c}{text}{c}{text}{c}{text}{c}{text}
\newcommand{\opts}[8]{%
  \par\noindent\hspace*{0.08\textwidth}%
  \makebox[0.215\textwidth][l]{\tick{#1}\ \ #2}%
  \makebox[0.215\textwidth][l]{\tick{#3}\ \ #4}%
  \makebox[0.215\textwidth][l]{\tick{#5}\ \ #6}%
  \makebox[0.215\textwidth][l]{\tick{#7}\ \ #8}\par\vspace{2pt}}
% four medium-length options on a 2 x 2 grid
\newcommand{\opttwo}[8]{%
  \par\noindent
  \begin{tabular}{@{\hspace{0.08\textwidth}}l@{\hspace{2.5mm}}p{0.36\textwidth}%
                  l@{\hspace{2.5mm}}p{0.36\textwidth}@{}}
    \tick{#1} & #2 & \tick{#3} & #4\\[3pt]
    \tick{#5} & #6 & \tick{#7} & #8
  \end{tabular}\par\vspace{2pt}}
% four long options, one per line
\newcommand{\optlist}[8]{%
  \par\noindent
  \begin{tabular}{@{\hspace{8mm}}l@{\hspace{3mm}}p{0.8\textwidth}@{}}
    \tick{#1} & #2\\[2pt] \tick{#3} & #4\\[2pt] \tick{#5} & #6\\[2pt] \tick{#7} & #8
  \end{tabular}\par\vspace{2pt}}
% explanation printed under an MCQ in the key only
\newcommand{\why}[1]{\ifkey\par\noindent\hspace*{8mm}%
  \begin{minipage}{0.86\textwidth}\small\color{keyblue}\emph{Why:} #1\end{minipage}\par\vspace{2pt}\fi}

% ------------------------------------------------------------- key-only --
\NewDocumentEnvironment{scheme}{+b}{%
  \ifkey\par\vspace{1pt}\noindent
  \begin{tcolorbox}[enhanced, colback=black!2, colframe=black!45, boxrule=0.4pt, arc=1mm,
     width=\framewidth, left=2mm, right=2mm, top=1mm, bottom=1mm, before skip=1pt,
     after skip=2pt, fontupper=\small, title={\sffamily\bfseries Marking scheme},
     fonttitle=\small, coltitle=black, colbacktitle=black!10, toptitle=0.5mm, bottomtitle=0.5mm]
  #1
  \end{tcolorbox}\fi}{}
\NewDocumentEnvironment{tip}{+b}{%
  \ifkey\par\noindent
  \begin{tcolorbox}[enhanced, colback=tipred!4, colframe=tipred!75, boxrule=0.5pt, arc=1mm,
     width=\framewidth, left=2mm, right=2mm, top=1mm, bottom=1mm, before skip=1pt,
     after skip=2pt, fontupper=\small, title={\sffamily\bfseries Examiner's tip},
     fonttitle=\small, coltitle=white, colbacktitle=tipred!80, toptitle=0.5mm, bottomtitle=0.5mm]
  #1
  \end{tcolorbox}\fi}{}
% neutral note, printed in the key only
\NewDocumentEnvironment{note}{+b}{%
  \ifkey\par\noindent
  \begin{tcolorbox}[enhanced, colback=black!3, colframe=black!30, boxrule=0.4pt, arc=1mm,
     width=\framewidth, left=2mm, right=2mm, top=1mm, bottom=1mm, before skip=1pt,
     after skip=2pt, fontupper=\small, title={\sffamily\bfseries Note},
     fonttitle=\small, coltitle=black, colbacktitle=black!8, toptitle=0.5mm, bottomtitle=0.5mm]
  #1
  \end{tcolorbox}\fi}{}
% \pt{n}{criterion} inside a scheme: "(1) n pt -- criterion"
\newcommand{\pt}[3]{\par\noindent\circnum{#1}\ \textbf{#2}\ \ #3}

% closing line of each paper / score line of each key
\newcommand{\finish}{%
  \par\vspace{5mm}
  \ifkey
    \noindent\begin{tcolorbox}[enhanced, sharp corners, colback=white, colframe=black!60,
      boxrule=0.5pt, width=\textwidth, halign=center]
      \sffamily Your score: \makebox[14mm]{\dotfill}\,/\,\totalmarks
      \qquad$\longrightarrow$\qquad mark out of 20 $=$ score $\times\,20/\totalmarks$
      $=$ \makebox[14mm]{\dotfill}\,/\,20
    \end{tcolorbox}
  \else
    \begin{center}\sffamily\small\color{black!60}--- End of the test ---\end{center}
  \fi}

% receiver / generator convention sketch (arrows as in Fig. 14 of the notes)
% \convfig{receiver}{R}, \convfig{generator}{e}, or \convfig[R]{generator}{R}
% (optional argument: the bipole to draw instead of the default one)
\NewDocumentCommand{\convfig}{O{} m m}{%
  \begin{circuitikz}[line width=0.5pt, baseline={(0,0.55)}]
    \ifstrequal{#2}{receiver}{\tikzset{cfbip/.style={R}}}%
                             {\tikzset{cfbip/.style={battery1, invert}}}%
    \ifstrempty{#1}{}{\tikzset{cfbip/.style={#1}}}%
    \draw (0,-0.45) -- (0,0) to[cfbip, l=$#3$] (0,1.3) -- (0,1.85);
    \ifstrequal{#2}{receiver}{%
      \draw[-{Latex[length=1.8mm]}] (0,1.85) -- (0,1.5) node[pos=0.2, right=1pt] {$i$};
    }{%
      \draw[-{Latex[length=1.8mm]}] (0,1.45) -- (0,1.85) node[pos=0.75, right=1pt] {$i$};
    }
    \draw[-{Latex[length=1.8mm]}] (0.75,0) -- (0.75,1.3) node[midway, right=1pt] {$u$};
    \node[font=\scriptsize] at (0.3,-0.75) {#2};
  \end{circuitikz}}

% small i = f(u) characteristic: \charplot{label}{curve drawing}
\newcommand{\charplot}[2]{%
  \begin{tikzpicture}[scale=0.62, line width=0.5pt, >={Latex[length=1.6mm]}]
    \draw[->] (-1.7,0) -- (1.9,0) node[right, font=\scriptsize] {$u$};
    \draw[->] (0,-1.5) -- (0,1.7) node[above, font=\scriptsize] {$i$};
    \node[below left, font=\scriptsize, inner sep=1pt] at (0,0) {$O$};
    \begin{scope}[line width=1.2pt, blue!55!black] #2 \end{scope}
    \node[font=\small] at (0.1,-2.05) {(#1)};
  \end{tikzpicture}}

% handy symbols
\newcommand{\Req}{R_{\mathrm{eq}}}
\newcommand{\ETh}{E_{\mathrm{Th}}}
\newcommand{\RTh}{R_{\mathrm{Th}}}
\newcommand{\INo}{I_{\mathrm{No}}}
\newcommand{\RNo}{R_{\mathrm{No}}}
\newcommand{\dd}{\mathrm{d}}
\endinput
