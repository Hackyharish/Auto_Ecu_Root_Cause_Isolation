# IN-VEHICLE NETWORKING (IVN) CAPSTONE PROJECT
## EVALUATION & PRESENTATION DEFENSE GUIDE

**Project Title**: Automated Root Cause Isolation in Multi-ECU Networks via Directed Acyclic Graphs  
**Candidate**: Harish R (Reg. No: CB.EN.U4EEE23112)  
**Program**: B.Tech Electrical & Electronics Engineering (Sem 7)  
**Industry Partner**: Tata Technologies TechPulse Collaboration  
**Scheduled Slot**: 10:30 AM – 11:15 AM (Total: 45 Minutes)  
**Mandatory Venue Arrival**: **10:15 AM** (Strictly 15 minutes before session start)

---

## 1. SESSION SCHEDULE & TIMING ARCHITECTURE

```
+---------------------------------------------------------------------------------------+
| 10:15 AM - 10:30 AM | PRE-SESSION SETUP & HARDWARE/SOFTWARE READINESS (15 min)        |
+---------------------------------------------------------------------------------------+
| 10:30 AM - 10:31 AM | SLIDE 1: Title, Credentials & ISO Standards Context (1 min)     |
| 10:31 AM - 10:34 AM | SLIDE 2: Problem Statement, Alarm Floods & Objectives (3 min)   |
| 10:34 AM - 10:37 AM | SLIDE 3: System Architecture & Multi-Layer Design (3 min)       |
| 10:37 AM - 10:40 AM | SLIDE 4: Node, Message & Signal Structure (15 msg/43 sig) (3 min)|
| 10:40 AM - 10:44 AM | SLIDE 5: Implementation: DAG Pruning Algorithm & Math (4 min)   |
| 10:44 AM - 10:47 AM | SLIDE 6: Vector CANoe 16.0 Simulation & Diagnostics Panel (3 min)|
| 10:47 AM - 10:51 AM | SLIDE 7: Solution Demonstration across 6 Failure Modes (4 min)  |
| 10:51 AM - 10:59 AM | SLIDE 8: Video Demonstration & Live CANoe Execution (8 min)     |
| 10:59 AM - 11:02 AM | SLIDE 9: Quantitative Results & State-of-the-Art Benchmark (3 min)|
| 11:02 AM - 11:05 AM | SLIDE 10: Key Learnings, Zonal Scalability & Conclusion (3 min) |
+---------------------------------------------------------------------------------------+
| 11:05 AM - 11:15 AM | EVALUATOR Q&A AND TECHNICAL INTERACTION (EXACTLY 10 MIN)        |
+---------------------------------------------------------------------------------------+
```

---

## 2. PRE-SESSION READINESS CHECKLIST (AT 10:15 AM)

Before the evaluators arrive, execute this checklist step-by-step:

### A. Laptop & Display Output
- [ ] Connect HDMI / USB-C to venue projector. Set display to **Duplicate** (`Win + P` $\to$ Duplicate) at native $1920 \times 1080$ resolution.
- [ ] Verify audio output through projector/PA system for video playback.
- [ ] Connect AC power adapter (do not run on battery power to prevent power throttling during CANoe execution).
- [ ] Disable Windows notifications (`Focus Assist` / `Do Not Disturb` $\to$ ON).

### B. Software & Project Files Setup
1. **Presentation Deck**:
   - Open `Presentation/Project_Presentation.pdf` in Adobe Acrobat / SumatraPDF in **Full Screen Mode** (`Ctrl + L`).
   - Verify page count is exactly **10 slides**.
2. **Demonstration Video**:
   - Open `CB.EN.U4EEE23112_IVN_VIDEO.mp4` in VLC Media Player / MPC-HC.
   - Pause at `00:00`, keep window minimized on taskbar.
   - Test seek shortcuts (Space for pause/resume, left/right arrows for 5s seek).
3. **Vector CANoe 16.0 Environment**:
   - Launch Vector CANoe 16.0.
   - Load configuration: `CANoe_Simulation/AUTOMOTIVE_NETWORK_SIMULATION.cfg`.
   - Verify CAN database `CAN_Communication_Network.dbc` is loaded without unresolved symbol warnings.
   - Open Diagnostic Master Panel (`PANEL_NORMAL.xvp`).
   - Check CAPL compilation: Press `F9` in CAPL browser $\to$ `0 Errors, 0 Warnings`.
   - Start simulation (`F9` in CANoe) once to verify 500 kbps bus activity and 0 bus-off conditions, then press `F9` to pause/stop ready for live demo.

### C. Backup Redundancy Plan
- [ ] **Backup Copy 1**: USB Flash Drive mounted at root containing:
  - `Project_Presentation.pdf`
  - `CB.EN.U4EEE23112_IVN_VIDEO.mp4`
  - Full project folder `Project/`
- [ ] **Backup Copy 2**: Secondary local drive partition (`C:\Backup_IVN_Project\`).
- [ ] **Paper Copy**: 1 printed copy of the IEEE paper `IEEE_Root_Cause_Isolation_Paper.pdf` placed on evaluator table.

---

## 3. SLIDE-BY-SLIDE PRESENTATION SCRIPT (35 MINUTES)

### SLIDE 1: Title, Credentials & ISO Standards Context (Time: 10:30 – 10:31 | 1 min)
* **What to Show**: Slide 1 Title card displaying project credentials, Tata Technologies TechPulse badge, and automotive regulatory frameworks.
* **Verbal Script**:
  > "Respected evaluators, good morning. I am Harish R, final year student of Electrical and Electronics Engineering, registration CB.EN.U4EEE23112. Today, in collaboration with the Tata Technologies TechPulse initiative, I present our capstone project: **Automated Root Cause Isolation in Multi-ECU In-Vehicle Networks using Directed Acyclic Graphs**.
  >
  > In modern vehicles operating under ISO 26262 ASIL D functional safety mandates, AUTOSAR Classic architectures, and ISO 14229 Unified Diagnostic Services, electronic control units are heavily cross-coupled over high-speed CAN networks. When a single component fails, it triggers an avalanche of downstream diagnostic trouble codes across healthy ECUs. Today, I will demonstrate how we solve this fundamental problem using deterministic, graph-theoretic causality pruning with zero machine learning overhead, implemented and validated in Vector CANoe 16.0."

---

### SLIDE 2: Problem Statement & Research Objectives (Time: 10:31 – 10:34 | 3 min)
* **What to Show**: Slide 2 highlighting cascading alarm floods, warranty misdiagnosis statistics, and four concrete research objectives.
* **Verbal Script**:
  > "Let us examine why this problem is critical for automotive OEMs today.
  >
  > In modern vehicles, a primary fault—for instance, a Wheel Speed Sensor harness failure—does not remain localized to the ABS controller. Because the Engine Control Module relies on vehicle speed for torque management, the Transmission Control Module needs it for gear-shift schedules, and the Body Control Module needs it for chassis stability, all four ECUs simultaneously detect signal loss and flag DTCs.
  >
  > This results in an **alarm flood** of 5 to 8 simultaneous DTCs within a single 100 ms diagnostic window. Standard workshop scan tools simply dump these DTCs without causality information. This leads to three severe consequences:
  > 1. **Warranty Misdiagnosis & High NTF (No Trouble Found) Rates**: Up to 40% of ECUs replaced in service bays are completely healthy; technicians replace secondary victims because their DTCs appeared first or had higher priority.
  > 2. **ISO 26262 ASIL D Safety Violations**: Faults cascade faster than human reaction times. During critical events like high-speed braking at 160 km/h, the vehicle must rapidly isolate the primary actuator defect to execute appropriate limp-home mitigation.
  > 3. **High Diagnostic Latency**: Manual troubleshooting on OEM assembly lines and service bays escalates vehicle downtime and warranty reserves.
  >
  > To resolve this, we formulated four strict research objectives:
  > - **Objective 1**: Develop a deterministic in-vehicle root cause isolation algorithm executed within microcontrollers under strict AUTOSAR memory constraints.
  > - **Objective 2**: Formulate a Directed Acyclic Graph (DAG) dependency model mathematically mapping all signal, physical, and cross-ECU dependencies.
  > - **Objective 3**: Implement dynamic in-degree topological pruning that filters symptom DTCs and extracts the singleton primary fault in real time.
  > - **Objective 4**: Validate the architecture in Vector CANoe 16.0 across high-risk dynamic driving scenarios, achieving over 60% alarm reduction with deterministic execution latency under 50 ms."

---

### SLIDE 3: System Architecture & Multi-Layer Design (Time: 10:34 – 10:37 | 3 min)
* **What to Show**: Slide 3 detailed architecture block diagram: Fault Injection Layer, High-Speed CAN Bus (500 kbps), 4 Target ECUs, and Central Diagnostic Master.
* **Verbal Script**:
  > "Slide 3 illustrates the complete system architecture designed and validated in this project.
  >
  > The network operates on a High-Speed CAN physical layer at 500 kbps, 8-byte payload, using 11-bit standard identifiers in strict conformance with ISO 11898-2. We model four primary vehicle domains:
  > 1. **ABS / ESP ECU (0x100)**: Houses safety-critical signals including 4-wheel independent speeds, master cylinder brake pressure, yaw rate, and ABS active status.
  > 2. **ECM (Engine Control Module, 0x200)**: Controls throttle position, engine speed up to 6500 RPM, coolant temperature, fuel mass, and calculated torque.
  > 3. **TCM (Transmission Control Module, 0x300)**: Manages gear position (P-R-N-D-1-5), torque converter slip, and transmission fluid temperature.
  > 4. **BCM (Body Control Module, 0x400)**: Aggregates driver inputs including physical brake switch status, steering wheel angle, accelerator pedal position, and ambient sensors.
  >
  > Alongside these functional controllers, we introduce the **Central Diagnostic Master (0x700 / DIAG_TESTER)**. This node acts as an in-vehicle supervisory gateway. It executes three integrated modules:
  > - An **Active Signal Monitor** evaluating cyclic message timings, CRC checksums, and plausibility cross-checks.
  > - The **DAG Inference Engine**, which holds the pre-compiled dependency adjacency matrix.
  > - The **UDS & Alarm Suppression Controller**, which broadcasts ISO 14229 diagnostic suppression commands to prevent healthy nodes from logging spurious DTCs."

---

### SLIDE 4: Node, Message & Signal Structure (Time: 10:37 – 10:40 | 3 min)
* **What to Show**: Slide 4 DBC communication layout showing the exact 15 CAN messages, 43 signals, transmission periodicities, and priority arbitration hierarchy.
* **Verbal Script**:
  > "Slide 4 presents the exact communication layout implemented in our network database (`CAN_Communication_Network.dbc`).
  >
  > The bus carries **15 distinct CAN messages and 43 individual signals**. 
  >
  > Notice the CAN ID priority mapping:
  > - CAN ID `0x0A0` (`ABS_Status_01`) and `0x0B0` (`ABS_WheelSpeeds`) hold the highest priority arbitration on the bus with a 10 ms cycle time, reflecting their ASIL D classification.
  > - Powertrain messages like `0x1A0` (`ECM_TorqueControl`) and `0x1B0` (`ECM_EngineData`) follow at 20 ms.
  > - Transmission messages `0x2A0` (`TCM_GearInfo`) cycle at 20 ms.
  > - Chassis and body messages `0x3A0` (`BCM_DriverInputs`) cycle at 50 ms.
  > - Diagnostic physical request and response channels use `0x7DF` functional broadcast and `0x7E0–0x7E8` UDS addressing.
  >
  > Every signal is configured with explicit scale factors, offsets, and physical limits matching automotive production standards—for example, wheel speeds scale from 0 to 250 km/h with 0.1 km/h resolution, and brake pressure scales up to 250 bar."

---

### SLIDE 5: Implementation Methodology: DAG Pruning Algorithm (Time: 10:40 – 10:44 | 4 min)
* **What to Show**: Slide 5 mathematical formulation: Graph definition, adjacency matrix, active failure subgraph, in-degree pruning equation, and topological ordering.
* **Verbal Script**:
  > "Now, let us examine the mathematical core of our solution: the **Directed Acyclic Graph (DAG) Causality Pruning Algorithm**.
  >
  > We model the vehicle's functional network as a directed graph $G = (V, E)$, where each vertex $v_i \in V$ represents a diagnostic failure mode or signal anomaly, and each directed edge $e_{ij} = (v_i, v_j) \in E$ denotes that fault $v_i$ causally induces symptom $v_j$. Because physical causation is strictly unidirectional and acyclic, $G$ is guaranteed to be a DAG.
  >
  > When anomalies occur across the network, the Diagnostic Master forms the **Active Failure Subgraph** $G_F = (V_F, E_F)$, where $V_F$ contains all vertices whose detection status $s(v) = 1$.
  >
  > Within this active subgraph, the in-degree of any node $v$ is given by:
  > $$\deg_{G_F}^-(v) = \sum_{u \in V_F} A[u, v]$$
  > where $A[u, v]$ is the binary adjacency matrix.
  >
  > Here is the governing theorem of our approach:
  > **Theorem**: *The true root cause $v^*$ of a cascading fault event is an active failure node that has no active causal antecedents within the active subgraph.*
  > Mathematically, the root cause set is:
  > $$R = \{ v \in V_F \mid \deg_{G_F}^-(v) = 0 \}$$
  >
  > Any vertex with $\deg_{G_F}^-(v) \ge 1$ is an induced secondary symptom and is immediately suppressed.
  >
  > Why is this approach revolutionary for automotive ECUs?
  > 1. **Deterministic Execution**: It requires no matrix inversion, no gradient descent, and no stochastic iterations.
  > 2. **Linear Time Complexity**: The worst-case runtime is strictly $O(|V_F| + |E_F|)$. For our 15-node failure graph, execution completes in **42.5 microseconds** on a 32-bit automotive microcontroller (Renesas RH850 or Infineon AURIX TC3xx).
  > 3. **Minimal Memory Footprint**: The adjacency matrix and status bitmask occupy less than **320 bytes of RAM**, fitting comfortably into the most resource-constrained AUTOSAR Classic BSW stacks."

---

### SLIDE 6: Vector CANoe 16.0 Simulation & Diagnostics Panel (Time: 10:44 – 10:47 | 3 min)
* **What to Show**: Slide 6 showing the CANoe simulation environment, CAPL event architecture, and high-contrast graphical Diagnostic Panel.
* **Verbal Script**:
  > "Slide 6 shows our experimental validation environment built entirely within industry-standard **Vector CANoe 16.0**.
  >
  > We implemented the complete simulation stack:
  > - **CAPL Event Architecture**: Each ECU runs dedicated event-driven CAPL scripts (`on timer`, `on message`, `on sysvar`) executing real-time signal generation, fault injection hooks, and diagnostic handler loops.
  > - **Diagnostic Master Panel**: We engineered a custom high-contrast Vector panel displaying real-time vehicle instrumentation—speed gauge (0–200 km/h), RPM gauge (0–7000 RPM), throttle and brake sliders, active DTC monitors, and the live Root Cause Isolation readout.
  > - **Fault Injection Switchboard**: Allows deterministic injection of physical layer disruptions, sensor open-circuits, plausibility mismatches, and complete ECU power cutoffs at calibrated driving speeds."

---

### SLIDE 7: Solution Demonstration: Multi-Scenario Fault Isolation (Time: 10:47 – 10:51 | 4 min)
* **What to Show**: Slide 7 detailing the 6 validated failure modes with before-and-after alarm counts and isolation proof.
* **Verbal Script**:
  > "We subjected our DAG isolation algorithm to six safety-critical failure scenarios:
  >
  > - **Scenario 1: Front-Left Wheel Speed Sensor Open Circuit**: At 60 km/h cruising, the ABS controller detects wheel speed dropout. Healthy ECM, TCM, and BCM nodes immediately log speed plausibility DTCs (5 raw alarms). Our DAG isolates the ABS FL Sensor as root cause and suppresses the 4 downstream alerts in 41.2 ms.
  > - **Scenario 2: Brake Switch Stuck at High-Speed (160 km/h, 6500 RPM)**: This is an ISO 26262 ASIL D critical scenario. The brake switch electrical contacts weld shut while the vehicle is accelerating at wide-open throttle. Standard systems flag simultaneous engine torque cut, transmission shift-lock, and brake plausibility alarms (6 alarms). Our engine cross-checks the hydraulic master cylinder pressure ($P_{brake} = 0.8\text{ bar} < 5.0\text{ bar}$ threshold), proves the brake pedal is physically disengaged, isolates BCM Brake Switch Stuck, and suppresses 5 secondary alarms.
  > - **Scenario 3: Complete ABS Node Bus Cutoff**: Physical harness severance causes loss of cyclic heartbeat `0x0A0`. ECM, TCM, and BCM raise timeout DTCs `U0121` (7 alarms). The DAG algorithm detects that all missing signals originate from the ABS node, correctly identifying ABS ECU Node Failure in 46.8 ms.
  > - **Scenarios 4, 5, and 6**: Throttle Position Sensor plausibility mismatch, CAN Bus physical babbling idiot jabbering (bus load spikes to 70%), and Transmission Fluid Over-Temperature cascades.
  >
  > In all six scenarios, the algorithm achieved **100% true-positive root cause isolation accuracy**."

---

### SLIDE 8: Project Video Demonstration & Live CANoe Execution (Time: 10:51 – 10:59 | 8 min)
* **What to Show**: Slide 8 showing the playback link and scenario cues for `CB.EN.U4EEE23112_IVN_VIDEO.mp4` (12 min 45 sec).
* **Verbal Script & Video Playback Runbook**:
  > *"Evaluators, I will now transition to the live recorded demonstration in Vector CANoe 16.0, captured directly from our simulation testbed."*
  > 
  > *(Switch to video player or click the Beamer video hyperlink)*
  >
  > **Timestamp Navigation & Live Narration**:
  > - **00:00 – 02:15 [Baseline Cruising]**:
  >   > "Here we observe normal vehicle operation. Vehicle speed accelerates smoothly to 60 km/h, engine RPM tracks at 2400 RPM, CAN bus load is stable at 24.3%, and the Root Cause display reads 'SYSTEM NORMAL'."
  > - **02:15 – 04:30 [Scenario 1: WSS Open Circuit Injection]**:
  >   > "At 02:15, we trigger the Front-Left Wheel Speed Sensor open circuit. Notice the Trace window: five raw DTCs fire across ABS, ECM, TCM, and BCM. Within 41.2 ms, the DAG engine executes, prunes the 4 downstream alarms, and the panel display instantly highlights 'ABS: WSS FL Sensor Circuit Open' in red, while secondary alerts are marked SUPPRESSED."
  > - **04:30 – 07:45 [Scenario 2: Brake Switch Stuck at 160 km/h]**:
  >   > "Here is our ASIL D high-speed test. Vehicle is at 160 km/h, 6500 RPM. We inject the Brake Switch Stuck condition. Observe that master cylinder pressure remains at 0.8 bar. The Diagnostic Master detects the physical impossibility of 160 km/h cruise with hard braking, overrides the ECM torque-kill command, and pinpoints the BCM switch."
  > - **07:45 – 10:30 [Scenario 3: ABS ECU Cutoff]**:
  >   > "Now we sever the ABS node. A storm of seven `U0121` loss-of-communication DTCs floods the bus. The in-degree pruning isolates the root cause to the node itself rather than downstream communication timeouts."
  > - **10:30 – 12:45 [Scenarios 4–6 & Bus Load Analysis]**:
  >   > "Finally, observe the bus performance under 70% heavy bus load. Latency remains bounded at 43.1 ms, proving complete immunity to transmission jitter."

---

### SLIDE 9: Quantitative Results & State-of-the-Art Benchmark (Time: 10:59 – 11:02 | 3 min)
* **What to Show**: Slide 9 experimental results summary table and comparative benchmark against five recent 2023–2025 published works.
* **Verbal Script**:
  > "Slide 9 compiles our empirical metrics across all 60 physical test runs and benchmarks our performance against state-of-the-art literature published between 2023 and 2025.
  >
  > Across all test scenarios:
  > - Raw DTC alarms were reduced from **36 total to 13 isolated**, representing a **63.89% average alarm flood reduction**.
  > - Mean root cause isolation latency was **41.00 ms**, governed by the deterministic 40 ms UDS collection window plus 1 ms evaluation step.
  > - Diagnostic accuracy was **100%**, with zero false isolations.
  >
  > When compared against contemporary research:
  > - **Lin et al. (2023)** achieved 96.4% accuracy using Deep Graph Convolutional Networks, but required 145 ms latency and high GPU/NPU hardware overhead impossible on automotive MCUs.
  > - **Liu et al. (2023)** achieved 92.1% using Dynamic Bayesian Networks, with 210 ms latency and nondeterministic convergence.
  > - **Wang et al. (2023)** used Random Forests with 85 ms latency and 58.2% alarm reduction.
  > - **Lu et al. (2025)** applied Graph Neural Networks achieving 98.2% accuracy, but with 180 ms latency.
  > - **Our work** delivers **100% accuracy, 63.9% alarm reduction, and 42.5 ms latency**—running entirely in **320 bytes of RAM** with zero external dependencies."

---

### SLIDE 10: Key Learnings, Zonal Scalability & Conclusion (Time: 11:02 – 11:05 | 3 min)
* **What to Show**: Slide 10 summarizing engineering takeaways, scalability to Zonal E/E Architectures, and the handoff to the evaluation panel.
* **Verbal Script**:
  > "To conclude, I summarize our key engineering takeaways and future scalability.
  >
  > 1. **Determinism Trumps Complexity in Safety-Critical Systems**: In automotive electronics, predictable worst-case execution time ($O(|V|+|E|)$) and zero false positives are vastly superior to opaque, compute-heavy machine learning models.
  > 2. **Substantial OEM Cost Reduction**: By eliminating 63.9% of secondary alarms, our solution directly cuts diagnostic technician triage time from 45 minutes to under 5 minutes, significantly lowering OEM warranty liabilities and No-Trouble-Found part replacements.
  > 3. **Scalability to Next-Generation Zonal Architectures**: As the automotive industry transitions from distributed domain ECUs to Zonal Controllers connected over 1 Gbps Automotive Ethernet and SOME/IP, the DAG algorithm scales seamlessly. A full-vehicle graph of 50 zonal nodes requires less than **1.2 kilobytes of memory**, making it ideal for AUTOSAR Adaptive and Central Compute platforms.
  >
  > This concludes our presentation. We are now exactly at 11:05 AM, and I welcome all questions and technical critique from the evaluation committee. Thank you."

---

## 4. EVALUATOR Q&A DEFENSE GUIDE (11:05 – 11:15 AM | 10 MINUTES)

Prepare for the following anticipated questions from industry (Tata Technologies) and academic evaluators:

### Q1: "Why did you choose a Directed Acyclic Graph (DAG) instead of Machine Learning or Deep Neural Networks?"
* **Bulletproof Answer**:
  > "In automotive safety-critical systems governed by **ISO 26262 ASIL D**, algorithms must provide **deterministic execution and 100% structural explainability**. 
  > Neural networks and Bayesian models suffer from three fatal automotive drawbacks:
  > 1. **Non-deterministic convergence and latency**: A deep learning model's inference time varies unpredictably under load, lacking worst-case bounded response guarantees.
  > 2. **High hardware footprint**: Automotive body and chassis microcontrollers (like Renesas RH850 or NXP S32K) have kilobytes of RAM and no GPU or floating-point tensor accelerators.
  > 3. **Black-box certification risk**: ISO 26262 Part 8 requires qualification of software tools and algorithms. A DAG with an adjacency matrix has a mathematically provable worst-case execution time of $O(|V|+|E|)$ and can be fully verified with formal methods."

---

### Q2: "What happens if there is a feedback loop in the vehicle dynamics? Doesn't that create a cyclic graph?"
* **Bulletproof Answer**:
  > "That is an excellent control systems observation. In continuous vehicle dynamics, feedback loops exist (e.g., wheel speed affects throttle torque, which in turn affects wheel speed). 
  > However, in **diagnostic fault propagation**, time is strictly monotonic ($\Delta t > 0$). A primary fault event occurs at $t = t_0$. Secondary consequences occur at $t = t_0 + \Delta t$. 
  > By modeling the dependency graph based on the **temporal order of physical causality** and applying a discrete sampling debounce time ($\tau = 20\text{ ms}$), physical causation remains strictly unidirectional and acyclic. Thus, the diagnostic graph is always a DAG."

---

### Q3: "How does your algorithm handle CAN bus arbitration loss and high bus load conditions?"
* **Bulletproof Answer**:
  > "Under CAN 2.0B / ISO 11898-1, message transmission utilizes non-destructive bitwise arbitration.
  > In our network DBC layout, critical safety messages are assigned dominant, low CAN IDs:
  > - `0x0A0` (ABS Status) and `0x0B0` (Wheel Speed) win arbitration against any body or diagnostic traffic.
  > - Diagnostic requests use `0x7DF` and `0x7E0`, which have lower priority.
  > In Scenario 5, we intentionally saturated the bus to 70% load using jabbering frames. Because the Diagnostic Master operates on message reception timestamps rather than bus arbitration ownership, and our CAPL handlers are event-driven, root cause isolation completed within 43.1 ms with zero buffer overrun."

---

### Q4: "How does the Brake Switch Stuck scenario distinguish between a driver genuinely pressing the brake while pressing the throttle versus an electrical short?"
* **Bulletproof Answer**:
  > "We implement a **multi-sensor physical plausibility cross-check**.
  > The BCM reads the digital brake pedal contact switch ($S_{brake} \in \{0, 1\}$).
  > Simultaneously, the ABS/ESP module reads the analog hydraulic master cylinder pressure transducer ($P_{brake}$ in bar).
  > If $S_{brake} = 1$ (closed contact indicating braking), but $P_{brake} < 5.0\text{ bar}$ (no physical hydraulic pressure built in the brake lines) and vehicle speed is $> 30\text{ km/h}$ with throttle open, physical laws prove the brake pads are not clamped to the rotors. 
  > The algorithm therefore diagnoses the discrete switch as electrically stuck and suppresses false brake actuation interventions in the powertrain."

---

### Q5: "How does this comply with ISO 14229 Unified Diagnostic Services (UDS)?"
* **Bulletproof Answer**:
  > "Our Central Diagnostic Master acts as a UDS client and server conforming to:
  > - **Service 0x19 (ReadDTCInformation)**: Queries sub-function `0x02` (ReportDTCByStatusMask) to poll pending and confirmed DTCs from all 4 ECU servers.
  > - **Service 0x14 (ClearDiagnosticInformation)** / **DTC Suppression Mask**: Once the DAG algorithm identifies a node as a secondary symptom, it applies a diagnostic suppression bitmask, preventing the secondary ECU from latching the DTC into its persistent EEPROM/Flash freeze frame buffer.
  > This ensures that when a service technician connects an OBD-II scan tool via Service 0x19, only the true root cause DTC is reported."

---

### Q6: "How does this solution scale when migrating to Zonal Vehicle Architectures?"
* **Bulletproof Answer**:
  > "In a Zonal Architecture, individual domain ECUs are replaced by 2 to 4 Zonal Gateway Controllers (e.g., Front-Left Zone, Front-Right Zone, Rear Zone) communicating with a Central Compute Unit over 100BASE-T1 or 1000BASE-T1 Automotive Ethernet using SOME/IP.
  > Our algorithm scales hierarchically:
  > 1. Each Zonal Gateway executes a local micro-DAG for edge sensors and actuators wired to that zone.
  > 2. The Central Compute Unit executes the inter-zonal DAG across Ethernet SOME/IP service anomalies.
  > Because graph storage scales with $O(|V|^2)$ in bits and computation scales with $O(|V|+|E|)$, a 50-node zonal graph requires only **312 bytes for the adjacency matrix**, executing in under 150 microseconds on an ARM Cortex-R52 core."

---

## 5. QUICK-REFERENCE CARD FOR CANDIDATE (KEEP ON PODIUM)

| Metric / Parameter | Value |
|:---|:---|
| Total CAN Messages | 15 Messages |
| Total CAN Signals | 43 Signals |
| Bus Baud Rate | 500 kbps (High-Speed CAN, ISO 11898-2) |
| Standard Identifier | 11-bit CAN 2.0B |
| Target ECUs | ABS/ESP (0x100), ECM (0x200), TCM (0x300), BCM (0x400) |
| Central Diagnostic Master | CAN ID 0x700 / DIAG_TESTER |
| Average Alarm Reduction | 63.89% (from 36 raw DTCs to 13 isolated) |
| Average Isolation Latency | 41.00 ms (6 / 6 Scenarios) |
| Algorithm Complexity | Worst-case time: $O(\|V\| + \|E\|)$; RAM: $< 320$ bytes |
| Key Automotive Standards | ISO 26262 (ASIL D), ISO 14229 (UDS), ISO 11898-2, AUTOSAR Classic |
| Video Demonstration File | `CB.EN.U4EEE23112_IVN_VIDEO.mp4` (12m 45s, 1080p 60fps) |
