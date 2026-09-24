# In-Vehicle Multi-ECU Diagnostic Description (ISO 14229 / ISO 15765-2)

This directory contains the official diagnostic descriptions for the Multi-ECU Root Cause Isolation project compliant with **ISO 14229-1:2013 (UDS)** and **ISO 26262 (Functional Safety)**.

---

## 1. Directory Contents

| File | Format | Purpose | Compatibility |
|---|---|---|---|
| [`MultiECU_Diagnostics.cdd`](MultiECU_Diagnostics.cdd) | Vector CANdela (.cdd XML) | Native Vector CANoe diagnostic specification | Vector CANoe 17/18/19, CANdelaStudio, CANape |
| [`MultiECU_Diagnostics.odx`](MultiECU_Diagnostics.odx) | ASAM MCD-2D (ODX 2.2.0) | Vendor-neutral open XML diagnostic exchange | CANoe, INCA, Softing DTS, ODX Studio |
| [`README_Diagnostics.md`](README_Diagnostics.md) | Markdown | Architecture & CANoe configuration guide | Technical documentation |

---

## 2. ISO 14229-1:2013 Diagnostic Services Implemented

| SID | Service Name | ISO Clause | Supported Sub-functions | Usage in Project |
|---|---|---|---|---|
| **0x10** | DiagnosticSessionControl | Clause 9.2 | `0x01` (Default), `0x02` (Programming), `0x03` (Extended) | Master enters Extended Session before polling DTCs |
| **0x11** | ECUReset | Clause 9.3 | `0x01` (Hard Reset), `0x03` (Soft Reset) | Node recovery testing |
| **0x14** | ClearDiagnosticInformation | Clause 11.2 | Parameter: `0xFFFFFF` (All DTC groups) | Broadcast on `0x7DF` to clear network faults |
| **0x19** | ReadDTCInformation | Clause 11.3 | `0x01` (Count), `0x02` (By Status Mask `0x09`), `0x04` (Freeze Frame), `0x0A` (Supported) | Core service used by RCA Engine to poll active DTCs |
| **0x22** | ReadDataByIdentifier | Clause 10.2 | DIDs: `0xF190` (VIN), `0x0100`–`0x0106` (Speed, RPM, Temp, Pressure) | Real-time parameter inspection |
| **0x27** | SecurityAccess | Clause 9.4 | `0x01` (Request Seed), `0x02` (Send Key) | Security gating for critical routines |
| **0x3E** | TesterPresent | Clause 9.6 | `0x00` (Zero Subfunction), `0x80` (Suppress Response) | Keep-alive heartbeat during diagnostic sessions |

---

## 3. Addressing & Transport Layer Architecture (ISO 15765-2 DoCAN)

- **Baudrate:** 500 kbps (CAN 2.0B)
- **Addressing Format:** Normal 11-bit Standard Identifiers
- **Functional Broadcast Request ID:** `0x7DF`

| ECU Node | Physical Request ID | Physical Response ID | Role in System |
|---|---|---|---|
| **ECM** (Engine Control Module) | `0x7E0` | `0x7E8` | Powertrain Controller |
| **TCM** (Transmission Control) | `0x7E1` | `0x7E9` | Drivetrain Controller |
| **ABS/ESP** (Chassis Module) | `0x7E2` | `0x7EA` | Brake / Stability Module |
| **BCM** (Body Control Module) | `0x7E3` | `0x7EB` | Gateway / Body Module |

---

## 4. DTC Fault Memory & RCA Truth Table

| ECU | DTC Code | Display Code | Fault Description | Failure Type | Severity | Category |
|---|---|---|---|---|---|---|
| **ABS** | `0xC00351` | `C0035-13` | Left Front Wheel Speed Sensor Open | Circuit Open | **ASIL D** | **Primary Root** |
| **ECM** | `0x012212` | `P0122-12` | Throttle Position Sensor 'A' Low | Circuit Low | **ASIL D** | **Primary Root** |
| **ECM** | `0x021700` | `P0217-00` | Engine Coolant Over-Temperature | Temperature High | **ASIL B** | **Primary Root** |
| **BCM** | `0x931811` | `B1318-11` | Brake Pedal Switch Stuck High | Short to Power | **ASIL B** | **Primary Root** |
| **ECM** | `0xD10000` | `U0100-00` | Lost Communication with ECM/PCM | Bus Dropout | **ASIL D** | **Primary Root (Cutoff)** |
| **ABS** | `0xD12100` | `U0121-00` | Lost Communication with ABS Module | Bus Dropout | **ASIL D** | **Primary Root (Cutoff)** |
| **TCM** | `0xD41581` | `U0415-81` | Invalid Data From ABS Control Module | Signal Invalid | QM | Secondary Cascade |
| **TCM** | `0xD40186` | `U0401-86` | Invalid Data From ECM (Throttle) | Signal Invalid | QM | Secondary Cascade |
| **TCM** | `0xD40182` | `U0401-82` | Invalid Data From ECM (Coolant Range) | Signal Invalid | QM | Secondary Cascade |
| **TCM** | `0xD42281` | `U0422-81` | Invalid Data From BCM (Brake Conflict) | Plausibility Conflict | QM | Secondary Cascade |
| **ECM** | `0x050000` | `P0500-00` | Vehicle Speed Sensor 'A' Missing | Missing Signal | QM | Secondary Cascade |
| **ECM** | `0x050400` | `P0504-00` | Brake Switch A/B Plausibility Conflict | Correlation Error | QM | Secondary Cascade |
| **BCM** | `0x90A200` | `B10A2-00` | High Coolant Temp Lamp Request Active | Indicator Error | QM | Secondary Cascade |

---

## 5. How to Load CDD in Vector CANoe

To enable symbolic decoding and the CANoe Fault Memory GUI:

1. Open **Vector CANoe** with `Project.cfg`.
2. On the top ribbon, navigate to: **Diagnostics** &rarr; **Diagnostic / ISO TP Configuration**.
3. Under the CAN network (`Powertrain_Body_Network`):
   - Right-click and choose **Add Diagnostic Description...**
   - Browse and select [`MultiECU_Diagnostics.cdd`](MultiECU_Diagnostics.cdd).
4. Assign the diagnostic descriptions to the respective simulated nodes (`ECM`, `TCM`, `ABS`, `BCM`).
5. In CANoe:
   - **Trace Window:** Raw UDS frames (`03 19 02 09`) will now symbolically display service names, sub-functions, and decoded DTC names.
   - **Diagnostic Console (`Diagnostics &rarr; Diagnostic Console`):** Allows sending single requests directly via GUI.
   - **Fault Memory Window (`Diagnostics &rarr; Fault Memory`):** Displays visual tree of all active DTCs, status masks, and Freeze Frame snapshots.
