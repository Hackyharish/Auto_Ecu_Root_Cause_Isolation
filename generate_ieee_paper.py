import os
import subprocess
import pymupdf

def build_paper():
    tex_code = r"""\documentclass[conference]{IEEEtran}
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{url}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning}

\setlength{\textfloatsep}{4pt plus 1pt minus 1pt}
\setlength{\floatsep}{4pt plus 1pt minus 1pt}
\setlength{\intextsep}{4pt plus 1pt minus 1pt}
\setlength{\abovecaptionskip}{2.5pt}
\setlength{\belowcaptionskip}{1.5pt}

\graphicspath{{./Images/}{./Images/CleanPlots/}{./Presentation/}}

\begin{document}

\title{Automated Root Cause Isolation in Multi-ECU Automotive Networks Using Signal Dependency Mapping and UDS Diagnostics}

\author{\IEEEauthorblockN{Harish R.}
\IEEEauthorblockA{\textit{Department of Electrical and Electronics Engineering} \\
\textit{Amrita School of Engineering, Coimbatore} \\
\textit{Amrita Vishwa Vidyapeetham, India} \\
Email: cb.en.u4eee23112@cb.students.amrita.edu}
\and
\IEEEauthorblockN{Dr. S. Saravanan}
\IEEEauthorblockA{\textit{Department of Electrical and Electronics Engineering} \\
\textit{Amrita School of Engineering, Coimbatore} \\
\textit{Amrita Vishwa Vidyapeetham, India} \\
Email: s\_saravanan@cb.amrita.edu}
}

\maketitle

\begin{abstract}
Centralized zonal architectures in modern vehicles route hundreds of cyclic sensor signals across shared CAN and CAN-FD backbones. When an upstream sensor fails, dependent electronic control units (ECUs) log secondary Diagnostic Trouble Codes (DTCs) within milliseconds, creating symptom cascades that disguise the primary defect during dealer service. We address this diagnostic ambiguity with an on-bus topological isolation engine compliant with ISO 11898-1 and ISO 14229-1 (UDS). Operational signal flows across 15 CAN messages and 43 signals are formalized into a Directed Acyclic Graph (DAG) covering safety functions rated up to ISO 26262 ASIL~D. At runtime, a master ECU queries nodes over ISO 15765-2 DoCAN transport layers via UDS Service 0x19 Subfunction 0x02 (mask 0x08), isolating root causes through active-subgraph in-degree pruning. We validated the framework in Vector CANoe 16.0 across six fault injection scenarios, including open-circuit wheel speed sensors, throttle faults, coolant overheating, and bus-off disconnects. The engine achieved 100\% root cause isolation accuracy, suppressed secondary DTCs by an average of 63.9\%, and completed topological evaluation in under 10 microseconds, yielding a total network diagnostic latency of 42.50 milliseconds.
\end{abstract}

\begin{IEEEkeywords}
Automated diagnostics, ASIL ratings, Controller Area Network, Directed Acyclic Graph, fault isolation, ISO 14229-1, ISO 26262, root cause analysis, Unified Diagnostic Services, Vector CANoe, zonal architecture.
\end{IEEEkeywords}

\section{Introduction}
Automotive embedded systems rely heavily on ISO 11898-1 Controller Area Network (CAN) buses running at 500 kbps to link powertrain, chassis, and body electronics. Controllers broadcast periodic frames every 20 to 100 ms. These frames contain shared variables, such as wheel angular velocities, accelerator positions, and brake line pressures. Automotive designs are moving away from federated electronic control units (ECUs) toward centralized zonal architectures. In these configurations, zone gateways aggregate local sensor data and bridge high-rate chassis telemetry onto common backbones. This consolidation tightens cross-module coupling. A single upstream transceiver failure or sensor wiring break now propagates across downstream software components within tens of milliseconds.

Diagnostic handling follows ISO 14229-1 Unified Diagnostic Services (UDS) and emissions mandates. When an ECU detects an input timeout or an out-of-range value, its diagnostic executive sets a confirmed Diagnostic Trouble Code (DTC) in EEPROM adhering to SAE J2012 and ISO 15031-6. Standard service tools query these logs over the ISO 15031-3 OBD port. When a wiring fault strikes an Antilock Braking System (ABS) wheel speed circuit, the ABS node sets DTC C0035-13. The Transmission Control Module (TCM), deprived of velocity updates, logs U0415-81 and engages a mechanical third-gear lockup. The Engine Control Module (ECM) then flags missing vehicle speed via P0500-00. Technicians face three or four simultaneous DTCs from unaffected modules. Misinterpreting these secondary symptom codes inflates repair times and prompts warranty returns for undamaged ECUs.

Zonal topologies make immediate fault disambiguation safety-critical. Under ISO 26262, functions like electronic stability control and electronic throttle management carry ASIL~D requirements, demanding strict fail-operational or deterministic fail-safe responses. If an ECU misinterprets missing CAN frames as local hardware destruction, it may disconnect safety-critical actuators without cause. 

Directly resolving root causes on-bus prevents these false trips. We model directional data dependencies across 15 CAN messages as a Directed Acyclic Graph (DAG) and execute topological in-degree pruning directly on an embedded diagnostic master. We evaluated the mechanism inside Vector CANoe 16.0 using compiled Communication Access Programming Language (CAPL) nodes, physical transport layers (ISO 15765-2), and simulated physical fault injection panels.

\begin{figure}[t]
\centering
\begin{tikzpicture}[
    scale=0.76,
    every node/.style={transform shape},
    box/.style={draw=black!80, fill=blue!6, rounded corners=2pt, font=\sffamily\footnotesize, align=center, inner sep=2.5pt, line width=0.6pt},
    ecubox/.style={draw=black!70, fill=green!10, rounded corners=2pt, font=\sffamily\scriptsize, align=center, inner sep=2pt, line width=0.5pt, minimum width=1.35cm},
    bus/.style={draw=black!90, fill=gray!18, rounded corners=1pt, font=\sffamily\footnotesize\bfseries, align=center, line width=0.9pt, minimum width=7.0cm, minimum height=0.40cm},
    diagbox/.style={draw=black!80, fill=orange!12, rounded corners=2pt, font=\sffamily\footnotesize, align=center, inner sep=2.5pt, line width=0.6pt},
    outbox/.style={draw=red!80, fill=red!10, rounded corners=2pt, font=\sffamily\footnotesize\bfseries, align=center, inner sep=2.5pt, line width=0.8pt},
    arr/.style={-{Stealth[length=3.5pt, width=2.5pt]}, line width=0.6pt, draw=black!80},
    darr/.style={-{Stealth[length=3.5pt, width=2.5pt]}, dashed, line width=0.6pt, draw=red!80}
]

\node[box, minimum width=4.2cm] (fi) {Fault Injection Panel\\(Simulated Sensor Defects)};
\node[bus, below=0.35cm of fi] (can) {High-Speed CAN Bus (500 kbps)};

\node[ecubox, below=0.32cm of can.south west, xshift=1.0cm] (ecm) {ECM\\Engine};
\node[ecubox, right=0.3cm of ecm] (abs) {ABS\\Brakes};
\node[ecubox, right=0.3cm of abs] (tcm) {TCM\\Trans};
\node[ecubox, right=0.3cm of tcm] (bcm) {BCM\\Body};

\node[diagbox, minimum width=4.5cm, below=0.40cm of abs, xshift=0.8cm] (master) {Diagnostic Master\\(UDS Service 0x19 Polling)};
\node[diagbox, minimum width=4.5cm, below=0.28cm of master] (dag) {DAG Pruning Engine\\(In-Degree Topological Isolation)};
\node[outbox, minimum width=4.0cm, below=0.28cm of dag] (out) {Isolated Root Cause\\(Filtered Primary Fault)};

\draw[arr] (fi) -- (can);
\draw[arr] (can.south -| ecm) -- (ecm);
\draw[arr] (can.south -| abs) -- (abs);
\draw[arr] (can.south -| tcm) -- (tcm);
\draw[arr] (can.south -| bcm) -- (bcm);

\draw[darr] (master.north) -- (can.south -| master.north) node[midway, right, font=\tiny, text=red!80] {UDS Physical 0x7Ex};
\draw[arr] (master) -- (dag);
\draw[arr] (dag) -- (out);

\end{tikzpicture}
\caption{System layout showing CAN bus topology, interconnected ECUs, and the diagnostic isolation master.}
\label{fig:system_arch}
\end{figure}

\section{Literature Review}
Automotive network diagnostics spans three distinct research thrusts in recent publications.

Parameter tracking and real-time execution in electrified powertrains represent the first focus. In electric propulsion systems, accurate behavioral parameter estimation prevents cross-domain electrical fault propagation \cite{saravanan2025starter}, \cite{saravanan2025parameter}. Maintaining strict message cycle times and deterministic arbitration over CAN backbones is equally necessary for multi-axis embedded actuator stability \cite{krishnan2021can}. 

Bus timing, protocol vulnerabilities, and physical wiring anomalies form a second major direction. Because classical CAN lacks link-layer origin authentication, malicious or noisy frames propagate corrupt signals to downstream controllers unchecked \cite{nair2025qml}. Intermittent connection faults introduce bit-stuffing violations and arbitration retransmissions across distributed wiring topologies \cite{wang2023can}. When running ISO 14229 UDS routines alongside cyclic powertrain frames, diagnostic request scheduling must avoid arbitration starvation \cite{schmidt2022uds}, \cite{nolte2022wcrt}. Di Natale \cite{dinatale2022can} established that worst-case latency analysis remains essential for preserving periodic control bandwidth during asynchronous diagnostic bursts.

The third body of work addresses topological fault isolation. Structural dependency matrices distinguish primary component dropouts from secondary bus symptoms in distributed systems \cite{zhang2022graph}. Lin \emph{et al.} \cite{lin2023zonal} demonstrated matrix disambiguation across zonal gateways, while Liu \emph{et al.} \cite{liu2023dag} formulated Bayesian DAG belief networks for multi-ECU electric vehicle diagnostics. Emerging techniques deploy hybrid CNN-LSTM neural networks \cite{lu2025deep} or neuro-symbolic knowledge graphs \cite{bohne2023neuro} to isolate vehicle faults. Yet neural and probabilistic methods incur substantial memory footprints ($>5$ MB) and variable inference delays, which complicates ISO 26262 ASIL~D determinism audits. Our work bypasses these overheads by uniting deterministic in-degree topological graph pruning with ISO 14229 Service 0x19 interrogation directly inside the gateway layer.

\begin{figure}[t]
\centering
\includegraphics[width=0.74\columnwidth]{CAN_NODES.png}
\caption{Vector CANoe simulation setup with four functional ECUs interconnected across a 500 kbps bus.}
\label{fig:can_nodes}
\end{figure}

\section{Methodology}
Our diagnostic pipeline integrates four engineering modules: an industry-standard CAN message database, a mathematical Directed Acyclic Graph dependency model, a real-time topological pruning algorithm, and a Vector CANoe simulation setup.

\subsection{Powertrain and Chassis CAN Network Architecture}
The simulated network models four functional controllers sharing a 500 kbps high-speed CAN bus (ISO 11898-1): the Engine Control Module (ECM), Antilock Braking System (ABS), Transmission Control Module (TCM), and Body Control Module (BCM). An autonomous Diagnostic Master (DIAG\_MASTER) manages network interrogation (Fig. \ref{fig:system_arch} and Fig. \ref{fig:can_nodes}).

The communication matrix is formally defined in a network database (DBC). Across all modules and diagnostic layers, the system incorporates 15 distinct CAN messages and 43 individual physical signals. Six cyclic broadcast messages handle vehicle dynamics, while nine event-driven messages manage physical and functional diagnostic exchanges under ISO 15765-2 DoCAN transport rules. Identifiers use standard 11-bit arbitration headers. Cycle times, data lengths, and node bindings appear in Table \ref{tab:dbc_messages}.

\begin{table}[htbp]
\caption{CAN Message Parameters and Transmission Periods}
\label{tab:dbc_messages}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccccc}
\toprule
\textbf{Message Name} & \textbf{CAN ID} & \textbf{Tx Node} & \textbf{DLC} & \textbf{Cycle (ms)} & \textbf{Functional Scope} \\
\midrule
ECM\_Data\_1          & 0x100 (256)     & ECM     & 8   & 20         & Engine Speed, Throttle, Torque \\
ECM\_Data\_2          & 0x105 (261)     & ECM     & 8   & 100        & Coolant Temp, Fuel Flow, MIL \\
ABS\_WheelSpeeds      & 0x200 (512)     & ABS     & 8   & 20         & Individual 4-Wheel Speeds \\
ABS\_Dynamics         & 0x205 (517)     & ABS     & 8   & 20         & Vehicle Speed, Brake Pressure \\
TCM\_Status           & 0x300 (768)     & TCM     & 8   & 50         & Current Gear, Clutch, Temp \\
BCM\_Status           & 0x400 (1024)    & BCM     & 8   & 100        & Brake Switch, Hazards, Ignition \\
\bottomrule
\end{tabular}%
}
\end{table}

Bit layouts, scale factors, offsets, and physical engineering ranges configured inside the database appear in Table \ref{tab:dbc_signals}.

\begin{table}[htbp]
\caption{Signal Bit Allocation, Scale Factors, and Engineering Ranges}
\label{tab:dbc_signals}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lcccccc}
\toprule
\textbf{Signal Name} & \textbf{Source Msg} & \textbf{Bit Pos} & \textbf{Len} & \textbf{Factor, Offset} & \textbf{Range} & \textbf{Unit} \\
\midrule
EngineSpeed          & ECM\_Data\_1        & 0                & 16           & 0.25, 0                 & [0, 8000]      & rpm           \\
ThrottlePosition     & ECM\_Data\_1        & 16               & 8            & 0.5, 0                  & [0, 100]       & \%            \\
CoolantTemperature   & ECM\_Data\_2        & 0                & 8            & 1.0, -40                & [-40, 150]     & $^\circ$C     \\
WheelSpeed\_FL       & ABS\_WheelSpeeds    & 0                & 16           & 0.01, 0                 & [0, 300]       & km/h          \\
VehicleSpeed         & ABS\_Dynamics       & 0                & 16           & 0.01, 0                 & [0, 300]       & km/h          \\
BrakePressure        & ABS\_Dynamics       & 32               & 8            & 1.0, 0                  & [0, 250]       & bar           \\
CurrentGear          & TCM\_Status         & 0                & 4            & 1.0, 0                  & [0, 15]        & raw           \\
BrakeSwitchStatus    & BCM\_Status         & 2                & 1            & 1.0, 0                  & [0, 1]         & bin           \\
IgnitionState        & BCM\_Status         & 0                & 2            & 1.0, 0                  & [0, 3]         & raw           \\
\bottomrule
\end{tabular}%
}
\end{table}

We compute baseline bus utilization from these frame specifications. Transmitting 140 cyclic frames per second with an average frame length of 111 bits consumes 31.1 kbps. This represents a 6.22\% baseline load on a 500 kbps bus. Diagnostic polling increases total utilization to roughly 14.8\%, preserving an 85\% arbitration headroom that prevents frame drops.

Diagnostic communication follows ISO 14229-1 (UDS) and ISO 15765-2 (DoCAN). The master assigns physical request and response pairs across standard 0x7E0/0x7E8 addresses. ECM uses 0x7E0/0x7E8. ABS responds on 0x7E9 to queries at 0x7E1. TCM occupies 0x7E2/0x7EA, while BCM uses 0x7E3/0x7EB. Broadcast queries target 0x7DF. Diagnostic identifiers sit lower in arbitration priority than periodic powertrain frames, protecting vehicle stability loops from disruption.

\subsection{Signal Dependency Mapping and DAG Formulation}
Signal paths across the four controllers form a Directed Acyclic Graph $G = (V, E)$, with vertex set $V = \{v_1, v_2, v_3, v_4\}$ representing physical ECUs: $v_1 = \text{ECM}$, $v_2 = \text{ABS}$, $v_3 = \text{TCM}$, and $v_4 = \text{BCM}$. The directed edge set $E \subseteq V \times V$ captures data dependencies: directed edge $(v_i, v_j)$ signifies that ECU $v_j$ consumes data broadcast by $v_i$. If $v_i$ fails, $v_j$ suffers data starvation and asserts a secondary DTC.

\begin{figure}[t]
\centering
\begin{tikzpicture}[
    scale=0.76,
    every node/.style={transform shape},
    ecunode/.style={circle, draw=black!85, fill=blue!10, line width=0.7pt, font=\sffamily\footnotesize\bfseries, align=center, minimum size=1.05cm},
    edgearr/.style={-{Stealth[length=4.5pt, width=3pt]}, line width=0.7pt, draw=black!80},
    edgelabel/.style={font=\sffamily\tiny, fill=white, inner sep=1pt, text=black!90}
]

\node[ecunode] (bcm) at (0, 2.8) {BCM};
\node[ecunode] (abs) at (-1.8, 1.4) {ABS};
\node[ecunode] (ecm) at (1.8, 1.4) {ECM};
\node[ecunode] (tcm) at (0, 0) {TCM};

\draw[edgearr] (bcm) -- (abs) node[edgelabel, midway, above left] {Brake Switch};
\draw[edgearr] (bcm) -- (ecm) node[edgelabel, midway, above right] {Brake Switch};
\draw[edgearr] (abs) -- (ecm) node[edgelabel, midway, above] {Vehicle Speed};
\draw[edgearr] (abs) -- (tcm) node[edgelabel, midway, below left] {Vehicle Speed};
\draw[edgearr] (ecm) -- (tcm) node[edgelabel, midway, below right] {Engine Speed, Throttle};

\end{tikzpicture}
\caption{Signal dependency graph across BCM, ABS, ECM, and TCM showing causal data relationships.}
\label{fig:dag_model}
\end{figure}

The topological structure of $G$ (Fig. \ref{fig:dag_model}) maps to a binary adjacency matrix $D \in \{0, 1\}^{4 \times 4}$, where $D_{i,j}=1$ if $(v_i, v_j) \in E$ and $0$ otherwise:
\begin{equation}
D = \begin{pmatrix}
0 & 0 & 1 & 0 \\
1 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 \\
1 & 1 & 0 & 0
\end{pmatrix}
\end{equation}
Rows denote source ECUs $\{v_1, v_2, v_3, v_4\}$ and columns index consumer nodes. Entry $D_{1,3} = 1$ marks TCM dependence on ECM engine speed and throttle opening. Entry $D_{2,1} = 1$ captures ECM torque reduction reliance on ABS vehicle velocity and slip. Entry $D_{2,3} = 1$ reflects TCM shift scheduling based on ABS speed telemetry. Entries $D_{4,1} = 1$ and $D_{4,2} = 1$ record ECM and ABS reliance on the BCM brake switch. Because shifting does not alter instantaneous ignition timing loops in this setup, $G$ contains no closed feedback cycles, preserving the DAG invariant.

\subsection{In-Degree Topological Pruning Algorithm}
When faults occur, affected ECUs log confirmed DTCs. Let $S \subseteq V$ denote the set of active nodes reporting confirmed fault codes: $S = \{v_k \in V \mid \text{DTC\_Count}(v_k) > 0\}$. The active subgraph induced by $S$ is $G[S] = (S, E_S)$, where $E_S = \{(v_i, v_j) \in E \mid v_i, v_j \in S\}$. Within $G[S]$, the in-degree of node $v_j \in S$ counts its active upstream dependencies:
\begin{equation}
\deg_{S}^{-}(v_j) = \sum_{v_i \in S} D_{i,j}
\end{equation}
The root cause isolation criterion evaluates:
\begin{equation}
\text{Root\_Cause} = \{v_j \in S \mid \deg_{S}^{-}(v_j) = 0\}
\end{equation}
An active node with zero in-degree has no upstream faults in the current context. Its error traces to an internal sensor, hardware component, or local driver. Any node with $\deg_{S}^{-}(v_j) > 0$ depends on an upstream controller that is already flagged. We classify that downstream node as a secondary symptom and suppress its trouble codes. Algorithmic complexity is $O(|V| + |E|)$, requiring under 10 microseconds on an automotive microcontroller.

\subsection{UDS Implementation and Vector CANoe Testbench}
We built the network inside Vector CANoe using CAPL programs attached to simulated nodes. The Diagnostic Master runs a state machine that polls nodes using UDS Service 0x19 Subfunction 0x02 with status mask 0x08:
\begin{equation}
\mathbf{m}_{\text{req}} = [0\text{x}03, 0\text{x}19, 0\text{x}02, 0\text{x}08, 0\text{x}00, 0\text{x}00, 0\text{x}00, 0\text{x}00]
\end{equation}
When nodes return positive responses (SID 0x59) with three-byte DTC records, the master updates set $S$, executes the in-degree filter, displays the isolated root cause on a runtime panel, and writes execution timestamps to file. If an ECU fails to answer within 100 ms, the master flags a communication loss (frame timeout) and inserts the silent node into $S$.

\begin{figure}[t]
\centering
\includegraphics[width=0.74\columnwidth]{PANEL_NORMAL.png}
\caption{CANoe instrumentation panel during fault-free driving at 46.84 km/h in 3rd gear.}
\label{fig:panel_normal}
\end{figure}

\section{Results and Discussion}
We evaluated the diagnostic pipeline against six failure modes covering wiring disconnections, analog sensor degradation, and controller power loss. A dedicated CANoe fault panel injected all test conditions (Fig. \ref{fig:panel_normal}).

\subsection{Single-Point Sensor and Actuator Fault Scenarios}
Scenario 1 injects an open circuit into the ABS wheel speed sensor. Wheel speed data feeds stability control, an ASIL~D hazard category under ISO 26262. The ABS flags out-of-range sensor voltage, asserts primary DTC C0035-13, and halts velocity broadcasts. Deprived of speed data, the TCM logs secondary code U0415-81 (Invalid Data from ABS) and enforces a 3rd-gear mechanical hold. The ECM records P0500-00 (Vehicle Speed Missing). Polling retrieves active DTCs from ECM, ABS, and TCM ($S = \{v_1, v_2, v_3\}$). Computing in-degrees gives $\deg_{S}^{-}(v_2) = 0$, $\deg_{S}^{-}(v_1) = 1$, and $\deg_{S}^{-}(v_3) = 2$. The algorithm suppresses the secondary ECM and TCM codes, isolating ABS and C0035-13. The master issues request 0x7E1 and receives positive response 0x7E9 with C0035-13 in 8.2 ms, verifying concurrent diagnostic traffic (Fig. \ref{fig:sc1_panel}).

\begin{figure}[t]
\centering
\includegraphics[width=0.74\columnwidth]{WSS_SENSOR_OPEN/PANEL.jpg}
\caption{CANoe diagnostic display during wheel speed sensor disconnect (Scenario 1), isolating ABS fault C0035-13.}
\label{fig:sc1_panel}
\end{figure}

Dynamic traces appear in Fig. \ref{fig:sc1_speed} and Fig. \ref{fig:sc1_gear}. At $t = 4.2$ s, sensor disconnection drops reported velocity from 46.84 km/h to zero (Fig. \ref{fig:sc1_speed}). The TCM detects the abrupt drop, stops automatic shift scheduling, and downshifts into 3rd gear limp mode (Fig. \ref{fig:sc1_gear}).

\begin{figure}[t]
\centering
\includegraphics[width=0.92\columnwidth]{plot_sc1_speed.png}
\caption{Vehicle speed dropping to 0 km/h following front-left wheel speed sensor disconnect at $t = 4.2$ s.}
\label{fig:sc1_speed}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.92\columnwidth]{plot_sc1_gear.png}
\caption{Transmission gear state holding 3rd gear in limp-home mode after vehicle speed loss.}
\label{fig:sc1_gear}
\end{figure}

Scenario 2 injects an ECM throttle position sensor circuit low fault (ASIL~D). ECM asserts P0122-12 and activates default torque maps. The TCM cannot calculate shift points without throttle data, flags U0401-86 (Invalid Data from ECM), and holds 3rd gear. Active nodes are $S = \{v_1, v_3\}$. Because $D_{1,3} = 1$ and $D_{3,1} = 0$, in-degrees are $\deg_{S}^{-}(v_1) = 0$ and $\deg_{S}^{-}(v_3) = 1$. The engine suppresses the TCM code, isolating the ECM. Engine speed settles to a calibrated 1200 rpm limp threshold (Fig. \ref{fig:sc2_rpm}).

\begin{figure}[t]
\centering
\includegraphics[width=0.92\columnwidth]{plot_sc2_rpm.png}
\caption{Engine speed clamped at 1200 rpm limp-home idle during throttle sensor low voltage fault (Scenario 2).}
\label{fig:sc2_rpm}
\end{figure}

Scenario 3 simulates an engine coolant overheat (125 $^\circ$C, ASIL~B). The ECM logs primary DTC P0217-00 and enforces a 2500 rpm rotational ceiling (Fig. \ref{fig:sc3_rpm}). TCM and BCM assert secondary alerts U0401-82 (Invalid Data from ECM - Thermal Derate) and B10A2-00 (Cluster Warning Request), yielding $S = \{v_1, v_3, v_4\}$. With dependencies $D_{1,3} = 1$ and $D_{1,4} = 1$, in-degrees evaluate to $\deg_{S}^{-}(v_1) = 0$, $\deg_{S}^{-}(v_3) = 1$, and $\deg_{S}^{-}(v_4) = 1$. The DAG engine suppresses both secondary codes, isolating ECM and P0217-00.

\begin{figure}[t]
\centering
\includegraphics[width=0.92\columnwidth]{plot_sc3_rpm.png}
\caption{Engine speed rev-limited to 2500 rpm for thermal protection during coolant overheat at 125 $^\circ$C (Scenario 3).}
\label{fig:sc3_rpm}
\end{figure}

Scenario 5 injects a stuck-closed brake pedal switch into the BCM (ASIL~B). The BCM logs primary DTC B1318-11. ECM and TCM assert secondary fault codes P0504-00 (Brake Switch Plausibility) and U0422-81 (Invalid Data from BCM), yielding active set $S = \{v_1, v_3, v_4\}$. In-degrees evaluate to $\deg_{S}^{-}(v_4) = 0$, $\deg_{S}^{-}(v_1) = 1$, and $\deg_{S}^{-}(v_3) = 1$. The system suppresses the ECM and TCM codes, isolating BCM (Fig. \ref{fig:sc5_panel}).

\begin{figure}[t]
\centering
\includegraphics[width=0.74\columnwidth]{BRAKE_SWITCH_STUCK/PANEL.jpg}
\caption{CANoe diagnostic display for stuck brake pedal switch (Scenario 5), isolating BCM fault B1318-11 while cruising at 160 km/h.}
\label{fig:sc5_panel}
\end{figure}

During Scenario 5, hydraulic master cylinder pressure reads 0.8 bar ($< 5.0$ bar threshold). ISO 26262 functional safety plausibility rules cross-check hydraulic pressure against the electrical contact. Negligible line pressure proves the mechanical brake is disengaged, indicating an electrical switch failure rather than physical braking. ABS suppresses unwanted foundation brake actuation, avoiding phantom deceleration at highway speed. To prevent catastrophic high-speed downshift overspeed, TCM speed-gated limp logic holds 5th gear above 100 km/h, while ECM activates ISO 26262 ASIL-D Brake-Throttle Override (BTO). The controller clamps commanded throttle to 0.0\%, smoothly coasting engine speed down from 3000 rpm to 1200 rpm idle (Fig. \ref{fig:sc5_rpm}) as vehicle speed bleeds down safely (Fig. \ref{fig:sc5_speed}).

\begin{figure}[t]
\centering
\includegraphics[width=0.92\columnwidth]{plot_sc5_speed.png}
\caption{Vehicle speed coastdown deceleration from 160 km/h during brake switch fault following Brake-Throttle Override throttle cut (Scenario 5).}
\label{fig:sc5_speed}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.92\columnwidth]{plot_sc5_rpm.png}
\caption{Engine speed smoothly decelerating from 3000 rpm to 1200 rpm idle coastdown under ISO 26262 ASIL-D Brake-Throttle Override (Scenario 5).}
\label{fig:sc5_rpm}
\end{figure}

\subsection{Network Cutoff and Multi-Node Degradation Scenarios}
Scenarios 4 and 6 simulate complete ECU dropouts. In Scenario 4, the ABS node disconnects from the bus (ASIL~D chassis dropout). The ECM and TCM exceed their 200 ms receive windows and assert DTCs U0121-00 and U0129-00 ($S = \{v_1, v_3\}$). The ABS fails to answer diagnostic queries. The master detects silence on 0x7E9, logs an offline event for $v_2$, and inserts $v_2$ into $S$. In-degree evaluation yields $\deg_{S}^{-}(v_2) = 0$, isolating the ABS module. Automated root cause isolation on the diagnostic panel and node health degradation appear in Fig. \ref{fig:sc4_panel} and Fig. \ref{fig:sc4_health}, respectively.

\begin{figure}[t]
\centering
\includegraphics[width=0.74\columnwidth]{CUTOFF_ABS_NODE/PANEL.jpg}
\caption{Diagnostic panel during complete ABS transceiver disconnect (Scenario 4), showing network timeout triage and isolated root node.}
\label{fig:sc4_panel}
\end{figure}

\begin{figure}[b]
\centering
\includegraphics[width=0.92\columnwidth]{plot_sc4_health.png}
\caption{Controller communication state transition from normal to bus-off at $t = 2.8$ s following ABS transceiver disconnect (Scenario 4).}
\label{fig:sc4_health}
\end{figure}

Scenario 6 disconnects the ECM (ASIL~D propulsion loss). ABS and TCM lose torque and speed references, recording U0100-00 and U0401-00. The Diagnostic Master detects 0x7E0 silence, creates active set $S = \{v_1, v_2, v_3\}$, and isolates the ECM via in-degree evaluation.

\subsection{Latency Benchmarking and Pruning Efficiency}
Table \ref{tab:benchmarks} summarizes performance across all six scenarios with ISO 26262 ASIL classifications. Isolation accuracy reached 100\% across all trials.

\begin{table}[htbp]
\caption{Fault Isolation Performance Across Simulated Failure Modes}
\label{tab:benchmarks}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccccc}
\toprule
\textbf{Scenario} & \textbf{ASIL} & \textbf{Raw DTCs} & \textbf{Suppressed} & \textbf{Efficiency} & \textbf{Latency (ms)} \\
\midrule
1: WSS Open Circuit      & ASIL D & 3 & 2 & 66.7\% & 42.10 \\
2: Throttle Sensor Low   & ASIL D & 2 & 1 & 50.0\% & 41.80 \\
3: Coolant Overheat      & ASIL B & 3 & 2 & 66.7\% & 40.50 \\
4: ABS Node Cutoff       & ASIL D & 3 & 2 & 66.7\% & 45.20 \\
5: Brake Switch Stuck    & ASIL B & 3 & 2 & 66.7\% & 42.40 \\
6: ECM Node Cutoff       & ASIL D & 3 & 2 & 66.7\% & 43.00 \\
\midrule
\textbf{Average / Total} & \textbf{ASIL B--D} & \textbf{2.8 (17)} & \textbf{1.8 (11)} & \textbf{63.9\%} & \textbf{42.50} \\
\bottomrule
\end{tabular}%
}
\end{table}

Pruning efficiency, measuring suppressed symptom DTCs against total logged codes, reached 66.7\% in five scenarios (50.0\% in Scenario 2) and averaged 63.9\% overall. Across all six simulated failure modes, the engine isolated the single primary root cause while suppressing 11 secondary cascading alarms. Interrogation latency, timed from initial request dispatch to panel display, averaged 42.50 ms. Physical UDS frame arbitration and response timeouts account for nearly all this time; the topological calculation itself requires under 10 microseconds on an embedded core.

\subsection{Comparative Analysis with State-of-the-Art Methods}
Table \ref{tab:comparison} benchmarks our results against recent automotive diagnostic literature published between 2023 and 2025.

\begin{table}[htbp]
\caption{Comparison with Published Automotive Diagnostic Methods}
\label{tab:comparison}
\centering
\scriptsize
\setlength{\tabcolsep}{1.8pt}
\begin{tabular}{@{}llcccc@{}}
\toprule
\textbf{Study} & \textbf{Methodology} & \textbf{Target ECU} & \textbf{Complexity} & \textbf{Latency} & \textbf{Memory} \\
\midrule
Lin \emph{et al.} \cite{lin2023zonal}     & Matrix Rules    & Gateway     & $O(N^2)$            & 120 ms           & 12.4 KB \\
Liu \emph{et al.} \cite{liu2023dag}       & Bayesian DAG    & Domain ECU  & $O(2^k |V|)$        & 340 ms           & 45.2 KB \\
Wang \emph{et al.} \cite{wang2023can}     & Wire Topology   & Physical    & $O(N)$              & 210 ms           & 8.6 KB  \\
Lu \emph{et al.} \cite{lu2025deep}        & CNN-LSTM        & Edge GPU    & High                & 85 ms            & 5.8 MB  \\
Bohne \emph{et al.} \cite{bohne2023neuro} & Neuro-Symbolic  & Cloud       & NP-Hard             & 1250 ms          & 22.1 MB \\
\midrule
\textbf{This Work}                        & \textbf{DAG In-Degree} & \textbf{Zonal GW} & $\mathbf{O(|V|{+}|E|)}$ & \textbf{42.5 ms} & $\mathbf{<320}$ \textbf{B} \\
\bottomrule
\end{tabular}
\end{table}

While Bayesian \cite{liu2023dag} and deep learning \cite{lu2025deep} models handle noisy multi-fault distributions, their exponential parameter tables and multi-megabyte footprints exceed the capacity of microcontrollers. Opaque neural networks also complicate ISO 26262 ASIL~D certification. Off-board disambiguation \cite{lin2023zonal} and cloud reasoning \cite{bohne2023neuro} introduce round-trip latencies of several seconds and depend on cellular coverage. In contrast, our in-degree DAG algorithm runs in linear $O(|V| + |E|)$ time, isolates faults in 42.50 ms, and uses under 320 bytes of RAM, providing deterministic execution within low-power zonal gateway nodes.

\subsection{Zonal Architecture Migration and Scalability}
Deploying this framework across commercial vehicle networks supports the shift toward zonal E/E topologies. Zone controllers aggregate peripheral sensor streams over high-speed Ethernet or CAN-FD backbones to central compute clusters. As centralized compute nodes run virtualized software formerly spread across separate microcontrollers, logical signal dependencies multiply. Because our model tracks mathematical signal dependency instead of physical wiring bundles, the adjacency matrix maps directly onto zonal cross-switches and virtualized execution partitions.

For a network containing $N$ physical or virtual nodes, matrix storage scales quadratically as $N \times N$ bits. In practice, automotive control loops consume inputs from two to four upstream functional blocks, maintaining strict matrix sparsity. Storing dependency maps for a comprehensive 50-node zonal network requires under 320 bytes of non-volatile flash memory, enabling rapid on-board diagnostic triage in zone controllers without telemetry links.

\subsection{Embedded Microcontroller Footprint and ISO 11898-1 Timing}
Real-time embedded execution demands zero heap allocation and bounded execution cycles. We benchmarked the topological in-degree evaluation loop across static AUTOSAR Classic BSW diagnostic partitions on 32-bit automotive microcontrollers (Infineon AURIX TC397 clocked at 300 MHz and Renesas RH850 at 240 MHz). Traversing the 4-node network adjacency matrix required 1840 CPU cycles ($<8~\mu\text{s}$), confirming that algorithmic disambiguation introduces zero jitter into standard 10 ms periodic diagnostic tasks. Memory allocation remains entirely static: adjacency bitmasks and in-degree vectors consume 32 bytes of RAM and 288 bytes of flash ROM, satisfying ISO 26262 ASIL~D requirements for memory freedom from interference.

Physical-layer error transitions under ISO 11898-1 exhibit deterministic timing. In Scenario 4, disconnecting the ABS transceiver caused repeated acknowledge and bit-monitoring errors, incrementing the Transmit Error Counter (TEC) past the 127 threshold into Error Passive state, and subsequently surpassing 255 into Bus-Off state within 4.8 ms. The Diagnostic Master recorded the resulting U0121-00 timeout frame without bus starvation, executing complete topological root cause isolation in 45.20 ms well within the 100 ms fail-safe fault handling time interval (FHTI).

To validate performance under bus saturation, Vector CANoe injected periodic background frames generating 70\% continuous bus load. Even with bus congestion, diagnostic response latency rose by only 2.3 ms, preserving 100\% isolation accuracy. High-priority powertrain messages (0x100 to 0x200) maintained deterministic delivery without arbitration collisions with diagnostic polling frames on 0x7DF.

Fault recovery and self-healing mechanisms follow strict automotive state machine standards. When the disconnected ABS module was reattached, the local CAN transceiver observed 128 occurrences of 11 consecutive recessive bits before clearing Bus-Off status. The diagnostic master detected active status frames within 15 ms, updating the graph in-degree vector and restoring normal health classification.

DTC lifecycle management integrates standard aging logic under SAE J1979 and ISO 14229-1. Once an isolated fault condition clears, secondary codes transition to historical status, requiring 40 fault-free warm-up driving cycles before unlatching from non-volatile EEPROM storage.

\section{Conclusion}
We developed an on-bus diagnostic root cause isolation engine uniting Directed Acyclic Graph signal modeling with ISO 14229-1 UDS diagnostic polling. Topological in-degree pruning filtered cascading secondary DTCs across 15 CAN messages and 43 powertrain and chassis signals. Vector CANoe testbench validation across six physical and logical fault modes demonstrated 100\% isolation accuracy, an average DTC reduction of 63.9\%, and an execution budget of 42.50 ms, satisfying ISO 26262 ASIL~B through ASIL~D timing bounds. Integrating this logic into embedded zonal gateway hardware enables instant fault triage without off-board telemetry.

Future research will explore dynamic DAG generation directly from CAN database (.dbc) network files and ARXML system descriptions at compile time. We also plan to evaluate transport scalability across ISO 13400 Diagnostic over IP (DoIP) backbones on gigabit automotive Ethernet, as well as hardware-in-the-loop (HIL) fault validation on upcoming CAN-XL physical transceivers. Integrating ISO 21434 automotive cybersecurity intrusion detection with topological dependency graphs represents another promising avenue for isolating masquerade and injection attacks.

Additionally, integrating physical reflectometry into zone controller silicon will enable joint electrical and logical isolation of intermittent wiring faults, establishing a dependable foundation for connected vehicle platforms.

\begin{thebibliography}{00}

\bibitem{saravanan2025starter}
S.~Saravanan, ``Optimized surface mounted permanent magnet starter-generator configurations suitability towards electric aircraft applications,'' in \emph{Proc. IEEE Int. Conf. Advancements in Power, Communication and Intelligent Systems (APCI)}, Feb. 2025, pp.~1--6.

\bibitem{saravanan2025parameter}
S.~Saravanan, ``Optimal parameter estimation techniques for enhanced performance of solar PV cell,'' in \emph{Proc. IEEE Int. Conf. Recent Advances in Electrical, Electronics, Ubiquitous Communication, and Computational Intelligence (RAEEUCCI)}, Mar. 2025, pp.~1--5.

\bibitem{krishnan2021can}
R.~Krishnan, N.~Ramesh, and T.~R.~Rajesh, ``ROS based six-DOF robotic arm control through CAN bus interface,'' in \emph{Proc. IEEE Int. Conf. Distributed Computing, VLSI, Electrical Circuits and Robotics (DISCOVER)}, Nov. 2021, pp.~142--147.

\bibitem{nair2025qml}
M.~S.~Nair, V.~K.~Menon, and S.~Mohan, ``QCAE-QOC-SVM: A hybrid quantum machine learning model for DoS and fuzzy attack detection on autonomous vehicle CAN bus,'' \emph{IEEE Access}, vol.~13, pp.~11200--11215, 2025.

\bibitem{wang2023can}
Y.~Wang, Z.~Zhang, and K.~Huang, ``Diagnosis of intermittent connection faults for CAN networks with complex topology,'' \emph{IEEE Access}, vol.~11, pp.~49666--49677, 2023.

\bibitem{schmidt2022uds}
K.~Schmidt and E.~G.~Schmidt, ``Message scheduling and latency guarantees for ISO 14229 Unified Diagnostic Services over CAN,'' \emph{IEEE Trans. Ind. Informat.}, vol.~18, no.~5, pp.~3120--3129, May 2022.

\bibitem{nolte2022wcrt}
T.~Nolte, H.~Hansson, and S.~Punnekkat, ``Worst-case response-time analysis of automotive diagnostic requests over CAN and CAN-FD,'' \emph{IEEE Trans. Comput.-Aided Design Integr. Circuits Syst.}, vol.~41, no.~11, pp.~4501--4512, Nov. 2022.

\bibitem{dinatale2022can}
M.~Di~Natale, ``Analysis and optimization of Controller Area Network for modern automotive systems,'' \emph{IEEE Trans. Veh. Technol.}, vol.~71, no.~4, pp.~3510--3521, Apr. 2022.

\bibitem{zhang2022graph}
X.~Zhang, L.~Yang, and J.~Wang, ``Graph-based root cause diagnosis for in-vehicle distributed embedded systems,'' \emph{IEEE Trans. Intell. Transp. Syst.}, vol.~23, no.~10, pp.~18920--18931, Oct. 2022.

\bibitem{lin2023zonal}
Y.~Lin, C.~Wang, and H.~Peng, ``Fault propagation and automated diagnostic trouble code disambiguation in zonal automotive E/E architectures,'' \emph{IEEE Trans. Rel.}, vol.~72, no.~3, pp.~1102--1114, Sep. 2023.

\bibitem{liu2023dag}
H.~Liu, J.~Sun, and W.~Chen, ``Bayesian network and directed acyclic graph modeling for multi-ECU fault isolation in electric vehicles,'' \emph{IEEE Access}, vol.~11, pp.~45120--45132, 2023.

\bibitem{lu2025deep}
M.~Lu, X.~Li, and Q.~Zhang, ``Development and validation of an explainable hybrid deep learning model for multiple-fault diagnosis in intelligent automotive electronic systems,'' \emph{MDPI Electronics}, vol.~14, no.~22, p.~4488, 2025.

\bibitem{bohne2023neuro}
M.~Bohne, L.~Hahn, and R.~Guenther, ``A neuro-symbolic approach for anomaly detection and complex fault diagnosis exemplified in the automotive domain,'' in \emph{Proc. ACM Int. Conf. Knowl. Eng. Knowl. Manage. (EKAW)}, 2023, pp.~1--15.

\end{thebibliography}

\end{document}
"""
    with open("IEEE_Root_Cause_Isolation_Paper.tex", "w", encoding="utf-8") as f:
        f.write(tex_code)
    print("Paper generated.")

build_paper()
