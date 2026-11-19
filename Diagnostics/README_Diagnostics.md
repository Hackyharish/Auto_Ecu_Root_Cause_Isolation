# In-Vehicle Multi-ECU Diagnostic Description (ISO 14229 / ISO 15765-2)

This directory contains the official diagnostic descriptions for the Multi-ECU Root Cause Isolation project compliant with **ISO 14229-1:2013 (UDS)** and **ISO 26262 (Functional Safety)**.

---

## 1. Directory Contents

| File | Format | Purpose | Compatibility |
|---|---|---|---|
| [`MultiECU_Diagnostics.cdd`](MultiECU_Diagnostics.cdd) | Vector CANdela (.cdd XML) | Native Vector CANoe diagnostic specification | Vector CANoe 17/18/19, CANdelaStudio, CANape |
| [`MultiECU_Diagnostics.pdx`](MultiECU_Diagnostics.pdx) | ASAM MCD-2D Container (PDX) | Standard packed ODX container (ZIP + index.xml + odx-d) | Vector CANoe, ODXStudio, DTS Monaco, CANape |
| [`MultiECU_Diagnostics.odx`](MultiECU_Diagnostics.odx) | ASAM MCD-2D (ODX 2.2.0) | Vendor-neutral open XML diagnostic exchange | CANoe, INCA, Softing DTS, ODX Studio |
| [`README_Diagnostics.md`](README_Diagnostics.md) | Markdown | Architecture & CANoe configuration guide | Technical documentation |

---

## 2. ISO 14229-1:2013 Diagnostic Services Implemented

| SID | Service Name | ISO Clause | Supported Sub-functions / DIDs | Usage in Project |
|---|---|---|---|---|
| **0x10** | DiagnosticSessionControl | Clause 9.2 | `0x01` (Default), `0x02` (Programming), `0x03` (Extended), `+0x80` suppress | Master / Console enters Extended Session before polling DTCs |
| **0x11** | ECUReset | Clause 9.3 | `0x01` (Hard Reset), `0x03` (Soft Reset), `+0x80` suppress | Resets node faults & DTC memory |
| **0x14** | ClearDiagnosticInformation | Clause 11.2 | Parameter: `0xFFFFFF` (All DTC groups) | Broadcast on `0x7DF` or physical ID to clear faults |
| **0x19** | ReadDTCInformation | Clause 11.3 | `0x01` (Report Number of DTCs), `0x02` (Report DTC by Status Mask, `AvailMask=0x09`) | Core service used by Fault Memory GUI & RCA Engine (`07 59 02 09 <DTC3> <Status>` or `03 59 02 09` when clear) |
| **0x22** | ReadDataByIdentifier | Clause 10.2 | ECM: `0x0100` RPM, `0x0101` Throttle, `0x0102` Coolant (+40); ABS: `0x0200` WheelSpeeds, `0x0201` VehSpeed; TCM: `0x0300` Gear; BCM: `0x0400` Switches | Live telemetry inspection in Diagnostic Console |
| **0x3E** | TesterPresent | Clause 9.6 | `0x00` (Zero Subfunction), `0x80` (Suppress Response) | Periodic keep-alive heartbeat required by CANoe Diagnostic Console / Fault Memory |

> Unsupported SIDs, sub-functions, or unknown DIDs return ISO 14229-1 Negative Response (`0x7F <SID> <NRC>`: `0x11`, `0x12`, `0x31`) on **physical** requests (`0x7E0`–`0x7E3`) and are suppressed on **functional** broadcast (`0x7DF`).

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

## 5. How to Load PDX in Vector CANoe 19

> **Note:** `Project.cfg` uses Vector CANoe 19 binary-serialized configuration blocks, so the PDX container must be attached once via the CANoe GUI (and saved with `Ctrl+S`).

1. Open **Vector CANoe 19** with `Project.cfg`.
2. On the top ribbon, open **Diagnostics** &rarr; **Diagnostic / ISO TP Configuration**.
3. Under the CAN network (`Powertrain_Body_Network`):
   - Right-click &rarr; **Add Diagnostic Description...** &rarr; select [`MultiECU_Diagnostics.pdx`](MultiECU_Diagnostics.pdx).
   - Select **Add** for all four ECU variants (**`ECM_ECU`**, **`TCM_ECU`**, **`ABS_ESP_ECU`**, **`BCM_ECU`**) using protocol **`UDS_on_CAN`** (physical IDs `0x7E0/0x7E8` .. `0x7E3/0x7EB`, functional `0x7DF`, `500 kbps`).
4. In the **Diagnostic/ISO TP** settings for each added ECU, keep **Diagnostic Simulation / Simulated ECU** **unchecked** so your CAPL nodes (`ECM.can`, `TCM.can`, `ABS_ESP.can`, `BCM.can`) generate the live fault and telemetry responses.
5. Click **OK**, press **F9** (Compile All CAPL Nodes), save (`Ctrl+S`), and start measurement (`F9` / Start).
6. Use **Trace Window**, **Diagnostic Console** (`Diagnostics -> Diagnostic Console`), or **Fault Memory** (`Diagnostics -> Fault Memory`) to query DTCs (`0x19 02 09`), read DIDs (`0x22`), clear faults (`0x14 FF FF FF`), or reset (`0x11 01`).

Regenerate & verify the PDX container offline at any time using:
```bash
python Scripts/generate_pdx.py
```
