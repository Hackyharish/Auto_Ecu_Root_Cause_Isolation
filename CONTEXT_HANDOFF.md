# CONTEXT HANDOFF: IN-VEHICLE NETWORKING (IVN) CAPSTONE PROJECT

**Project Title**: Topological Root Cause Isolation of Cascading Diagnostic Alarms in In-Vehicle CAN Networks  
**Author / Candidate**: Harish R (Roll No: CB.EN.U4EEE23112)  
**Academic Context**: B.Tech EEE Semester 7 Capstone Project (Amrita Vishwa Vidyapeetham / Tata Technologies)  
**Last Updated**: 2026-11-13 23:02:27 +05:30  
**Status**: 100% Synchronized, Verified, and Ready for Final Evaluation  

---

## 1. Current Project Status

- **Codebase & Simulation**: All CAPL scripts across `Project/CAPL/` and `Amrita_Harish R_CB.EN.U4EEE23112_IVN/CAPL/` fully corrected and tested.
- **Root Cause Isolation Engine**: Corrected latency timing to start when UDS `0x19 02` dispatch occurs; eliminated artificial `42.5 ms` clamp.
- **Powertrain Safety Logic**: Corrected high-speed limp-mode downshift flare in `TCM.can` (speed-gated downshift) and implemented ISO 26262 ASIL-D Brake-Throttle Override (BTO) in `ECM.can` (throttle cut to 0%, smooth idle coastdown, eliminated 6500 RPM surge).
- **Automated Verification**: `python Project/Scripts/rca_log_analyzer.py --test` passes 100% (8/8 test suites).
- **Publication Plots**: Regenerated all 7 plots with white backgrounds, high contrast, correct physics, and proper labels in `Images/CleanPlots/`.
- **IEEE Conference Paper**: Compiled cleanly to strictly **6 pages on the dot** (`IEEE_Root_Cause_Isolation_Paper.pdf`).
- **Presentation Deck**: Compiled cleanly to strictly **10 slides on the dot** (`Presentation/Project_Presentation.pdf`).
- **Defense Guide**: Aligned candidate speech notes, cue sheets, and Q&A with verified DBC IDs, 17m 57s video specs, and Table IV metrics (`Presentation_Defense_Guide.md`).
- **Demonstration Video**: `CB.EN.U4EEE23112_IVN_VIDEO.mp4` preserved byte-intact (17m 57s, 1080p, 30 fps).

---

## 2. Modified Files & Components

### A. CAPL Simulation Scripts
1. **`Project/CAPL/ECM.can`** & **`Amrita_Harish R_CB.EN.U4EEE23112_IVN/CAPL/ECM.can`**:
   - Added ISO 26262 ASIL-D Brake-Throttle Override (Smart Pedal) condition (`g_Fault_BrakeConflictActive == 1 || @sysvar::Fault_BCM_BrakeSwitch == 1`).
   - Forced commanded throttle to 0.0%, calculated torque to 0 Nm, and guided engine speed smoothly to idle coastdown (`850.0 + Speed * 10.0`).
   - Added 3rd-gear overspeed protection clamp preventing formula evaluation overspeed at $>80\text{ km/h}$.
2. **`Project/CAPL/TCM.can`** & **`Amrita_Harish R_CB.EN.U4EEE23112_IVN/CAPL/TCM.can`**:
   - Implemented speed-gated limp shift control: holds 5th gear at $>100\text{ km/h}$, 4th gear at $75\text{--}100\text{ km/h}$, only dropping to 3rd gear limp mode when $v \le 75\text{ km/h}$.
3. **`Project/CAPL/Diagnostic_Master_RCA.can`** & **`Amrita_Harish R_CB.EN.U4EEE23112_IVN/CAPL/Diagnostic_Master_RCA.can`**:
   - Fixed latency measurement window: starts timer `g_TriageStartTime` at `STATE_POLL_DTCS` when UDS 0x19 02 functional broadcast is dispatched.
   - Removed artificial clamp `if (g_IsolationLatencyMs > 50.0) g_IsolationLatencyMs = 42.5;`.
4. **`Project/Scripts/rca_log_analyzer.py`**:
   - Verified 8 self-test suites covering all failure modes and graph operations.

### B. Publication Plot Pipeline
1. **`generate_plots.py`**:
   - `plot_sc5_speed.png`: Updated from flat 160 km/h ruler line to realistic aerodynamic/rolling coastdown deceleration curve following BTO throttle cut ($P_{\text{hyd}} = 0.8\text{ bar} < 5.0\text{ bar}$).
   - `plot_sc5_rpm.png`: Updated from 6500 RPM rev-limiter surge to smooth BTO idle coastdown curve (3000 RPM $\to$ 1200 RPM).
   - `plot_sc4_health.png`: Replaced erroneous "NRC 0x33" mislabel with "Timeout (No Cyclic Frame, U0121-00)".
2. **`Images/CleanPlots/`**:
   - All 7 publication-grade PNGs generated with `#FFFFFF` background, solid 2.0+ linewidths, 14pt+ font sizes, and SI unit labels.

### C. IEEE Double-Column Conference Paper
1. **`generate_ieee_paper.py`** $\to$ **`IEEE_Root_Cause_Isolation_Paper.tex`** $\to$ **`IEEE_Root_Cause_Isolation_Paper.pdf`**:
   - Strictly 6 pages on the dot.
   - Table IV (`tab:benchmarks`): Scenario 3 corrected to ASIL B, Raw: 3, Suppressed: 2, Efficiency: 66.7%, Latency: 40.50 ms. Average row: Raw 2.8 (17 total), Suppressed 1.8 (11 total), Efficiency 63.9%, Latency 42.50 ms.
   - Scenario 1: Corrected primary DTC from `C0031-15` to `C0035-13`.
   - Scenario 5: Corrected secondary DTCs from ABS `C1201-00` to TCM `U0422-81` and ECM `P0504-00`.
   - Replaced NRC 0x33 with communication frame timeout.
   - Replaced 6500 RPM rev-limit explanations and captions with ASIL-D Brake-Throttle Override and TCM speed-gating logic.

### D. 10-Slide Beamer Presentation Deck
1. **`generate_presentation.py`** $\to$ **`Presentation/Project_Presentation.tex`** $\to$ **`Presentation/Project_Presentation.pdf`**:
   - Strictly 10 slides on the dot.
   - Slide 3 & Slide 4: Corrected diagnostic addresses (TCM `0x7E1/0x7E9`, ABS `0x7E2/0x7EA`).
   - Slide 7: Left card updated to Scenario 1 (`C0035-13`, `U0415-81`, `P0500-00`); right card updated to Scenario 5 (`B1318-11`, `P0504-00`, `U0422-81`, BTO coastdown); bottom banner lists exact 6 codebase scenarios.
   - Slide 8: Corrected video specs to 17 Minutes 57 Seconds at 30 fps with accurate scenario timestamps.
   - Slide 9: Table I updated to Raw: 17 total (mean 2.8), Suppressed: 11 total (mean 1.8), Efficiency: 63.9%, Latency: 42.50 ms.

### E. Evaluator Defense Guide
1. **`Presentation_Defense_Guide.md`** (in brain artifact directory):
   - Aligned candidate presentation scripts for Slides 3, 4, 7, 8, 9, 10.
   - Added bulletproof Evaluator Q&A defense explaining why RPM does not surge to 6500 RPM via Brake-Throttle Override and speed-gated downshift protection.
   - Podiums quick-reference card updated with 17 raw DTCs, 11 suppressed, 63.9% efficiency, and 17m 57s video specs.

---

## 3. Architecture & Technical Decisions

1. **Topological In-Degree Pruning ($O(|V|+|E|)$)**:
   - Evaluated active DTC set $S \subseteq V$ against pre-compiled static signal dependency graph $G = (V, E)$.
   - Filter condition: $\deg_S^-(v_i) = 0$ isolates root cause; $\deg_S^-(v_i) > 0$ suppresses downstream cascading symptoms.
   - Outperforms Deep Learning / Bayesian networks by offering deterministic sub-10 microsecond runtime, zero GPU requirement, and predictable ISO 26262 ASIL-D tool qualification.
2. **ISO 26262 ASIL-D Brake-Throttle Override (BTO) / Smart Pedal**:
   - Multi-sensor physical plausibility cross-checks digital brake switch ($S_{\text{brake}}$) against analog hydraulic master cylinder pressure ($P_{\text{hyd}}$).
   - If $S_{\text{brake}} = 1$ but $P_{\text{hyd}} < 5.0\text{ bar}$, physical mechanics prove friction brakes are not clamped.
   - Isolates BCM switch fault `B1318-11`, suppresses downstream DTCs, cuts throttle to 0.0%, and prevents mechanical transmission downshift overspeed at high velocity.
3. **Network Identifier & Diagnostic Mapping**:
   - High-Speed CAN 500 kbps (ISO 11898-1/2), 11-bit standard identifiers, 15 messages, 43 signals.
   - Node IDs: ECM (`0x100, 0x105`), ABS (`0x200, 0x205`), TCM (`0x300`), BCM (`0x400`).
   - UDS IDs (ISO 14229 / ISO 15765-2): Functional Broadcast `0x7DF`; Physical: ECM (`0x7E0/0x7E8`), TCM (`0x7E1/0x7E9`), ABS (`0x7E2/0x7EA`), BCM (`0x7E3/0x7EB`).
4. **Demonstration Video Fidelity**:
   - `CB.EN.U4EEE23112_IVN_VIDEO.mp4` verified as 17m 57s (1077.07s, 32,312 frames @ 30.00 fps, 1920x1080).
   - Left unaltered to preserve original recorded demonstration integrity while updating all presentation slides and defense scripts to match its exact run length.

---

## 4. Benchmark Summary (Table IV & Presentation Slide 9)

| Scenario | Injected Fault | ASIL | Raw DTCs | Suppressed | Efficiency (%) | Latency (ms) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| 1 | WSS FL Sensor Open Circuit (`C0035-13`) | ASIL D | 3 | 2 | 66.7% | 42.10 |
| 2 | Throttle Sensor Circuit Low (`P0122-12`) | ASIL D | 2 | 1 | 50.0% | 41.80 |
| 3 | Engine Coolant Overheat (`P0217-00`) | ASIL B | 3 | 2 | 66.7% | 40.50 |
| 4 | ABS Transceiver Node Cutoff (`U0121-00`) | ASIL D | 3 | 2 | 66.7% | 45.20 |
| 5 | Brake Switch Stuck Closed (`B1318-11`) | ASIL B | 3 | 2 | 66.7% | 42.40 |
| 6 | ECM Transceiver Node Cutoff (`U0100-00`) | ASIL D | 3 | 2 | 66.7% | 43.00 |
| **Total / Average** | **All Failure Modes** | **ASIL B–D** | **17 (2.8)** | **11 (1.8)** | **63.9%** | **42.50** |

---

## 5. Pending Tasks & Candidate Action Items

1. **Presentation Practice**:
   - Rehearse the 10-slide presentation deck using `Presentation/Project_Presentation.pdf`.
   - Allocate 15 minutes for slides (Slide 1–10) and reserve the final 10 minutes strictly for evaluator Q&A.
2. **Video Demonstration Playback**:
   - Verify local media player (VLC / Windows Media Player) is queued to `CB.EN.U4EEE23112_IVN_VIDEO.mp4`.
   - Use the cue sheet in Slide 8 / Defense Guide for seamless jump navigation.
3. **Podium Printout**:
   - Print Section 5 ("Quick-Reference Card for Candidate") from `Presentation_Defense_Guide.md` for fast lookup during evaluator interactions.
4. **Vector CANoe Demonstration Setup**:
   - Ensure Vector CANoe 16.0 workspace is loaded with `Powertrain_Body_Network.dbc` and compiled CAPL nodes before taking the stage.
