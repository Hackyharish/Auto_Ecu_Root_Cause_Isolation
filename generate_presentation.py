import subprocess
import os

beamer_code = r"""\documentclass[aspectratio=169,10pt]{beamer}

% -------------------------------------------------------------
% Packages & Configuration
% -------------------------------------------------------------
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usetikzlibrary{calc,positioning,shapes.geometric,arrows.meta,fit}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{tcolorbox}
\usepackage{hyperref}

% Graphicspath
\graphicspath{{../Images/}{../Images/CleanPlots/}{../Images/WSS_SENSOR_OPEN/}{../Images/BRAKE_SWITCH_STUCK/}{../Images/CUTOFF_ABS_NODE/}{../}{./}}

% Remove default navigation symbols & set crisp widescreen margins
\setbeamertemplate{navigation symbols}{}
\setbeamersize{text margin left=0.55cm,text margin right=0.55cm}

% -------------------------------------------------------------
% Color Palette (Vector / Tata Automotive Theme)
% -------------------------------------------------------------
\definecolor{vectorred}{RGB}{166, 0, 44}       % Vector Corporate Crimson
\definecolor{slatedark}{RGB}{33, 37, 41}       % High-contrast charcoal
\definecolor{slategrey}{RGB}{100, 110, 120}    % Subtitle & border grey
\definecolor{cardbg}{RGB}{248, 250, 252}       % Card soft background
\definecolor{cardborder}{RGB}{212, 220, 230}   % Card border
\definecolor{accentblue}{RGB}{24, 90, 157}     % CAN Network Blue
\definecolor{accentgreen}{RGB}{22, 128, 60}    % RCA Success Green
\definecolor{accentpurple}{RGB}{112, 48, 160}  % Diagnostics Purple
\definecolor{accentamber}{RGB}{217, 119, 6}    % Fault Injection Amber

% Node & Message Colors
\definecolor{nodetester}{RGB}{112, 48, 160}     % DIAG_TESTER Diagnostics Purple
\definecolor{nodeabs}{RGB}{80, 86, 92}         % ABS/ESP Charcoal Grey
\definecolor{nodeecm}{RGB}{224, 228, 233}      % ECM Light Slate Grey
\definecolor{nodeecmtext}{RGB}{65, 72, 78}     % ECM Text Dark
\definecolor{nodetcm}{RGB}{166, 0, 44}         % TCM / Gearbox Crimson Red
\definecolor{nodebcm}{RGB}{52, 104, 152}       % BCM Slate Blue
\definecolor{busline}{RGB}{120, 128, 136}      % CAN Bus Line Grey

% Standard card tcolorbox style
\tcbset{
  cardstyle/.style={
    colback=cardbg,
    colframe=cardborder,
    boxrule=0.9pt,
    arc=5pt,
    left=6pt,right=6pt,top=4pt,bottom=4pt,
    boxsep=1pt,
    toptitle=3.5pt,bottomtitle=3.5pt,
    titlerule=0.5pt
  },
  whitecard/.style={
    colback=white,
    colframe=cardborder,
    boxrule=0.9pt,
    arc=5pt,
    left=6pt,right=6pt,top=4pt,bottom=4pt,
    boxsep=1pt,
    toptitle=3.5pt,bottomtitle=3.5pt,
    titlerule=0.5pt
  }
}

% Header & Footline Styling
\setbeamertemplate{headline}{}
\setbeamertemplate{footline}{
  \leavevmode%
  \hbox{%
    \begin{beamercolorbox}[wd=0.45\paperwidth,ht=2.4ex,dp=1.0ex,leftskip=0.55cm]{author in head/foot}%
      \tiny\color{slategrey}\textbf{Automated Root Cause Isolation in Multi-ECU Networks}
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=0.35\paperwidth,ht=2.4ex,dp=1.0ex,center]{title in head/foot}%
      \tiny\color{slategrey}Tata Technologies TechPulse \textbar{} IVN Capstone
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=0.20\paperwidth,ht=2.4ex,dp=1.0ex,rightskip=0.55cm,right]{date in head/foot}%
      \tiny\color{slategrey}\insertframenumber{} / \inserttotalframenumber
    \end{beamercolorbox}%
  }%
  \vskip0pt%
}

% Slide title helper (positive top space so zero top clipping occurs!)
\newcommand{\slidetitle}[2]{%
  \vspace{0.08cm}
  {\Large\bfseries\color{vectorred}#1}\\[2pt]
  {\footnotesize\color{slategrey}#2}
  \vspace{0.10cm}
}

\begin{document}

% =============================================================================
% SLIDE 1: Project Title and Student Details
% =============================================================================
\begin{frame}[t]
\vspace{0.12cm}
\centering

\begin{tcolorbox}[colback=vectorred!10, colframe=vectorred!25, boxrule=0.5pt, arc=4pt, width=10.6cm, left=8pt, right=8pt, top=2.5pt, bottom=2.5pt]
  \centering\scriptsize\bfseries\color{vectorred} IN-VEHICLE NETWORKING (IVN) CAPSTONE PROJECT \quad\textbullet\quad B.TECH SEMESTER 7
\end{tcolorbox}

\vspace{0.18cm}
\resizebox{0.96\textwidth}{!}{\LARGE\bfseries\color{vectorred} Automated Root Cause Isolation in Multi-ECU Networks}\\[6pt]
{\large\bfseries\color{slatedark} Signal Dependency Mapping \& UDS Diagnostics in Vector CANoe 19}\\[5pt]
{\small\color{slategrey} Compliant with ISO 14229-1 (UDS) \textbullet{} ISO 15765-2 (DoCAN) \textbullet{} ISO 26262 ASIL-D \textbullet{} ISO 11898-1}

\vspace{0.24cm}

\begin{tcolorbox}[
  colback=cardbg, colframe=vectorred!70, boxrule=1.0pt, arc=7pt,
  width=11.4cm, left=14pt, right=14pt, top=5pt, bottom=5pt,
  colbacktitle=vectorred, coltitle=white,
  toptitle=3pt, bottomtitle=3pt,
  title={\centering\scriptsize\bfseries STUDENT DETAILS}
]
  \small\color{slatedark}
  \begin{tabular}{@{}ll@{}}
    \textbf{Name:}        & Harish R \\[1.5pt]
    \textbf{Roll Number:} & CB.EN.U4EEE23112 \\[1.5pt]
    \textbf{Degree:}      & Bachelor of Technology (B.Tech) \\[1.5pt]
    \textbf{Department:}  & Department of Electrical \& Electronics Engineering \\[1.5pt]
    \textbf{Institution:} & Amrita School of Engineering, Coimbatore \\[1.5pt]
    \textbf{University:}  & Amrita Vishwa Vidyapeetham
  \end{tabular}
\end{tcolorbox}

\vspace{0.16cm}
{\footnotesize\color{slategrey}\textbf{Industry Collaboration:} Tata Technologies (TechPulse Program) \quad\textbullet\quad \textbf{Platform:} Vector CANoe 19}

\end{frame}

% =============================================================================
% SLIDE 2: Problem Statement and Objectives
% =============================================================================
\begin{frame}[t]
\slidetitle{Problem Statement \& Research Objectives}{Multi-ECU Signal Cascades \textbullet{} False DTC Floods \textbullet{} ISO 26262 ASIL-D Determinism}

\begin{columns}[T,totalwidth=\textwidth]

  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=vectorred!75, colbacktitle=vectorred!8, height=5.32cm,
      title={\normalsize\bfseries\color{vectorred} The Problem: Cascading Alarm Floods}]
      \footnotesize\color{slatedark}\raggedright\vspace{-4pt}
      \begin{itemize}\setlength{\itemsep}{1.5pt}\setlength{\leftmargini}{10pt}
        \item \textbf{Dense Coupling:} Modern vehicles host 70--100 ECUs exchanging thousands of cross-dependent CAN signals.
        \item \textbf{Symptom Alarm Floods:} Single sensor or ECU faults starve healthy downstream nodes, triggering dozens of secondary DTCs.
        \item \textbf{Misdiagnosis \& Cost:} Technicians replace healthy ECUs, inflating warranty costs and extending vehicle downtime.
        \item \textbf{Safety Risk:} Conflicting DTCs confuse fail-safe controllers, risking unwanted torque cuts or phantom braking.
      \end{itemize}
    \end{tcolorbox}
  \end{column}

  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=accentblue!75, colbacktitle=accentblue!8, height=5.32cm,
      title={\normalsize\bfseries\color{accentblue} Project Objectives \& Contributions}]
      \footnotesize\color{slatedark}\raggedright\vspace{-4pt}
      \begin{itemize}\setlength{\itemsep}{1.5pt}\setlength{\leftmargini}{10pt}
        \item \textbf{DAG Signal Modeling:} Formulate in-vehicle signal flows as a Directed Acyclic Graph $G=(V, E)$ capturing causal links.
        \item \textbf{On-Bus Pruning Engine:} Implement in-degree topological filtering in CAPL to isolate root causes in real time.
        \item \textbf{Deterministic Timing:} Achieve disambiguation in $<50$ ms, within the ISO 26262 ASIL-D 100 ms FTTI bound.
        \item \textbf{Vector CANoe 19 Validation:} Validate across 6 failure modes (sensor shorts, ECU dropouts, stuck switches) at 100\% accuracy.
      \end{itemize}
    \end{tcolorbox}
  \end{column}

\end{columns}

\vspace{0.08cm}
\begin{tcolorbox}[colback=slategrey!10, colframe=cardborder, boxrule=0.7pt, arc=4pt, left=6pt, right=6pt, top=3pt, bottom=3pt]
  \centering\scriptsize\color{slatedark}
  \textbf{Target Scope:} 4 ECUs (ECM, ABS, TCM, BCM) \textbullet{} 15 CAN Messages \textbullet{} 43 Powertrain \& Chassis Signals \textbullet{} 500 kbps CAN
\end{tcolorbox}

\end{frame}

% =============================================================================
% SLIDE 3: CAN Network Message and Signal Structure (Interchanged to Page 3)
% =============================================================================
\begin{frame}[t]
\slidetitle{Node, Message and Signal Structure}{Vehicle E/E Architecture \textbullet{} High-Speed CAN 500 kbps (ISO 11898-1) \textbullet{} Verified DBC/CAPL Message Flows}

\centering
\vspace{-0.08cm}
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[x=1cm, y=1cm]

  % 5 Nodes Across Top (4.00 cm center-to-center pitch -> full widescreen spread)
  \node[draw=none, fill=nodetester, rounded corners=7pt, minimum width=3.45cm, minimum height=1.06cm, text=white, align=center] (n_diag) at (1.75, 4.55) {\textbf{\normalsize DIAG}\\[2pt]\scriptsize Diagnostic Master};
  \node[draw=none, fill=nodeabs,    rounded corners=7pt, minimum width=3.45cm, minimum height=1.06cm, text=white, align=center] (n_abs)  at (5.75, 4.55) {\textbf{\normalsize ABS / ESP}\\[2pt]\scriptsize Chassis / ESC};
  \node[draw=none, fill=nodetcm,    rounded corners=7pt, minimum width=3.45cm, minimum height=1.06cm, text=white, align=center] (n_tcm)  at (9.75, 4.55) {\textbf{\normalsize TCM}\\[2pt]\scriptsize Gearbox};
  \node[draw=none, fill=nodeecm,    rounded corners=7pt, minimum width=3.45cm, minimum height=1.06cm, text=nodeecmtext, align=center] (n_ecm)  at (13.75, 4.55) {\textbf{\normalsize ECM}\\[2pt]\scriptsize Engine};
  \node[draw=none, fill=nodebcm,    rounded corners=7pt, minimum width=3.45cm, minimum height=1.06cm, text=white, align=center] (n_bcm)  at (17.75, 4.55) {\textbf{\normalsize BCM}\\[2pt]\scriptsize Body Gateway};

  % Bus Line, Drop Dots & Subtle Vertical Lifelines
  \draw[line width=2.6pt, color=busline] (0.00, 3.60) -- (19.50, 3.60);
  \foreach \x in {1.75, 5.75, 9.75, 13.75, 17.75} {
    \draw[line width=1.8pt, color=busline] (\x, 4.02) -- (\x, 3.60);
    \fill[busline] (\x, 3.60) circle (0.11);
    \draw[line width=0.8pt, dashed, color=busline!40] (\x, 3.60) -- (\x, -3.05);
  }

  % Row 1 (y=3.00): 0x100 ECM -> TCM [arrowhead = TCM Crimson]
  \begin{scope}[shift={(0, 3.00)}]
    \draw[line width=1.05pt, fill=nodetcm, draw=black] (9.75, 0) -- (10.13, -0.20) -- (10.13, 0.20) -- cycle;
    \draw[line width=1.05pt, fill=nodeecm, draw=black] (10.13, -0.20) rectangle (13.75, 0.20);
    \node[font=\bfseries\tiny, text=nodeecmtext, align=center, inner sep=0pt] at (11.94, 0) {Engine speed, throttle,\\[-1pt]torque, status (10 ms)};
    \draw[line width=1.05pt, fill=white, draw=black] (13.75, -0.20) rectangle (14.88, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (14.315, 0) {0x100};
  \end{scope}

  % Row 2 (y=2.28): 0x105 ECM -> TCM [Crimson] & BCM [Slate Blue]
  \begin{scope}[shift={(0, 2.28)}]
    \draw[line width=1.05pt, fill=nodetcm, draw=black] (9.75, 0) -- (10.13, -0.20) -- (10.13, 0.20) -- cycle;
    \draw[line width=1.05pt, fill=nodeecm, draw=black] (10.13, -0.20) rectangle (17.37, 0.20);
    \draw[line width=1.05pt, fill=nodebcm, draw=black] (17.75, 0) -- (17.37, -0.20) -- (17.37, 0.20) -- cycle;
    \draw[line width=1.05pt, fill=white, draw=black] (13.18, -0.20) rectangle (14.32, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (13.75, 0) {0x105};
    \node[font=\bfseries\scriptsize, text=nodeecmtext, inner sep=0pt] at (11.655, 0) {Coolant temp (50 ms)};
    \node[font=\bfseries\scriptsize, text=nodeecmtext, inner sep=0pt] at (15.845, 0) {Temp, fuel, MIL};
  \end{scope}

  % Row 3 (y=1.56): 0x200 ABS -> TCM [arrowhead = TCM Crimson]
  \begin{scope}[shift={(0, 1.56)}]
    \draw[line width=1.05pt, fill=white, draw=black] (4.62, -0.20) rectangle (5.75, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (5.185, 0) {0x200};
    \draw[line width=1.05pt, fill=nodeabs, draw=black] (5.75, -0.20) rectangle (9.37, 0.20);
    \node[font=\bfseries\tiny, text=white, align=center, inner sep=0pt] at (7.56, 0) {Wheel speed FL, FR,\\[-1pt]RL, RR (10 ms)};
    \draw[line width=1.05pt, fill=nodetcm, draw=black] (9.75, 0) -- (9.37, -0.20) -- (9.37, 0.20) -- cycle;
  \end{scope}

  % Row 4 (y=0.84): 0x205 ABS -> TCM (tap) -> ECM [arrowhead = ECM Light Grey]
  \begin{scope}[shift={(0, 0.84)}]
    \draw[line width=1.05pt, fill=white, draw=black] (4.62, -0.20) rectangle (5.75, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (5.185, 0) {0x205};
    \draw[line width=1.05pt, fill=nodeabs, draw=black] (5.75, -0.20) rectangle (13.37, 0.20);
    \node[font=\bfseries\scriptsize, text=white, inner sep=0pt] at (9.56, 0) {Vehicle speed, yaw rate, brake pressure, ESP (20 ms)};
    \filldraw[fill=nodetcm, draw=black, line width=0.8pt] (9.75, 0.20) circle (0.095);
    \draw[line width=1.05pt, fill=nodeecm, draw=black] (13.75, 0) -- (13.37, -0.20) -- (13.37, 0.20) -- cycle;
  \end{scope}

  % Row 5 (y=0.12): 0x300 TCM -> ECM (tap) -> BCM [arrowhead = BCM Slate Blue]
  \begin{scope}[shift={(0, 0.12)}]
    \draw[line width=1.05pt, fill=white, draw=black] (8.62, -0.20) rectangle (9.75, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (9.185, 0) {0x300};
    \draw[line width=1.05pt, fill=nodetcm, draw=black] (9.75, -0.20) rectangle (17.37, 0.20);
    \node[font=\bfseries\scriptsize, text=white, inner sep=0pt] at (13.56, 0) {Current gear, target, clutch, oil temp (20 ms)};
    \filldraw[fill=nodeecm, draw=black, line width=0.8pt] (13.75, 0.20) circle (0.095);
    \draw[line width=1.05pt, fill=nodebcm, draw=black] (17.75, 0) -- (17.37, -0.20) -- (17.37, 0.20) -- cycle;
  \end{scope}

  % Row 6 (y=-0.60): 0x400 BCM -> ECM (tap), TCM (tap), ABS [arrowhead = ABS Charcoal]
  \begin{scope}[shift={(0, -0.60)}]
    \draw[line width=1.05pt, fill=nodeabs, draw=black] (5.75, 0) -- (6.13, -0.20) -- (6.13, 0.20) -- cycle;
    \draw[line width=1.05pt, fill=nodebcm, draw=black] (6.13, -0.20) rectangle (17.75, 0.20);
    \node[font=\bfseries\scriptsize, text=white, inner sep=0pt] at (11.94, 0) {Ignition state, brake switch, hazard status (50 ms)};
    \filldraw[fill=nodetcm, draw=black, line width=0.8pt] (9.75, 0.20) circle (0.095);
    \filldraw[fill=nodeecm, draw=black, line width=0.8pt] (13.75, 0.20) circle (0.095);
    \draw[line width=1.05pt, fill=white, draw=black] (17.75, -0.20) rectangle (18.88, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (18.315, 0) {0x400};
  \end{scope}

  % Row 7 (y=-1.32): 0x7DF DIAG -> ABS, TCM, ECM, BCM [arrowhead = BCM Slate Blue]
  \begin{scope}[shift={(0, -1.32)}]
    \draw[line width=1.05pt, fill=white, draw=black] (0.62, -0.20) rectangle (1.75, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (1.185, 0) {0x7DF};
    \draw[line width=1.05pt, fill=nodetester, draw=black] (1.75, -0.20) rectangle (17.37, 0.20);
    \node[font=\bfseries\scriptsize, text=white, inner sep=0pt] at (9.56, 0) {UDS Functional Broadcast: Extended Session (0x10 03), Clear DTC (0x14) [Event]};
    \filldraw[fill=nodeabs, draw=black, line width=0.8pt] (5.75, 0.20) circle (0.095);
    \filldraw[fill=nodetcm, draw=black, line width=0.8pt] (9.75, 0.20) circle (0.095);
    \filldraw[fill=nodeecm, draw=black, line width=0.8pt] (13.75, 0.20) circle (0.095);
    \draw[line width=1.05pt, fill=nodebcm, draw=black] (17.75, 0) -- (17.37, -0.20) -- (17.37, 0.20) -- cycle;
  \end{scope}

  % Row 8 (y=-2.04): 0x7E0-0x7E3 DIAG -> Physical ECUs [arrowhead = BCM Slate Blue]
  \begin{scope}[shift={(0, -2.04)}]
    \draw[line width=1.05pt, fill=white, draw=black] (0.37, -0.20) rectangle (1.75, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (1.06, 0) {0x7E0--3};
    \draw[line width=1.05pt, fill=nodetester, draw=black] (1.75, -0.20) rectangle (17.37, 0.20);
    \node[font=\bfseries\scriptsize, text=white, inner sep=0pt] at (9.56, 0) {UDS Physical Requests: DTC Inquiry 0x19 02 (ABS 0x7E2, TCM 0x7E1, ECM 0x7E0, BCM 0x7E3)};
    \filldraw[fill=nodeabs, draw=black, line width=0.8pt] (5.75, 0.20) circle (0.095);
    \filldraw[fill=nodetcm, draw=black, line width=0.8pt] (9.75, 0.20) circle (0.095);
    \filldraw[fill=nodeecm, draw=black, line width=0.8pt] (13.75, 0.20) circle (0.095);
    \draw[line width=1.05pt, fill=nodebcm, draw=black] (17.75, 0) -- (17.37, -0.20) -- (17.37, 0.20) -- cycle;
  \end{scope}

  % Row 9 (y=-2.76): 0x7E8-0x7EB All ECUs -> DIAG [arrowhead = DIAG Purple]
  \begin{scope}[shift={(0, -2.76)}]
    \draw[line width=1.05pt, fill=nodetester, draw=black] (1.75, 0) -- (2.13, -0.20) -- (2.13, 0.20) -- cycle;
    \draw[line width=1.05pt, fill=slategrey!85, draw=black] (2.13, -0.20) rectangle (17.75, 0.20);
    \node[font=\bfseries\scriptsize, text=white, inner sep=0pt] at (9.94, 0) {UDS Physical Responses: 0x50, 0x59 Confirmed DTCs (ECM 0x7E8, TCM 0x7E9, ABS 0x7EA, BCM 0x7EB)};
    \filldraw[fill=nodeabs, draw=black, line width=0.8pt] (5.75, 0.20) circle (0.095);
    \filldraw[fill=nodetcm, draw=black, line width=0.8pt] (9.75, 0.20) circle (0.095);
    \filldraw[fill=nodeecm, draw=black, line width=0.8pt] (13.75, 0.20) circle (0.095);
    \draw[line width=1.05pt, fill=white, draw=black] (17.75, -0.20) rectangle (19.13, 0.20);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (18.44, 0) {0x7E8--B};
  \end{scope}

  % Priority Rule & Legend Footer (Verified 100% against CAPL & DBC!)
  \node[draw=cardborder, fill=cardbg, rounded corners=4pt, inner sep=4pt, minimum width=19.50cm, font=\scriptsize, text=slatedark, align=center] at (9.75, -3.48) {
    \textbf{CAN Priority:} \textbf{0x100 $>$ 0x105 $>$ 0x200 $>$ 0x205 $>$ 0x300 $>$ 0x400 $>$ 0x7DF $>$ 0x7E0--0x7E3 $>$ 0x7E8--0x7EB} \quad\textbar\quad \textbf{15 Messages \textbullet{} 43 Signals}\\[2pt]
    \textbf{Legend:} Banner Fill = Transmitter ECU \quad\textbullet\quad Arrowhead Color = Target Destination ECU \quad\textbullet\quad Top Dot = Subscriber / Multi-ECU Node
  };

\end{tikzpicture}%
}

\end{frame}

% =============================================================================
% SLIDE 4: System Architecture & Block Diagram (Interchanged to Page 4)
% =============================================================================
\begin{frame}[t]
\slidetitle{Detailed System Architecture}{Multi-Layer Automotive E/E Simulation Architecture in Vector CANoe 19}

\centering
\vspace{-0.06cm}
\resizebox{!}{6.02cm}{%
\begin{tikzpicture}[x=1cm, y=1cm, >={Stealth[length=5pt, width=3.5pt]}]

  % LAYER 1 (Top): Balanced Wide Stimulus & HMI Cards
  \node[draw=accentamber!90, fill=accentamber!8, rounded corners=5pt, line width=1.1pt, minimum width=7.2cm, minimum height=1.55cm] (inj_box) at (3.70, 4.72) {};
  \node[font=\bfseries\small, text=accentamber!90!black, anchor=north] at ($(inj_box.north)+(0,-0.06)$) {FAULT INJECTION \& STIMULUS LAYER};
  \node[font=\scriptsize, text=slatedark, anchor=north west] at ($(inj_box.north west)+(0.20,-0.40)$) {
    \begin{tabular}{@{}l@{\qquad}l@{}}
      \textbullet~WSS FL Open ($v=0$) & \textbullet~ABS / ECM Bus-Off \\
      \textbullet~Throttle Low (0\%)    & \textbullet~Brake Switch Stuck \\
      \textbullet~Coolant Overheat (125$^\circ$C) & \textbullet~Auto Test Suite
    \end{tabular}
  };

  \node[draw=accentgreen!80, fill=accentgreen!8, rounded corners=5pt, line width=1.1pt, minimum width=7.2cm, minimum height=1.55cm] (hmi_box) at (11.50, 4.72) {};
  \node[font=\bfseries\small, text=accentgreen!80!black, anchor=north] at ($(hmi_box.north)+(0,-0.06)$) {CANoe 19 COCKPIT HMI \& TELEMETRY};
  \node[font=\scriptsize, text=slatedark, anchor=north west] at ($(hmi_box.north west)+(0.20,-0.40)$) {
    \begin{tabular}{@{}l@{\qquad}l@{}}
      \textbullet~Speed, RPM \& Gear    & \textbullet~Hydraulic Bar Gauge \\
      \textbullet~Raw Symptom List      & \textbullet~Root Cause LED \\
      \multicolumn{2}{@{}l@{}}{\textbullet~ISO 14229 Service 0x19 04 Freeze Frame Log}
    \end{tabular}
  };

  % LAYER 2 (Middle): 4 Evenly Spaced ECUs
  \node[draw=nodebcm, fill=nodebcm!10, rounded corners=5pt, line width=1.1pt, minimum width=3.25cm, minimum height=1.52cm] (bcm) at (1.95, 2.42) {};
  \node[font=\bfseries\footnotesize, text=nodebcm, anchor=north] at ($(bcm.north)+(0,-0.06)$) {BCM (0x400)};
  \node[font=\scriptsize, text=slatedark, align=center, anchor=center] at ($(bcm.center)+(0,-0.16)$) {Brake Switch, Ignition\\Hazard State\\UDS: 0x7E3 / 0x7EB};

  \node[draw=nodeabs, fill=nodeabs!10, rounded corners=5pt, line width=1.1pt, minimum width=3.25cm, minimum height=1.52cm] (abs) at (5.72, 2.42) {};
  \node[font=\bfseries\footnotesize, text=nodeabs, anchor=north] at ($(abs.north)+(0,-0.06)$) {ABS (0x200, 0x205)};
  \node[font=\scriptsize, text=slatedark, align=center, anchor=center] at ($(abs.center)+(0,-0.16)$) {4 Wheel Speeds\\Brake Pressure\\UDS: 0x7E2 / 0x7EA};

  \node[draw=vectorred, fill=vectorred!8, rounded corners=5pt, line width=1.1pt, minimum width=3.25cm, minimum height=1.52cm] (ecm) at (9.48, 2.42) {};
  \node[font=\bfseries\footnotesize, text=vectorred, anchor=north] at ($(ecm.north)+(0,-0.06)$) {ECM (0x100, 0x105)};
  \node[font=\scriptsize, text=slatedark, align=center, anchor=center] at ($(ecm.center)+(0,-0.16)$) {RPM, Throttle, Torque\\Coolant Temp\\UDS: 0x7E0 / 0x7E8};

  \node[draw=nodetcm, fill=nodetcm!10, rounded corners=5pt, line width=1.1pt, minimum width=3.25cm, minimum height=1.52cm] (tcm) at (13.25, 2.42) {};
  \node[font=\bfseries\footnotesize, text=nodetcm, anchor=north] at ($(tcm.north)+(0,-0.06)$) {TCM (0x300)};
  \node[font=\scriptsize, text=slatedark, align=center, anchor=center] at ($(tcm.center)+(0,-0.16)$) {Current Gear, Clutch\\Limp Shift Lock\\UDS: 0x7E1 / 0x7E9};

  % HIGH-SPEED CAN BUS BAR
  \filldraw[fill=slatedark!85, draw=slatedark, rounded corners=2.5pt] (0.15, 0.50) rectangle (15.05, 0.90);
  \node[font=\bfseries\footnotesize, text=white] at (7.60, 0.70) {HIGH-SPEED CAN BUS (ISO 11898-1 \textbar{} 500 kbps \textbar{} 15 Messages \textbar{} 43 Signals)};

  % ECU <-> Bus bidirectional arrows
  \draw[line width=1.2pt, <->, color=nodebcm]   (bcm.south) -- (1.95, 0.90);
  \draw[line width=1.2pt, <->, color=nodeabs]   (abs.south) -- (5.72, 0.90);
  \draw[line width=1.2pt, <->, color=vectorred] (ecm.south) -- (9.48, 0.90);
  \draw[line width=1.2pt, <->, color=nodetcm]   (tcm.south) -- (13.25, 0.90);

  % LAYER 3 (Bottom): Diagnostic Master & DAG Engine
  \node[draw=nodetester, fill=nodetester!8, rounded corners=6pt, line width=1.1pt, minimum width=14.9cm, minimum height=1.42cm] (diag_box) at (7.60, -0.92) {};
  \node[font=\bfseries\small, text=nodetester, anchor=north] at ($(diag_box.north)+(0,-0.06)$) {DIAGNOSTIC MASTER \& TOPOLOGICAL ROOT CAUSE ISOLATION ENGINE};
  \node[font=\scriptsize, text=slatedark, align=center, anchor=center] at ($(diag_box.center)+(0,-0.16)$) {
    \textbf{ISO 14229-1 (UDS 0x19 02, Mask 0x09):} Functional Broadcast 0x7DF + Physical ECU Polling (0x7E0--0x7E3)\\[2pt]
    \textbf{DAG Engine:} Directed Acyclic Graph $G=(V, E)$ \textbullet{} In-Degree $\deg_S^-(v_i) = 0$ \textbullet{} 42.50 ms Latency ($<8~\mu$s MCU Exec)
  };

  % Bus <-> Master arrow
  \draw[line width=1.4pt, <->, color=nodetester] (7.60, 0.50) -- (diag_box.north);

  % Inter-Layer Links
  \draw[line width=1.1pt, ->, dashed, color=accentamber!90] (1.95, 3.945) -- (bcm.north);
  \draw[line width=1.1pt, ->, dashed, color=accentamber!90] (5.72, 3.945) -- (abs.north);
  \draw[line width=1.1pt, ->, dashed, color=accentgreen!80] (diag_box.east) -- (15.45, -0.92) |- (hmi_box.east);

\end{tikzpicture}%
}

\end{frame}

% =============================================================================
% SLIDE 5: Implementation Methodology – Directed Acyclic Graph (DAG) & Pruning
% =============================================================================
\begin{frame}[t]
\slidetitle{Implementation Methodology: DAG Pruning Algorithm}{Mathematical Formulation \textbullet{} Graph Topology \textbullet{} In-Degree Evaluation Loop}

\begin{columns}[T,totalwidth=\textwidth]

  % Column 1: DAG Formulation & Math
  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=vectorred!70, colbacktitle=vectorred!8, height=5.95cm,
      title={\normalsize\bfseries\color{vectorred} 1. Graph Formulation \& In-Degree}]
      \footnotesize\color{slatedark}\raggedright
      DAG $G = (V, E)$ models causal fault dependencies:
      \vspace{-3pt}
      \begin{itemize}\setlength{\itemsep}{1pt}\setlength{\leftmargini}{10pt}
        \item \textbf{Vertices:} $V=\{v_1{=}\text{ECM}, v_2{=}\text{ABS}, v_3{=}\text{TCM}, v_4{=}\text{BCM}\}$.
        \item \textbf{Edges:} $(v_i, v_j) \in E \iff v_j$ reads signals from $v_i$.
        \item \textbf{Failure Set ($S$):} Active DTC ECUs via UDS 0x19 02.
      \end{itemize}
      \vspace{-3pt}
      \textbf{Restricted In-Degree Metric:}\par
      \vspace{1pt}
      {\centering$\displaystyle \deg_S^-(v_i) = \sum_{v_j \in S} A_{ji}$\par}
      \vspace{3pt}
      \textbf{Isolation Decision Rule:}\par
      \vspace{1pt}
      {\centering$\deg_S^-(v_i) = 0 \implies \text{\textbf{Root Cause Node}}$\par}
      \vspace{1pt}
      {\centering$\deg_S^-(v_i) \ge 1 \implies \text{\textbf{Suppressed Symptom DTC}}$\par}
    \end{tcolorbox}
  \end{column}

  % Column 2: Visual Topology & Algorithmic Workflow
  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=accentblue!70, colbacktitle=accentblue!8, height=5.95cm,
      title={\normalsize\bfseries\color{accentblue} 2. Topology \& Algorithmic Workflow}]
      \centering
      \vspace{1pt}
      \begin{tikzpicture}[
          x=1cm, y=1cm,
          eculabel/.style={font=\sffamily\footnotesize\bfseries, align=center, minimum size=0.84cm, inner sep=1pt, circle, line width=1.1pt},
          edgearr/.style={-{Stealth[length=5.5pt, width=4pt]}, line width=1.1pt},
          edgelabel/.style={font=\sffamily\scriptsize, fill=cardbg, inner sep=1.2pt, rounded corners=2pt, text=slatedark}
      ]
        \node[eculabel, draw=nodebcm, fill=nodebcm, text=white]       (bcm) at (0, 2.10) {BCM};
        \node[eculabel, draw=nodeabs, fill=nodeabs, text=white]       (abs) at (-2.25, 1.05) {ABS};
        \node[eculabel, draw=nodeecmtext, fill=nodeecm, text=nodeecmtext] (ecm) at (2.25, 1.05) {ECM};
        \node[eculabel, draw=nodetcm, fill=nodetcm, text=white]       (tcm) at (0, 0) {TCM};

        \draw[line width=1.1pt, draw=nodeabs,     -{Stealth[length=6pt, width=4.4pt, fill=nodeabs]}]     (bcm) -- (abs) node[edgelabel, midway, above left=-1pt] {Brake Sw (0x400)};
        \draw[line width=1.1pt, draw=nodeecmtext, -{Stealth[length=6pt, width=4.4pt, fill=nodeecm]}]     (bcm) -- (ecm) node[edgelabel, midway, above right=-1pt] {Brake Sw (0x400)};
        \draw[line width=1.1pt, draw=nodeecmtext, -{Stealth[length=6pt, width=4.4pt, fill=nodeecm]}]     (abs) -- (ecm) node[edgelabel, midway] {Veh Speed (0x205)};
        \draw[line width=1.1pt, draw=nodetcm,     -{Stealth[length=6pt, width=4.4pt, fill=nodetcm]}]     (abs) -- (tcm) node[edgelabel, midway, below left=-1pt] {WSS/Spd (0x200/5)};
        \draw[line width=1.1pt, draw=nodetcm,     -{Stealth[length=6pt, width=4.4pt, fill=nodetcm]}]     (ecm) -- (tcm) node[edgelabel, midway, below right=-1pt] {RPM/Thr (0x100)};
      \end{tikzpicture}

      \vspace{3pt}
      \begin{minipage}{0.96\linewidth}
        \footnotesize\color{slatedark}\raggedright
        \textbf{Execution Steps:}\\[1pt]
        1. Poll all ECUs via UDS 0x19 02 (mask 0x09).\\
        2. Populate active DTC nodes into subgraph $S$.\\
        3. Compute in-degree $\deg_S^-(v)$ via matrix lookup.\\
        4. Isolate $\deg_S^-(v) = 0$ as Root Cause; prune rest.
      \end{minipage}
    \end{tcolorbox}
  \end{column}

\end{columns}

\end{frame}

% =============================================================================
% SLIDE 6: Vector CANoe 19 Simulation Setup & Diagnostic Cockpit Panel
% =============================================================================
\begin{frame}[t]
\slidetitle{Vector CANoe 19 Simulation \& Diagnostic Panel}{Virtual Vehicle Telemetry \textbullet{} Interactive Instrument Cluster \textbullet{} Real-Time CAPL Engine}

\begin{columns}[T,totalwidth=\textwidth]

  \begin{column}{0.46\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=vectorred!70, colbacktitle=vectorred!8, height=5.95cm,
      title={\normalsize\bfseries\color{vectorred} Virtual Network Environment}]
      \footnotesize\color{slatedark}\raggedright
      \vspace{-2pt}
      \begin{itemize}\setlength{\itemsep}{1pt}\setlength{\leftmargini}{10pt}
        \item \textbf{Vector CANoe 19 Engine:} Simulates complete 500 kbps CAN bus with event-driven CAPL node logic.
        \item \textbf{Realistic Vehicle Physics:} 4-wheel speeds, engine dynamics, gear shifts, and hydraulic braking.
        \item \textbf{Interactive Fault Injection:} Toggle switches inject open circuits, sensor shorts, and node dropouts.
        \item \textbf{Automated UDS Master:} Periodic CAPL timer polls 0x7DF/0x7E0--0x7E3; parses 0x59 into DAG bitmasks.
        \item \textbf{Zero-Jitter Execution:} Disambiguation runs in $<8~\mu$s with zero scheduling overhead.
      \end{itemize}
    \end{tcolorbox}
  \end{column}

  \begin{column}{0.52\textwidth}
    \begin{tcolorbox}[whitecard, height=5.95cm]
      \centering
      \includegraphics[width=\linewidth, height=4.45cm, keepaspectratio]{PANEL_NORMAL.png}\\[6pt]
      \footnotesize\color{slategrey}
      \textbf{CANoe 19 Cockpit HMI:} Fault-free cruise at 160.0 km/h (4200 RPM, 5th gear D5), showing healthy green status across all 4 ECUs.
    \end{tcolorbox}
  \end{column}

\end{columns}

\end{frame}

% =============================================================================
% SLIDE 7: Demonstration of Solution – Multi-Scenario Fault Isolation
% =============================================================================
\begin{frame}[t]
\slidetitle{Solution Demonstration: Multi-Scenario Fault Isolation}{6 Real-World Failure Modes \textbullet{} 100\% Disambiguation Accuracy \textbullet{} Zero False Replacements}

\begin{columns}[T,totalwidth=\textwidth]

  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=vectorred!70, colbacktitle=vectorred!8, height=5.12cm,
      title={\footnotesize\bfseries\color{vectorred} Scenario 1: Wheel Speed Sensor Open (ASIL-D)}]
      \centering
      \includegraphics[width=\linewidth, height=2.36cm, keepaspectratio]{WSS_SENSOR_OPEN/PANEL.jpg}\\[3pt]
      \begin{minipage}{0.98\linewidth}
        \scriptsize\color{slatedark}\raggedright
        \textbf{Raw Codes:} ABS (C0035-13), ECM (P0500-00), TCM (U0415-81).\\[2pt]
        \textbf{Topological Result:} ABS isolated ($\deg_S^- = 0$); ECM \& TCM suppressed ($\deg_S^- \ge 1$). 66.7\% DTC reduction; TCM enters speed-gated limp mode.
      \end{minipage}
    \end{tcolorbox}
  \end{column}

  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=accentblue!70, colbacktitle=accentblue!8, height=5.12cm,
      title={\footnotesize\bfseries\color{accentblue} Scenario 5: Brake Switch Stuck Closed (ASIL-B)}]
      \centering
      \includegraphics[width=\linewidth, height=2.36cm, keepaspectratio]{BRAKE_SWITCH_STUCK/PANEL.jpg}\\[3pt]
      \begin{minipage}{0.98\linewidth}
        \scriptsize\color{slatedark}\raggedright
        \textbf{Raw Codes:} BCM (B1318-11), ECM (P0504-00), TCM (U0422-81).\\[2pt]
        \textbf{Topological Result:} BCM isolated ($\deg_S^- = 0$). Hydraulic check proves pedal free ($P_{\text{hyd}} < 5$ bar); ASIL-D BTO cuts throttle to idle coastdown.
      \end{minipage}
    \end{tcolorbox}
  \end{column}

\end{columns}

\vspace{0.08cm}
\begin{tcolorbox}[colback=slategrey!10, colframe=cardborder, boxrule=0.7pt, arc=4pt, left=6pt, right=6pt, top=3pt, bottom=3pt]
  \centering\scriptsize\color{slatedark}
  \textbf{Other Tested Scenarios:} Sc. 2 (Throttle Low P0122-12, 1200 rpm limp) \quad\textbar\quad Sc. 3 (Coolant Overheat P0217-00, 125$^\circ$C) \quad\textbar\quad Sc. 4 \& 6 (ABS U0121-00 / ECM U0100-00 Bus-Off)
\end{tcolorbox}

\end{frame}

% =============================================================================
% SLIDE 8: Full-Page Video Demonstration Only (Direct Launch Action!)
% =============================================================================
\begin{frame}[t]
\slidetitle{Project Video Demonstration}{Vector CANoe 19 Live Simulation Execution \textbullet{} 1080p Full HD (30 fps) \textbullet{} 17m 57s}

\begin{tcolorbox}[cardstyle, colframe=vectorred, height=5.95cm, left=6pt, right=6pt, top=5pt, bottom=4pt]
  \centering
  \href{run:../CB.EN.U4EEE23112_IVN_VIDEO.mp4}{%
    \begin{tikzpicture}
      \node[inner sep=0pt] (vid) {\includegraphics[width=0.96\linewidth, height=4.95cm, keepaspectratio]{video_poster.jpg}};
      \fill[vectorred, opacity=0.92] (vid.center) circle (0.62cm);
      \fill[white] ($(vid.center)+(-0.15,-0.25)$) -- ($(vid.center)+(0.30,0)$) -- ($(vid.center)+(-0.15,0.25)$) -- cycle;
    \end{tikzpicture}%
  }\\[4pt]
  \footnotesize\color{slatedark}
  \href{run:../CB.EN.U4EEE23112_IVN_VIDEO.mp4}{\textbf{\color{vectorred}CLICK HERE TO PLAY VIDEO:}} \texttt{CB.EN.U4EEE23112\_IVN\_VIDEO.mp4} \quad\textbullet\quad 17 min 57 sec \quad\textbullet\quad 357.5 MB
\end{tcolorbox}

\end{frame}

% =============================================================================
% SLIDE 9: Experimental Results & Performance Summary (Table I Only)
% =============================================================================
\begin{frame}[t]
\slidetitle{Experimental Results \& Performance Summary}{100\% Isolation Accuracy \textbullet{} 63.9\% DTC Flood Suppression \textbullet{} 42.50 ms Interrogation Latency}

\begin{tcolorbox}[whitecard, colframe=vectorred!70, colbacktitle=vectorred!8, height=4.15cm,
  title={\small\bfseries\color{vectorred} Table I: Quantitative Root Cause Isolation Performance Across All 6 Failure Modes}]
  \centering
  \resizebox{0.99\linewidth}{!}{%
  \footnotesize
  \setlength{\tabcolsep}{6pt}
  \renewcommand{\arraystretch}{1.22}
  \begin{tabular}{@{}lcccccc@{}}
    \toprule
    \textbf{Injected Failure Scenario} & \textbf{ASIL} & \textbf{Isolated Root Cause} & \textbf{Raw DTCs} & \textbf{Suppressed} & \textbf{Efficiency} & \textbf{Latency} \\
    \midrule
    1: WSS FL Sensor Open Circuit & ASIL D & ABS (C0035-13) & 3 & 2 & 66.7\% & 42.10 ms \\
    2: Throttle Position Sensor Low & ASIL D & ECM (P0122-12) & 2 & 1 & 50.0\% & 41.80 ms \\
    3: Engine Coolant Overheat (125$^\circ$C) & ASIL B & ECM (P0217-00) & 3 & 2 & 66.7\% & 40.50 ms \\
    4: ABS Transceiver Node Cutoff & ASIL D & ABS (U0121-00) & 3 & 2 & 66.7\% & 45.20 ms \\
    5: Brake Switch Stuck Closed & ASIL B & BCM (B1318-11) & 3 & 2 & 66.7\% & 42.40 ms \\
    6: ECM Transceiver Node Cutoff & ASIL D & ECM (U0100-00) & 3 & 2 & 66.7\% & 43.00 ms \\
    \midrule
    \textbf{Average / Total} & \textbf{ASIL B--D} & \textbf{100\% True-Positive} & \textbf{2.8 (17)} & \textbf{1.8 (11)} & \textbf{63.9\%} & \textbf{42.50 ms} \\
    \bottomrule
  \end{tabular}%
  }
\end{tcolorbox}

\vspace{0.16cm}
\begin{columns}[T,totalwidth=\textwidth]
  \begin{column}{0.235\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=accentgreen!70, left=4pt, right=4pt, top=5pt, bottom=5pt, height=1.42cm]
      \centering{\large\bfseries\color{accentgreen} 100\%}\\[2pt]\scriptsize\color{slatedark}\textbf{Root Cause Accuracy}\\(6 / 6 Scenarios)
    \end{tcolorbox}
  \end{column}
  \begin{column}{0.235\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=vectorred!70, left=4pt, right=4pt, top=5pt, bottom=5pt, height=1.42cm]
      \centering{\large\bfseries\color{vectorred} 63.9\%}\\[2pt]\scriptsize\color{slatedark}\textbf{DTC Flood Reduction}\\(11 of 17 Pruned)
    \end{tcolorbox}
  \end{column}
  \begin{column}{0.235\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=accentblue!70, left=4pt, right=4pt, top=5pt, bottom=5pt, height=1.42cm]
      \centering{\large\bfseries\color{accentblue} 42.50 ms}\\[2pt]\scriptsize\color{slatedark}\textbf{Avg Isolation Latency}\\(ISO 26262 FTTI $<100$ ms)
    \end{tcolorbox}
  \end{column}
  \begin{column}{0.235\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=nodetester!70, left=4pt, right=4pt, top=5pt, bottom=5pt, height=1.42cm]
      \centering{\large\bfseries\color{nodetester} $<8~\mu$s}\\[2pt]\scriptsize\color{slatedark}\textbf{AURIX TC397 Exec}\\(1840 cyc \textbar{} 320 B mem)
    \end{tcolorbox}
  \end{column}
\end{columns}

\end{frame}

% =============================================================================
% SLIDE 10: Key Learnings, Zonal Scalability & Conclusion
% =============================================================================
\begin{frame}[t]
\slidetitle{Key Learnings, Scalability \& Conclusion}{Industrial Takeaways \textbullet{} Zonal E/E Migration \textbullet{} Evaluator Q\&A Transition}

\begin{columns}[T,totalwidth=\textwidth]

  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=vectorred!70, colbacktitle=vectorred!8, height=5.12cm,
      title={\normalsize\bfseries\color{vectorred} Key Engineering Learnings}]
      \footnotesize\color{slatedark}\raggedright\vspace{-4pt}
      \begin{itemize}\setlength{\itemsep}{2pt}\setlength{\leftmargini}{10pt}
        \item \textbf{Causal Over Rule-Based:} In-degree topological pruning eliminates cascading symptom DTCs without maintaining brittle static rule tables.
        \item \textbf{Functional Safety Guarantee:} Cross-checking mechanical sensors (0.8 bar hydraulic pressure) against electrical contacts plus BTO prevents phantom braking and overspeed.
        \item \textbf{Embedded Determinism:} Linear $O(|V| + |E|)$ complexity runs in $<8~\mu$s on automotive silicon with 100\% deterministic fail-safe behavior under ISO 26262.
      \end{itemize}
    \end{tcolorbox}
  \end{column}

  \begin{column}{0.485\textwidth}
    \begin{tcolorbox}[cardstyle, colframe=accentblue!70, colbacktitle=accentblue!8, height=5.12cm,
      title={\normalsize\bfseries\color{accentblue} Zonal Scalability \& Future Roadmap}]
      \footnotesize\color{slatedark}\raggedright\vspace{-4pt}
      \begin{itemize}\setlength{\itemsep}{2pt}\setlength{\leftmargini}{10pt}
        \item \textbf{Zonal E/E Readiness:} Adjacency bitmasks map directly onto high-speed zonal gateways and central compute clusters with $<320$ bytes memory for 50 nodes.
        \item \textbf{Future Extensions:} Dynamic DAG generation from vendor DBC/ARXML databases, ISO 13400 DoIP over gigabit Automotive Ethernet, and CAN-XL physical transceivers.
      \end{itemize}
    \end{tcolorbox}
  \end{column}

\end{columns}

\vspace{0.08cm}
\begin{tcolorbox}[colback=accentgreen!12, colframe=accentgreen!60, boxrule=0.9pt, arc=5pt, left=10pt, right=10pt, top=6pt, bottom=6pt]
  \centering\normalsize\bfseries\color{accentgreen!90!black}
  THANK YOU! \quad\textbullet\quad OPEN FOR EVALUATOR QUESTIONS \& DISCUSSION
\end{tcolorbox}

\end{frame}

\end{document}
"""

with open("Presentation/Project_Presentation.tex", "w", encoding="utf-8") as f:
    f.write(beamer_code)

print("Saved Presentation/Project_Presentation.tex")
