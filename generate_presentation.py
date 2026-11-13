import subprocess
import os

beamer_code = r"""\documentclass[aspectratio=169,10pt]{beamer}

% -------------------------------------------------------------
% Packages & Configuration
% -------------------------------------------------------------
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usetikzlibrary{calc,positioning,shapes.geometric,arrows.meta,fit,shadows}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}

% Graphicspath
\graphicspath{{../Images/}{../Images/CleanPlots/}{../Images/WSS_SENSOR_OPEN/}{../Images/BRAKE_SWITCH_STUCK/}{../Images/CUTOFF_ABS_NODE/}{../}}

% Remove default navigation symbols
\setbeamertemplate{navigation symbols}{}

% -------------------------------------------------------------
% Color Palette (Vector / Tata Automotive Theme)
% -------------------------------------------------------------
\definecolor{vectorred}{RGB}{166, 0, 44}       % Vector Corporate Crimson
\definecolor{slatedark}{RGB}{33, 37, 41}       % High-contrast charcoal
\definecolor{slategrey}{RGB}{100, 110, 120}    % Subtitle & border grey
\definecolor{cardbg}{RGB}{248, 250, 252}       % Card soft background
\definecolor{cardborder}{RGB}{218, 224, 232}   % Card border
\definecolor{accentblue}{RGB}{24, 90, 157}     % CAN Network Blue
\definecolor{accentgreen}{RGB}{22, 128, 60}    % RCA Success Green
\definecolor{accentpurple}{RGB}{112, 48, 160}  % Diagnostics Purple
\definecolor{accentamber}{RGB}{217, 119, 6}    % Fault Injection Amber

% Node & Message Colors
\definecolor{nodetester}{RGB}{112, 48, 160}     % DIAG_TESTER Diagnostics Purple
\definecolor{nodeabs}{RGB}{85, 90, 95}         % ABS/ESP Charcoal Grey
\definecolor{nodeecm}{RGB}{220, 224, 228}      % ECM Light Slate Grey
\definecolor{nodeecmtext}{RGB}{75, 80, 85}     % ECM Text Dark
\definecolor{nodetcm}{RGB}{166, 0, 44}         % TCM / Gearbox Crimson Red
\definecolor{nodebcm}{RGB}{60, 110, 155}       % BCM Slate Blue
\definecolor{msgdark}{RGB}{110, 115, 120}      % ABS Message Body Dark Grey
\definecolor{msglight}{RGB}{225, 230, 235}     % ECM Message Body Light Grey
\definecolor{msgtcm}{RGB}{166, 0, 44}          % TCM Message Body Red
\definecolor{msgbcm}{RGB}{70, 120, 165}        % BCM Message Body Slate Blue
\definecolor{busline}{RGB}{130, 135, 140}      % CAN Bus Line Grey

% Header & Footline Styling
\setbeamertemplate{headline}{}
\setbeamertemplate{footline}{
  \leavevmode%
  \hbox{%
    \begin{beamercolorbox}[wd=0.45\paperwidth,ht=2.5ex,dp=1.1ex,leftskip=1cm]{author in head/foot}%
      \tiny\color{slategrey}\textbf{Automated Root Cause Isolation in Multi-ECU Networks}
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=0.35\paperwidth,ht=2.5ex,dp=1.1ex,center]{title in head/foot}%
      \tiny\color{slategrey}Tata Technologies TechPulse \textbar{} IVN Capstone
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=0.20\paperwidth,ht=2.5ex,dp=1.1ex,rightskip=1cm,right]{date in head/foot}%
      \tiny\color{slategrey}\insertframenumber{} / \inserttotalframenumber
    \end{beamercolorbox}%
  }%
  \vskip0pt%
}

% Custom TikZ Macros for Slide 4 Message Banners
\newcommand{\msgRight}[8]{
  \begin{scope}[shift={(#1,#2)}]
    \draw[line width=1.1pt, fill=white, draw=black] (0, -0.27) rectangle (1.1, 0.27);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at (0.55, 0) {#3};
    \draw[line width=1.1pt, fill=#6, draw=black] (1.1, -0.27) rectangle ({1.1+#5}, 0.27);
    \node[font=\bfseries\scriptsize, text=#7, inner sep=0pt] at ({1.1 + #5/2}, 0) {#4};
    \draw[line width=1.1pt, fill=#8, draw=black] ({1.1+#5}, -0.27) -- ({1.1+#5+0.45}, 0) -- ({1.1+#5}, 0.27) -- cycle;
  \end{scope}
}

\newcommand{\msgLeft}[8]{
  \begin{scope}[shift={(#1,#2)}]
    \draw[line width=1.1pt, fill=#8, draw=black] (0, 0) -- (0.45, -0.27) -- (0.45, 0.27) -- cycle;
    \draw[line width=1.1pt, fill=#6, draw=black] (0.45, -0.27) rectangle ({0.45+#5}, 0.27);
    \node[font=\bfseries\scriptsize, text=#7, inner sep=0pt] at ({0.45 + #5/2}, 0) {#4};
    \draw[line width=1.1pt, fill=white, draw=black] ({0.45+#5}, -0.27) rectangle ({0.45+#5+1.1}, 0.27);
    \node[font=\bfseries\scriptsize, text=black, inner sep=0pt] at ({0.45+#5+0.55}, 0) {#3};
  \end{scope}
}

\begin{document}

% =============================================================================
% SLIDE 1: Project Title and Student Details (Centered Card)
% =============================================================================
\begin{frame}[t]
\vspace{0.35cm}
\centering

% Category Badge
\begin{tikzpicture}
  \node[fill=vectorred!10, text=vectorred, rounded corners=3pt, font=\scriptsize\bfseries, inner sep=4pt] {
    IN-VEHICLE NETWORKING (IVN) CAPSTONE PROJECT \quad\textbullet\quad B.TECH SEMESTER 7
  };
\end{tikzpicture}

\vspace{0.25cm}

% Main Title
{\LARGE\bfseries\color{vectorred} Automated Root Cause Isolation in Multi-ECU Networks}\\[5pt]
{\large\bfseries\color{slatedark} Signal Dependency Mapping \& UDS Diagnostics in Vector CANoe}\\[7pt]
{\footnotesize\color{slategrey} Compliant with ISO 14229-1 (UDS) \textbullet{} ISO 15765-2 (DoCAN) \textbullet{} ISO 26262 ASIL-D \textbullet{} ISO 11898-1}

\vspace{0.45cm}

% Centered Student Details Card
\begin{tikzpicture}[x=1cm, y=1cm]
  \node[draw=cardborder, fill=cardbg, rounded corners=9pt, line width=1.1pt, minimum width=9.2cm, minimum height=3.2cm] (student_card) at (7.0, 0) {};
  \node[fill=vectorred, text=white, font=\bfseries\scriptsize, rounded corners=3pt, inner sep=3.5pt, anchor=north] at (student_card.north) {STUDENT DETAILS};
  \node[font=\footnotesize, text=slatedark, align=left, anchor=north west] at ($(student_card.north west)+(0.6, -0.4)$) {
    \textbf{Name:} Harish R\\[3pt]
    \textbf{Roll Number:} CB.EN.U4EEE23112\\[3pt]
    \textbf{Degree:} Bachelor of Technology (B.Tech)\\[3pt]
    \textbf{Department:} Department of Electrical \& Electronics Engineering\\[3pt]
    \textbf{Institution:} Amrita School of Engineering, Coimbatore\\[3pt]
    \textbf{University:} Amrita Vishwa Vidyapeetham
  };
\end{tikzpicture}

\vspace{0.25cm}
{\scriptsize\color{slategrey}\textbf{Industry Collaboration:} Tata Technologies (TechPulse Program) \quad\textbullet\quad \textbf{Platform:} Vector CANoe 16.0}

\end{frame}

% =============================================================================
% SLIDE 2: Problem Statement and Objectives
% =============================================================================
\begin{frame}[t]
\vspace{0.15cm}
{\Large\bfseries\color{vectorred} Problem Statement \& Research Objectives}
\vspace{0.08cm}

{\footnotesize\color{slategrey} Multi-ECU Signal Cascades \textbullet{} False DTC Floods \textbullet{} ISO 26262 ASIL-D Determinism}
\vspace{0.35cm}

\centering
\begin{columns}[T,totalwidth=0.96\linewidth]

  % Problem Statement Column
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=vectorred!70, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=8pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{vectorred} The Problem: Cascading Alarm Floods}\\[6pt]
          \footnotesize\color{slatedark}
          \begin{itemize}\setlength{\itemsep}{4pt}
            \item \textbf{Dense Coupling:} Modern vehicles host 70--100 ECUs exchanging thousands of cross-dependent CAN signals.
            \item \textbf{Symptom Alarm Floods:} A single sensor or ECU failure causes data starvation across healthy downstream nodes, triggering dozens of secondary DTCs.
            \item \textbf{Misdiagnosis \& Cost:} Technicians replace healthy ECUs, inflating warranty costs and extending vehicle downtime.
            \item \textbf{Safety Risk:} Conflicting DTCs confuse fail-safe controllers, threatening unwanted torque cuts or phantom braking under ISO 26262.
          \end{itemize}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

  % Objectives Column
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=accentblue!70, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=8pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{accentblue} Project Objectives \& Contributions}\\[6pt]
          \footnotesize\color{slatedark}
          \begin{itemize}\setlength{\itemsep}{4pt}
            \item \textbf{DAG Signal Modeling:} Formulate in-vehicle signal flows as a Directed Acyclic Graph $G=(V, E)$ to capture causal dependencies.
            \item \textbf{On-Bus Pruning Engine:} Implement in-degree topological filtering in CAPL to isolate the true root cause in real time.
            \item \textbf{Deterministic Timing:} Achieve root cause disambiguation in $<50$ ms, well within the ISO 26262 ASIL-D 100 ms fault handling interval.
            \item \textbf{Vector CANoe HIL Setup:} Validate across 6 failure modes (sensor shorts, ECU dropouts, stuck contacts) with 100\% isolation accuracy.
          \end{itemize}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

\end{columns}

\vspace{0.35cm}
\begin{tikzpicture}
  \node[fill=slategrey!10, draw=cardborder, rounded corners=4pt, text=slatedark, font=\scriptsize, inner sep=5pt] {
    \textbf{Target Scope:} 4 Distributed ECUs (ECM, ABS, TCM, BCM) \textbullet{} 15 CAN Messages \textbullet{} 43 Powertrain \& Chassis Signals \textbullet{} 500 kbps CAN
  };
\end{tikzpicture}

\end{frame}

% =============================================================================
% SLIDE 3: System Architecture & Block Diagram (Full-Height Scaled TikZ)
% =============================================================================
\begin{frame}[t]
\vspace{0.08cm}
{\Large\bfseries\color{vectorred} Detailed System Architecture}
\vspace{0.05cm}

{\footnotesize\color{slategrey} Multi-Layer Automotive E/E Simulation Architecture in Vector CANoe 16.0}
\vspace{0.12cm}

\centering
\begin{tikzpicture}[x=1cm, y=1cm, >=Latex]

  % LAYER 1 (Top Left): Fault Injection & Virtual HMI Stimulus
  \node[draw=accentamber!90, fill=accentamber!8, rounded corners=6pt, line width=0.9pt, minimum width=3.8cm, minimum height=1.7cm] (inj_box) at (2.0, 3.4) {};
  \node[font=\bfseries\scriptsize, text=accentamber!90!black, anchor=north] at (inj_box.north) {FAULT INJECTION \& HMI};
  \node[font=\tiny, text=slatedark, align=left, anchor=center] at ($(inj_box.center)+(0,-0.12)$) {
    \textbullet~WSS Open Circuit ($v = 0$ km/h)\\
    \textbullet~Throttle Sensor Low (APP 0\%)\\
    \textbullet~Coolant Overheat (125$^\circ$C)\\
    \textbullet~ABS / ECM Hardware Cutoff\\
    \textbullet~Brake Switch Stuck (160 km/h)
  };

  % LAYER 2 (Top Right): Real-Time CANoe Cockpit Panel
  \node[draw=accentgreen!80, fill=accentgreen!8, rounded corners=6pt, line width=0.9pt, minimum width=3.8cm, minimum height=1.7cm] (hmi_box) at (12.0, 3.4) {};
  \node[font=\bfseries\scriptsize, text=accentgreen!80!black, anchor=north] at (hmi_box.north) {CANoe COCKPIT HMI};
  \node[font=\tiny, text=slatedark, align=left, anchor=center] at ($(hmi_box.center)+(0,-0.12)$) {
    \textbullet~Vehicle Speed \& Engine RPM\\
    \textbullet~Transmission Gear \& Limp State\\
    \textbullet~Hydraulic Pressure Bar Graph\\
    \textbullet~Raw Symptom DTC Display\\
    \textbullet~Automated Root Cause LED
  };

  % LAYER 3 (Middle): 4 Simulated ECUs
  % BCM
  \node[draw=nodebcm, fill=nodebcm!10, rounded corners=5pt, line width=0.9pt, minimum width=2.4cm, minimum height=1.5cm] (bcm) at (1.5, 0.7) {};
  \node[font=\bfseries\scriptsize, text=nodebcm, anchor=north] at (bcm.north) {BCM (0x400)};
  \node[font=\tiny, text=slatedark, align=center] at ($(bcm.center)+(0,-0.1)$) {Brake Pedal Switch\\Hazard \& Ignition\\UDS: 0x7E3/0x7EB};

  % ABS
  \node[draw=nodeabs, fill=nodeabs!10, rounded corners=5pt, line width=0.9pt, minimum width=2.4cm, minimum height=1.5cm] (abs) at (5.0, 0.7) {};
  \node[font=\bfseries\scriptsize, text=nodeabs, anchor=north] at (abs.north) {ABS (0x200, 0x205)};
  \node[font=\tiny, text=slatedark, align=center] at ($(abs.center)+(0,-0.1)$) {4 Wheel Speeds\\Brake Pressure\\UDS: 0x7E2/0x7EA};

  % ECM
  \node[draw=vectorred, fill=vectorred!8, rounded corners=5pt, line width=0.9pt, minimum width=2.4cm, minimum height=1.5cm] (ecm) at (8.5, 0.7) {};
  \node[font=\bfseries\scriptsize, text=vectorred, anchor=north] at (ecm.north) {ECM (0x100, 0x105)};
  \node[font=\tiny, text=slatedark, align=center] at ($(ecm.center)+(0,-0.1)$) {Engine RPM, Throttle\\Coolant Temp, Torque\\UDS: 0x7E0/0x7E8};

  % TCM
  \node[draw=nodetcm, fill=nodetcm!10, rounded corners=5pt, line width=0.9pt, minimum width=2.4cm, minimum height=1.5cm] (tcm) at (12.0, 0.7) {};
  \node[font=\bfseries\scriptsize, text=nodetcm, anchor=north] at (tcm.north) {TCM (0x300)};
  \node[font=\tiny, text=slatedark, align=center] at ($(tcm.center)+(0,-0.1)$) {Current Gear, Clutch\\Limp Shift Lock\\UDS: 0x7E1/0x7E9};

  % CAN BUS (ISO 11898-1, 500 kbps)
  \draw[line width=2.4pt, color=busline] (0.0, -0.6) -- (14.0, -0.6);
  \node[font=\bfseries\scriptsize, text=slatedark, anchor=south west] at (0.0, -0.52) {HIGH-SPEED CAN BUS (500 kbps, 15 Messages, 43 Signals)};

  % ECU to CAN bus connections
  \draw[line width=1.1pt, <->, color=nodebcm] (bcm.south) -- (1.5, -0.6);
  \draw[line width=1.1pt, <->, color=nodeabs] (abs.south) -- (5.0, -0.6);
  \draw[line width=1.1pt, <->, color=vectorred] (ecm.south) -- (8.5, -0.6);
  \draw[line width=1.1pt, <->, color=nodetcm] (tcm.south) -- (12.0, -0.6);

  % LAYER 4 (Bottom): Diagnostic Master & Topological Pruning Engine
  \node[draw=nodetester, fill=nodetester!8, rounded corners=6pt, line width=1.0pt, minimum width=13.4cm, minimum height=1.45cm] (diag_box) at (7.0, -1.8) {};
  \node[font=\bfseries\scriptsize, text=nodetester, anchor=north] at (diag_box.north) {DIAGNOSTIC MASTER \& TOPOLOGICAL ROOT CAUSE ISOLATION ENGINE};
  \node[font=\tiny, text=slatedark, align=center] at ($(diag_box.center)+(0,-0.12)$) {
    \textbf{ISO 14229-1 (UDS Service 0x19 02, Mask 0x08)} \textbullet{} Periodic 10 ms Diagnostic Interrogation over 0x7DF Broadcast\\
    \textbf{Topological Signal Dependency Model:} Directed Acyclic Graph $G=(V, E)$ \textbullet{} Adjacency Matrix Lookup \textbullet{} In-Degree Evaluation $\deg_S^-(v_i) = 0$\\
    \textbf{Real-Time Performance:} Worst-Case Latency = 42.50 ms \textbullet{} AURIX TC397 Execution = 1840 cycles ($<8~\mu$s) \textbullet{} 100\% Disambiguation Accuracy
  };

  % Master connection to bus
  \draw[line width=1.3pt, <->, color=nodetester] (7.0, -0.6) -- (diag_box.north);

  % Inter-layer links
  \draw[line width=0.8pt, ->, dashed, color=accentamber!90] (inj_box.south) -- (bcm.north);
  \draw[line width=0.8pt, ->, dashed, color=accentgreen!80] (diag_box.east) -| (hmi_box.south);

\end{tikzpicture}

\end{frame}

% =============================================================================
% SLIDE 4: CAN Network Message and Signal Structure (from Frame 3)
% =============================================================================
\begin{frame}[t]
\vspace{0.10cm}
{\Large\bfseries\color{vectorred} Node, Message and Signal Structure}
\vspace{0.06cm}

{\footnotesize\color{slategrey} Vehicle E/E Architecture \textbullet{} High-Speed CAN 500 kbps (ISO 11898-1) \textbullet{} CAN Priority Arbitration Ordering}
\vspace{0.15cm}

\centering
\begin{tikzpicture}[x=1cm, y=1cm]

  % Bus Line (Stretches across all 5 nodes)
  \draw[line width=2.0pt, color=busline] (0.0, 0) -- (14.0, 0);
  \node[font=\bfseries\scriptsize, text=slatedark, anchor=south west] at (0.0, 0.08) {HIGH-SPEED CAN BUS (500 kbps)};

  % Stub drops to bus
  \draw[line width=1.1pt, color=busline] (1.3, 0) -- (1.3, -0.65);
  \draw[line width=1.1pt, color=busline] (4.1, 0) -- (4.1, -0.65);
  \draw[line width=1.1pt, color=busline] (6.9, 0) -- (6.9, -0.65);
  \draw[line width=1.1pt, color=busline] (9.7, 0) -- (9.7, -0.65);
  \draw[line width=1.1pt, color=busline] (12.5, 0) -- (12.5, -0.65);

  % NODE 1: DIAG_TESTER
  \draw[line width=1.1pt, fill=nodetester, draw=black] (0.2, -0.65) rectangle (2.4, -1.25);
  \node[font=\bfseries\scriptsize, text=white] at (1.3, -0.95) {DIAG\_TESTER};

  % NODE 2: ABS
  \draw[line width=1.1pt, fill=nodeabs, draw=black] (3.0, -0.65) rectangle (5.2, -1.25);
  \node[font=\bfseries\scriptsize, text=white] at (4.1, -0.95) {ABS};

  % NODE 3: ECM
  \draw[line width=1.1pt, fill=nodeecm, draw=black] (5.8, -0.65) rectangle (8.0, -1.25);
  \node[font=\bfseries\scriptsize, text=nodeecmtext] at (6.9, -0.95) {ECM};

  % NODE 4: TCM
  \draw[line width=1.1pt, fill=nodetcm, draw=black] (8.6, -0.65) rectangle (10.8, -1.25);
  \node[font=\bfseries\scriptsize, text=white] at (9.7, -0.95) {TCM};

  % NODE 5: BCM
  \draw[line width=1.1pt, fill=nodebcm, draw=black] (11.4, -0.65) rectangle (13.6, -1.25);
  \node[font=\bfseries\scriptsize, text=white] at (12.5, -0.95) {BCM};

  % Left-Pointing Messages (ABS, ECM to Bus)
  \msgLeft{1.6}{3.5}{0x205}{ABS\_Dynamics (20 ms)}{2.1}{msgdark}{white}{msgdark}
  \msgLeft{1.6}{2.8}{0x200}{ABS\_WheelSpeeds (20 ms)}{2.1}{msgdark}{white}{msgdark}
  \msgLeft{4.4}{2.1}{0x105}{ECM\_Data\_2 (100 ms)}{2.1}{msglight}{black}{msglight}
  \msgLeft{4.4}{1.4}{0x100}{ECM\_Data\_1 (20 ms)}{2.1}{msglight}{black}{msglight}

  % Right-Pointing Messages (TCM, BCM to Bus)
  \msgRight{7.2}{3.5}{0x300}{TCM\_Status (50 ms)}{2.1}{msgtcm}{white}{msgtcm}
  \msgRight{10.0}{2.8}{0x400}{BCM\_Status (100 ms)}{2.1}{msgbcm}{white}{msgbcm}

  % Diagnostic Addressing Banner (Bottom)
  \node[draw=cardborder, fill=cardbg, rounded corners=4pt, inner sep=4pt] at (7.0, -1.75) {
    \tiny\color{slatedark}
    \textbf{Diagnostic Request/Response Mapping (ISO 15765-2):}
    Functional: \textbf{0x7DF} \quad\textbar\quad
    ECM: \textbf{0x7E0 / 0x7E8} \quad\textbar\quad
    TCM: \textbf{0x7E1 / 0x7E9} \quad\textbar\quad
    ABS: \textbf{0x7E2 / 0x7EA} \quad\textbar\quad
    BCM: \textbf{0x7E3 / 0x7EB}
  };

\end{tikzpicture}

\end{frame}

% =============================================================================
% SLIDE 5: Implementation Methodology – Directed Acyclic Graph (DAG) & Pruning
% =============================================================================
\begin{frame}[t]
\vspace{0.08cm}
{\Large\bfseries\color{vectorred} Implementation Methodology: DAG Pruning Algorithm}
\vspace{0.04cm}

{\footnotesize\color{slategrey} Mathematical Formulation \textbullet{} Graph Topology \textbullet{} In-Degree Evaluation Loop}
\vspace{0.15cm}

\centering
\begin{columns}[T,totalwidth=0.98\linewidth]

  % Column 1: DAG Formulation & Math
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=6pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{vectorred} 1. Graph Formulation \& In-Degree}\\[4pt]
          \scriptsize\color{slatedark}
          A Directed Acyclic Graph $G = (V, E)$ defines causal dependencies:
          \begin{itemize}\setlength{\itemsep}{2pt}
            \item \textbf{Vertices ($V$):} Physical/Virtual ECUs:
            $V = \{v_1{=}\text{ECM}, v_2{=}\text{ABS}, v_3{=}\text{TCM}, v_4{=}\text{BCM}\}$.
            \item \textbf{Edges ($E$):} Signal dependencies $(v_i, v_j) \in E \iff v_j$ consumes signals broadcast by $v_i$.
            \item \textbf{Active Failure Subgraph ($S$):} Set of all ECUs reporting active DTCs via UDS Service 0x19 02.
            \item \textbf{In-Degree Metric:}
            $$\deg_S^-(v_i) = \sum_{v_j \in S} A_{ji}$$
            \item \textbf{Decision Rule:}
            $$\deg_S^-(v_i) = 0 \implies \text{\textbf{Root Cause Node}}$$
            $$\deg_S^-(v_i) \ge 1 \implies \text{\textbf{Pruned Symptom DTC}}$$
          \end{itemize}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

  % Column 2: Visual Topology & Pruning Flowchart
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=6pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{accentblue} 2. Topology \& Algorithmic Workflow}\\[4pt]
          \centering
          \begin{tikzpicture}[
              scale=0.72,
              every node/.style={transform shape},
              ecunode/.style={circle, draw=black!85, fill=blue!10, line width=0.7pt, font=\sffamily\scriptsize\bfseries, align=center, minimum size=0.95cm},
              edgearr/.style={-{Stealth[length=4pt, width=2.5pt]}, line width=0.7pt, draw=black!80},
              edgelabel/.style={font=\sffamily\tiny, fill=white, inner sep=0.8pt, text=black!90}
          ]
            \node[ecunode] (bcm) at (0, 2.3) {BCM};
            \node[ecunode] (abs) at (-1.5, 1.15) {ABS};
            \node[ecunode] (ecm) at (1.5, 1.15) {ECM};
            \node[ecunode] (tcm) at (0, 0) {TCM};

            \draw[edgearr] (bcm) -- (abs) node[edgelabel, midway, above left] {Brake Sw};
            \draw[edgearr] (bcm) -- (ecm) node[edgelabel, midway, above right] {Brake Sw};
            \draw[edgearr] (abs) -- (ecm) node[edgelabel, midway, above] {WSS / Speed};
            \draw[edgearr] (abs) -- (tcm) node[edgelabel, midway, below left] {Veh Speed};
            \draw[edgearr] (ecm) -- (tcm) node[edgelabel, midway, below right] {RPM / Torque};
          \end{tikzpicture}\\[3pt]
          \tiny\color{slatedark}
          \textbf{Execution Steps:}\\
          1. Poll all nodes via UDS 0x19 02 with mask 0x08 (ConfirmedDTC).\\
          2. Extract active DTC reporting nodes into failure set $S$.\\
          3. Evaluate restricted in-degree $\deg_S^-(v)$ for each node in $S$.\\
          4. Tag nodes with $\deg_S^-(v) = 0$ as Root Cause; prune others.
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

\end{columns}

\end{frame}

% =============================================================================
% SLIDE 6: Vector CANoe 16.0 Simulation Setup & Diagnostic Cockpit Panel
% =============================================================================
\begin{frame}[t]
\vspace{0.08cm}
{\Large\bfseries\color{vectorred} Vector CANoe 16.0 Simulation \& Diagnostic Panel}
\vspace{0.04cm}

{\footnotesize\color{slategrey} Virtual Vehicle Telemetry \textbullet{} Interactive Instrument Cluster \textbullet{} Real-Time CAPL Engine}
\vspace{0.15cm}

\centering
\begin{columns}[T,totalwidth=0.98\linewidth]

  % Left Column: Testbench Architecture & CAPL Features
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=6pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{vectorred} Virtual Network Environment}\\[4pt]
          \scriptsize\color{slatedark}
          \begin{itemize}\setlength{\itemsep}{3pt}
            \item \textbf{Vector CANoe 16.0 Engine:} Simulates complete 500 kbps CAN bus with event-driven CAPL node logic.
            \item \textbf{Realistic Vehicle Physics:} 4-wheel independent speeds, engine dynamics, transmission gear hunting, and hydraulic brake modeling.
            \item \textbf{Interactive Fault Injection:} Toggle switches inject physical open circuits, sensor shorts, and transceiver dropouts on demand.
            \item \textbf{Automated UDS Master:} Periodic CAPL timer polls 0x7DF broadcast every 10 ms; parses 0x59 positive responses into DAG bitmasks.
            \item \textbf{Zero-Jitter Execution:} Disambiguation finishes in $<8~\mu$s, adding 0\% scheduling overhead to critical powertrain tasks.
          \end{itemize}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

  % Right Column: Screenshot of CANoe Cockpit Panel
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=white, rounded corners=6pt, line width=0.9pt, inner sep=3pt] {
        \includegraphics[width=0.95\linewidth, height=4.2cm, keepaspectratio]{PANEL_NORMAL.png}
      };
    \end{tikzpicture}\\[2pt]
    {\tiny\color{slategrey}\textbf{Fig. 4:} CANoe instrumentation panel during fault-free driving at 46.84 km/h in 3rd gear.}
  \end{column}

\end{columns}

\end{frame}

% =============================================================================
% SLIDE 7: Demonstration of Solution – Multi-Scenario Fault Isolation
% =============================================================================
\begin{frame}[t]
\vspace{0.08cm}
{\Large\bfseries\color{vectorred} Solution Demonstration: Multi-Scenario Fault Isolation}
\vspace{0.04cm}

{\footnotesize\color{slategrey} 6 Real-World Failure Modes \textbullet{} 100\% Disambiguation Accuracy \textbullet{} Zero False Replacements}
\vspace{0.12cm}

\centering
\begin{columns}[T,totalwidth=0.98\linewidth]

  % Left Card: Scenario 1 (WSS Open Circuit)
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=4pt, minimum width=\linewidth] {
        \begin{minipage}{0.95\linewidth}
          {\scriptsize\bfseries\color{vectorred} Scenario 1: Wheel Speed Sensor Open (ASIL-D)}\\[2pt]
          \includegraphics[width=\linewidth, height=2.2cm, keepaspectratio]{WSS_SENSOR_OPEN/PANEL.jpg}\\[2pt]
          \tiny\color{slatedark}
          \textbf{Raw Codes:} ABS (C0035-13), ECM (P0500-00), TCM (U0415-81).\\
          \textbf{Topological Result:} ABS isolated ($\deg_S^- = 0$); ECM/TCM suppressed ($\deg_S^- = 1$). 66.7\% reduction. TCM enters 3rd-gear limp mode.
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

  % Right Card: Scenario 5 (Brake Switch Stuck at 160 km/h)
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=4pt, minimum width=\linewidth] {
        \begin{minipage}{0.95\linewidth}
          {\scriptsize\bfseries\color{accentblue} Scenario 5: Brake Switch Stuck Closed (ASIL-B)}\\[2pt]
          \includegraphics[width=\linewidth, height=2.2cm, keepaspectratio]{BRAKE_SWITCH_STUCK/PANEL.jpg}\\[2pt]
          \tiny\color{slatedark}
          \textbf{Raw Codes:} BCM (B1318-11), ECM (P0504-00), TCM (U0422-81).\\
          \textbf{Topological Result:} BCM isolated ($\deg_S^- = 0$). Hydraulic cross-check confirms pedal free ($P_{\text{hyd}} < 5$ bar); ASIL-D BTO cuts throttle to idle coastdown.
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

\end{columns}

\vspace{0.15cm}
\begin{tikzpicture}
  \node[fill=slategrey!10, draw=cardborder, rounded corners=3pt, text=slatedark, font=\tiny, inner sep=3.5pt] {
    \textbf{Other Tested Scenarios:} Sc. 2 (Throttle Low P0122-12, 1200 rpm limp) \textbar{} Sc. 3 (Coolant 125$^\circ$C P0217-00) \textbar{} Sc. 4 \& 6 (ABS U0121-00 / ECM U0100-00 Cutoffs).
  };
\end{tikzpicture}

\end{frame}

% =============================================================================
% SLIDE 8: Video Demonstration & Demo Walkthrough
% =============================================================================
\begin{frame}[t]
\vspace{0.08cm}
{\Large\bfseries\color{vectorred} Project Video Demonstration \& Live Runbook}
\vspace{0.04cm}

{\footnotesize\color{slategrey} Full Vector CANoe Test Execution \textbullet{} 1080p 30fps Recording \textbullet{} Timestamp Breakdown}
\vspace{0.15cm}

\centering
\begin{columns}[T,totalwidth=0.98\linewidth]

  % Left Column: Video Metadata & Playback Link
  \begin{column}{0.44\linewidth}
    \begin{tikzpicture}
      \node[draw=vectorred, fill=cardbg, rounded corners=6pt, line width=1.0pt, inner sep=6pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{vectorred} Demonstration Video File}\\[4pt]
          \scriptsize\color{slatedark}
          \textbf{File Name:} \texttt{CB.EN.U4EEE23112\_IVN\_VIDEO.mp4}\\[2pt]
          \textbf{Duration:} 17 Minutes 57 Seconds\\[2pt]
          \textbf{Resolution:} 1080p Full HD (30 fps)\\[2pt]
          \textbf{Size:} 357.5 MB\\[6pt]
          \begin{tikzpicture}
            \node[fill=vectorred, text=white, rounded corners=4pt, font=\scriptsize\bfseries, inner sep=5pt] {
              \href{run:../CB.EN.U4EEE23112_IVN_VIDEO.mp4}{\color{white}CLICK TO LAUNCH VIDEO DEMO}
            };
          \end{tikzpicture}\\[5pt]
          {\tiny\color{slategrey}\textit{Backup copy verified and ready in root and Video/ folders.}}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

  % Right Column: Video Breakdown Timeline Table
  \begin{column}{0.52\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=white, rounded corners=6pt, line width=0.9pt, inner sep=5pt, minimum width=\linewidth] {
        \begin{minipage}{0.95\linewidth}
          {\scriptsize\bfseries\color{slatedark} Video Scenario Breakdown \& Cue Sheet}\\[3pt]
          \tiny
          \begin{tabular}{@{}ccl@{}}
            \toprule
            \textbf{Timestamp} & \textbf{Phase} & \textbf{Key Observation / Proof Point} \\
            \midrule
            \textbf{00:00 - 02:45} & Baseline & 46.84 km/h cruising, 3rd gear, zero DTCs \\
            \textbf{02:45 - 05:30} & Sc. 1 (WSS) & Speed drops, ABS C0035-13 isolated (66.7\% pruned) \\
            \textbf{05:30 - 08:15} & Sc. 2 (APP) & Throttle 0\%, ECM P0122-12 isolated (50.0\% pruned) \\
            \textbf{08:15 - 11:00} & Sc. 3 (Coolant) & 125$^\circ$C overheat, ECM P0217-00 isolated \\
            \textbf{11:00 - 13:45} & Sc. 4 \& 6 (Cutoffs) & Missing heartbeats, ABS U0121 / ECM U0100 isolated \\
            \textbf{13:45 - 17:57} & Sc. 5 (Brake) & BTO idle coastdown, BCM B1318-11 isolated \\
            \bottomrule
          \end{tabular}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

\end{columns}

\vspace{0.25cm}
\begin{tikzpicture}
  \node[fill=accentgreen!10, draw=accentgreen!40, rounded corners=3pt, text=accentgreen!90!black, font=\scriptsize\bfseries, inner sep=4pt] {
    Demo Setup Verified: Vector CANoe 16.0 loaded \textbullet{} CANalyzer trace active \textbullet{} Virtual HMI responsive
  };
\end{tikzpicture}

\end{frame}

% =============================================================================
% SLIDE 9: Quantitative Results & State-of-the-Art Benchmark
% =============================================================================
\begin{frame}[t]
\vspace{0.06cm}
{\Large\bfseries\color{vectorred} Experimental Results \& State-of-the-Art Benchmark}
\vspace{0.04cm}

{\footnotesize\color{slategrey} 100\% Isolation Accuracy \textbullet{} 63.9\% DTC Suppression \textbullet{} 42.50 ms Interrogation Latency}
\vspace{0.12cm}

\centering
\begin{columns}[T,totalwidth=0.98\linewidth]

  % Left Table: 6 Scenarios Quantitative Performance
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=white, rounded corners=6pt, line width=0.9pt, inner sep=4pt, minimum width=\linewidth] {
        \begin{minipage}{0.95\linewidth}
          {\scriptsize\bfseries\color{vectorred} Table I: Scenario Performance Across Failure Modes}\\[2pt]
          \tiny
          \begin{tabular}{@{}lcccc@{}}
            \toprule
            \textbf{Scenario} & \textbf{ASIL} & \textbf{Raw} & \textbf{Suppressed} & \textbf{Latency} \\
            \midrule
            1: WSS Open Circuit   & ASIL D & 3 & 2 (66.7\%) & 42.10 ms \\
            2: Throttle Sensor Low & ASIL D & 2 & 1 (50.0\%) & 41.80 ms \\
            3: Coolant Overheat   & ASIL B & 3 & 2 (66.7\%) & 40.50 ms \\
            4: ABS Node Cutoff    & ASIL D & 3 & 2 (66.7\%) & 45.20 ms \\
            5: Brake Switch Stuck & ASIL B & 3 & 2 (66.7\%) & 42.40 ms \\
            6: ECM Node Cutoff    & ASIL D & 3 & 2 (66.7\%) & 43.00 ms \\
            \midrule
            \textbf{Average / Total} & \textbf{B--D} & \textbf{2.8 (17)} & \textbf{1.8 (63.9\%)} & \textbf{42.50 ms} \\
            \bottomrule
          \end{tabular}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

  % Right Table: State-of-the-Art Comparison
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=white, rounded corners=6pt, line width=0.9pt, inner sep=4pt, minimum width=\linewidth] {
        \begin{minipage}{0.95\linewidth}
          {\scriptsize\bfseries\color{accentblue} Table II: State-of-the-Art Comparative Benchmark}\\[2pt]
          \tiny
          \begin{tabular}{@{}llccc@{}}
            \toprule
            \textbf{Framework} & \textbf{Methodology} & \textbf{Complexity} & \textbf{Latency} & \textbf{RAM} \\
            \midrule
            Lin \emph{et al.} (2023)  & Matrix Rules   & $O(N^2)$      & 120 ms  & 12.4 KB \\
            Liu \emph{et al.} (2023)  & Bayesian DAG   & $O(2^k |V|)$  & 340 ms  & 45.2 KB \\
            Wang \emph{et al.} (2023) & Wire Topology  & $O(N)$        & 210 ms  & 8.6 KB  \\
            Lu \emph{et al.} (2025)   & CNN-LSTM       & High          & 85 ms   & 5.8 MB  \\
            Bohne \emph{et al.} (2023)& Neuro-Symbolic & NP-Hard       & 1250 ms & 22.1 MB \\
            \midrule
            \textbf{This Work}        & \textbf{DAG Pruning} & $\mathbf{O(|V|{+}|E|)}$ & \textbf{42.5 ms} & $\mathbf{<320}$ \textbf{B} \\
            \bottomrule
          \end{tabular}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

\end{columns}

\vspace{0.25cm}
\begin{tikzpicture}
  \node[fill=cardbg, draw=cardborder, rounded corners=4pt, text=slatedark, font=\tiny, inner sep=4pt] {
    \textbf{Microcontroller Silicon Benchmark:} Infineon AURIX TC397 (300 MHz) execution = \textbf{1840 cycles} ($<8~\mu$s) \textbullet{} 32 B RAM \textbullet{} 288 B Flash ROM.
  };
\end{tikzpicture}

\end{frame}

% =============================================================================
% SLIDE 10: Key Learnings, Zonal Scalability & Conclusion
% =============================================================================
\begin{frame}[t]
\vspace{0.08cm}
{\Large\bfseries\color{vectorred} Key Learnings, Scalability \& Conclusion}
\vspace{0.04cm}

{\footnotesize\color{slategrey} Industrial Takeaways \textbullet{} Zonal E/E Migration \textbullet{} Evaluator Q\&A Transition}
\vspace{0.20cm}

\centering
\begin{columns}[T,totalwidth=0.98\linewidth]

  % Card 1: Key Learnings
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=6pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{vectorred} Key Engineering Learnings}\\[4pt]
          \scriptsize\color{slatedark}
          \begin{itemize}\setlength{\itemsep}{3pt}
            \item \textbf{Causal Over Rule-Based:} In-degree topological pruning mathematically eliminates cascading symptom DTCs without maintaining massive, brittle static rule tables.
            \item \textbf{Functional Safety Guarantee:} Cross-checking mechanical sensors (e.g. 0 bar hydraulic pressure) against electrical switches prevents catastrophic phantom braking at highway speeds.
            \item \textbf{Embedded Determinism:} Linear $O(|V| + |E|)$ complexity runs in $<8~\mu$s on automotive silicon, providing 100\% deterministic fail-safe behavior under ISO 26262.
          \end{itemize}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

  % Card 2: Zonal Scalability & Conclusion
  \begin{column}{0.48\linewidth}
    \begin{tikzpicture}
      \node[draw=cardborder, fill=cardbg, rounded corners=6pt, line width=0.9pt, inner sep=6pt, minimum width=\linewidth] {
        \begin{minipage}{0.94\linewidth}
          {\normalsize\bfseries\color{accentblue} Zonal Scalability \& Conclusion}\\[4pt]
          \scriptsize\color{slatedark}
          \begin{itemize}\setlength{\itemsep}{3pt}
            \item \textbf{Zonal E/E Readiness:} Adjacency matrices map directly onto high-speed zonal gateways and virtualized software clusters with $<320$ bytes flash memory for 50 nodes.
            \item \textbf{Future Extensions:} Dynamic DAG parsing from vendor DBC/ARXML databases, ISO 13400 DoIP over gigabit Ethernet, and CAN-XL physical transceivers.
          \end{itemize}
          \vspace{4pt}
          \begin{tikzpicture}
            \node[fill=accentgreen!15, draw=accentgreen!50, rounded corners=4pt, text=accentgreen!90!black, font=\scriptsize\bfseries, inner sep=4pt] {
              THANK YOU! \quad\textbullet\quad OPEN FOR EVALUATOR Q\&A
            };
          \end{tikzpicture}
        \end{minipage}
      };
    \end{tikzpicture}
  \end{column}

\end{columns}

\vspace{0.25cm}
{\scriptsize\color{slategrey}\textbf{Project Repository \& Backups Verified} \quad\textbullet\quad Vector CANoe 16.0 Live Demo Ready}

\end{frame}

\end{document}
"""

with open("Presentation/Project_Presentation.tex", "w", encoding="utf-8") as f:
    f.write(beamer_code)

print("Saved Presentation/Project_Presentation.tex")
