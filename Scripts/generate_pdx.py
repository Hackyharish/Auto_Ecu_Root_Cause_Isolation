"""
Generate ASAM MCD-2D (ODX 2.2.0) / Vector CANoe 19 compliant PDX container
and standalone ODX file for the Multi-ECU Root Cause Isolation network.

Verifies round-trip parsing via odxtools (protocols, communication parameters,
physical/functional CAN IDs, baudrate, UDS service encode/decode, and DTCs).
"""

import os
import zipfile
from pathlib import Path
import odxtools

ROOT_DIR = Path(__file__).resolve().parents[1]
DIAG_DIR = ROOT_DIR / "Diagnostics"
PDX_PATH = DIAG_DIR / "MultiECU_Diagnostics.pdx"
ODX_PATH = DIAG_DIR / "MultiECU_Diagnostics.odx"

ECU_CONFIGS = [
    {
        "id": "ECU_ABS",
        "short": "ABS_ESP_ECU",
        "long": "Anti-Lock Braking System / Electronic Stability Program",
        "desc": "Chassis control module responsible for wheel speed sensing and ABS/ESP intervention.",
        "phys_req": 0x7E2,
        "phys_resp": 0x7EA,
        "link_id": "LL_ABS_ESP",
        "dtcs": [
            ("DTC_ABS_C003513", "C0035_13", 0xC00351, "C0035-13", "Left Front Wheel Speed Sensor Circuit Open"),
            ("DTC_ABS_U012100", "U0121_00", 0xD12100, "U0121-00", "Lost Communication with ABS Control Module"),
        ],
        "dids": [
            ("DID_0200", "WheelSpeeds_Snapshot", 0x0200, "WheelSpeed_FL_FR_RL_RR", 32),
            ("DID_0201", "VehicleSpeed", 0x0201, "VehicleSpeed_Raw", 16),
        ],
    },
    {
        "id": "ECU_ECM",
        "short": "ECM_ECU",
        "long": "Engine Control Module / Powertrain Controller",
        "desc": "Powertrain controller managing engine throttle, coolant telemetry, and torque.",
        "phys_req": 0x7E0,
        "phys_resp": 0x7E8,
        "link_id": "LL_ECM",
        "dtcs": [
            ("DTC_ECM_P012212", "P0122_12", 0x012212, "P0122-12", "Throttle Position Sensor 'A' Circuit Low Input"),
            ("DTC_ECM_P021700", "P0217_00", 0x021700, "P0217-00", "Engine Coolant Over-Temperature Condition"),
            ("DTC_ECM_P050000", "P0500_00", 0x050000, "P0500-00", "Vehicle Speed Sensor 'A' Missing Signal"),
            ("DTC_ECM_P050400", "P0504_00", 0x050400, "P0504-00", "Brake Switch A/B Correlation Plausibility Fault"),
            ("DTC_ECM_U010000", "U0100_00", 0xD10000, "U0100-00", "Lost Communication with ECM/PCM"),
            ("DTC_ECM_U012100", "U0121_00", 0xD12100, "U0121-00", "Lost Communication with ABS Control Module"),
        ],
        "dids": [
            ("DID_0100", "EngineSpeed", 0x0100, "EngineRPM_Value", 16),
            ("DID_0101", "ThrottlePosition", 0x0101, "ThrottlePos_Pct", 8),
            ("DID_0102", "CoolantTemperature", 0x0102, "CoolantTemp_Offset40", 8),
        ],
    },
    {
        "id": "ECU_TCM",
        "short": "TCM_ECU",
        "long": "Transmission Control Module",
        "desc": "Automatic transmission controller computing shift schedules and speed-gated limp mode.",
        "phys_req": 0x7E1,
        "phys_resp": 0x7E9,
        "link_id": "LL_TCM",
        "dtcs": [
            ("DTC_TCM_U041581", "U0415_81", 0xD41581, "U0415-81", "Invalid Data Received from ABS Module"),
            ("DTC_TCM_U040186", "U0401_86", 0xD40186, "U0401-86", "Invalid Data Received from ECM (Throttle Signal)"),
            ("DTC_TCM_U040182", "U0401_82", 0xD40182, "U0401-82", "Invalid Data Received from ECM (Coolant Range)"),
            ("DTC_TCM_U042281", "U0422_81", 0xD42281, "U0422-81", "Invalid Data Received from BCM (Brake Switch Conflict)"),
            ("DTC_TCM_U010000", "U0100_00", 0xD10000, "U0100-00", "Lost Communication with ECM/PCM"),
            ("DTC_TCM_U012100", "U0121_00", 0xD12100, "U0121-00", "Lost Communication with ABS Control Module"),
        ],
        "dids": [
            ("DID_0300", "CurrentGear", 0x0300, "CurrentGear_Enum", 8),
        ],
    },
    {
        "id": "ECU_BCM",
        "short": "BCM_ECU",
        "long": "Body Control Module",
        "desc": "Body electronics controller handling ignition state, brake switch, and warnings.",
        "phys_req": 0x7E3,
        "phys_resp": 0x7EB,
        "link_id": "LL_BCM",
        "dtcs": [
            ("DTC_BCM_B131811", "B1318_11", 0x931811, "B1318-11", "Brake Pedal Switch Stuck Active / Circuit Short to Power"),
            ("DTC_BCM_B10A200", "B10A2_00", 0x90A200, "B10A2-00", "High Coolant Temp Indicator Lamp Request Active"),
        ],
        "dids": [
            ("DID_0400", "ChassisSwitchState", 0x0400, "BrakeSwitch_Ignition_Bits", 8),
        ],
    },
]

ISO_11898_CS = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ODX MODEL-VERSION="2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="odx.xsd">
  <COMPARAM-SUBSET ID="CS_ISO_11898_Raw_CAN" CATEGORY="PHYSICAL">
    <SHORT-NAME>ISO_11898_Raw_CAN</SHORT-NAME>
    <LONG-NAME>ISO 11898 High-Speed CAN Physical Layer (500 kbps)</LONG-NAME>
    <COMPARAMS>
      <COMPARAM ID="CS_ISO_11898.CP_Baudrate" PARAM-CLASS="BUS" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_Baudrate</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>500000</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_CAN_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_11898.CP_SamplePoint" PARAM-CLASS="BUS" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_SamplePoint</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>80</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_CAN_Uint32"/>
      </COMPARAM>
    </COMPARAMS>
    <DATA-OBJECT-PROPS>
      <DATA-OBJECT-PROP ID="DOP_CAN_Uint32">
        <SHORT-NAME>DOP_CAN_Uint32</SHORT-NAME>
        <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
        <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>32</BIT-LENGTH></DIAG-CODED-TYPE>
        <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
      </DATA-OBJECT-PROP>
    </DATA-OBJECT-PROPS>
  </COMPARAM-SUBSET>
</ODX>
"""

ISO_15765_2_CS = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ODX MODEL-VERSION="2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="odx.xsd">
  <COMPARAM-SUBSET ID="CS_ISO_15765_2" CATEGORY="TRANSPORT">
    <SHORT-NAME>ISO_15765_2</SHORT-NAME>
    <LONG-NAME>ISO 15765-2 DoCAN Transport Protocol Parameters</LONG-NAME>
    <COMPARAMS>
      <COMPARAM ID="CS_ISO_15765_2.CP_CanFuncReqFormat" PARAM-CLASS="COM" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_CanFuncReqFormat</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>5</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_CanFuncReqId" PARAM-CLASS="COM" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_CanFuncReqId</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>2015</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_CanFuncReqExtAddr" PARAM-CLASS="COM" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_CanFuncReqExtAddr</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>0</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_SendRemoteFrame" PARAM-CLASS="COM" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_SendRemoteFrame</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>0</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_StMin" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_StMin</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>0</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_BlockSize" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_BlockSize</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>0</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_As" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_As</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>25000</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_Bs" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_Bs</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>75000</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_2.CP_Cr" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
        <SHORT-NAME>CP_Cr</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>150000</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
      </COMPARAM>
    </COMPARAMS>
    <COMPLEX-COMPARAMS>
      <COMPLEX-COMPARAM ID="CS_ISO_15765_2.CP_UniqueRespIdTable" PARAM-CLASS="UNIQUE_ID" CPTYPE="STANDARD" CPUSAGE="ECU-COMM" ALLOW-MULTIPLE-VALUES="true">
        <SHORT-NAME>CP_UniqueRespIdTable</SHORT-NAME>
        <COMPARAM ID="CS_ISO_15765_2.CP_CanPhysReqFormat" PARAM-CLASS="UNIQUE_ID" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
          <SHORT-NAME>CP_CanPhysReqFormat</SHORT-NAME>
          <PHYSICAL-DEFAULT-VALUE>5</PHYSICAL-DEFAULT-VALUE>
          <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
        </COMPARAM>
        <COMPARAM ID="CS_ISO_15765_2.CP_CanPhysReqId" PARAM-CLASS="UNIQUE_ID" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
          <SHORT-NAME>CP_CanPhysReqId</SHORT-NAME>
          <PHYSICAL-DEFAULT-VALUE>2016</PHYSICAL-DEFAULT-VALUE>
          <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
        </COMPARAM>
        <COMPARAM ID="CS_ISO_15765_2.CP_CanPhysReqExtAddr" PARAM-CLASS="UNIQUE_ID" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
          <SHORT-NAME>CP_CanPhysReqExtAddr</SHORT-NAME>
          <PHYSICAL-DEFAULT-VALUE>0</PHYSICAL-DEFAULT-VALUE>
          <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
        </COMPARAM>
        <COMPARAM ID="CS_ISO_15765_2.CP_CanRespUSDTFormat" PARAM-CLASS="UNIQUE_ID" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
          <SHORT-NAME>CP_CanRespUSDTFormat</SHORT-NAME>
          <PHYSICAL-DEFAULT-VALUE>5</PHYSICAL-DEFAULT-VALUE>
          <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
        </COMPARAM>
        <COMPARAM ID="CS_ISO_15765_2.CP_CanRespUSDTId" PARAM-CLASS="UNIQUE_ID" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
          <SHORT-NAME>CP_CanRespUSDTId</SHORT-NAME>
          <PHYSICAL-DEFAULT-VALUE>2024</PHYSICAL-DEFAULT-VALUE>
          <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
        </COMPARAM>
        <COMPARAM ID="CS_ISO_15765_2.CP_CanRespUSDTExtAddr" PARAM-CLASS="UNIQUE_ID" CPTYPE="STANDARD" CPUSAGE="ECU-COMM">
          <SHORT-NAME>CP_CanRespUSDTExtAddr</SHORT-NAME>
          <PHYSICAL-DEFAULT-VALUE>0</PHYSICAL-DEFAULT-VALUE>
          <DATA-OBJECT-PROP-REF ID-REF="DOP_TP_Uint32"/>
        </COMPARAM>
      </COMPLEX-COMPARAM>
    </COMPLEX-COMPARAMS>
    <DATA-OBJECT-PROPS>
      <DATA-OBJECT-PROP ID="DOP_TP_Uint32">
        <SHORT-NAME>DOP_TP_Uint32</SHORT-NAME>
        <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
        <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>32</BIT-LENGTH></DIAG-CODED-TYPE>
        <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
      </DATA-OBJECT-PROP>
    </DATA-OBJECT-PROPS>
  </COMPARAM-SUBSET>
</ODX>
"""

ISO_15765_3_CS = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ODX MODEL-VERSION="2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="odx.xsd">
  <COMPARAM-SUBSET ID="CS_ISO_15765_3_on_CAN" CATEGORY="SESSION">
    <SHORT-NAME>ISO_15765_3_on_CAN</SHORT-NAME>
    <LONG-NAME>ISO 15765-3 / ISO 14229-1 UDS Application Timing Parameters</LONG-NAME>
    <COMPARAMS>
      <COMPARAM ID="CS_ISO_15765_3.CP_P2Max" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="APPLICATION">
        <SHORT-NAME>CP_P2Max</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>50000</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_UDS_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_3.CP_P2Star" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="APPLICATION">
        <SHORT-NAME>CP_P2Star</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>5000000</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_UDS_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_3.CP_TesterPresentTime" PARAM-CLASS="TIMING" CPTYPE="STANDARD" CPUSAGE="APPLICATION">
        <SHORT-NAME>CP_TesterPresentTime</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>2000000</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_UDS_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_3.CP_TesterPresentHandling" PARAM-CLASS="COM" CPTYPE="STANDARD" CPUSAGE="APPLICATION">
        <SHORT-NAME>CP_TesterPresentHandling</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>1</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_UDS_Uint32"/>
      </COMPARAM>
      <COMPARAM ID="CS_ISO_15765_3.CP_TesterPresentReqRsp" PARAM-CLASS="COM" CPTYPE="STANDARD" CPUSAGE="APPLICATION">
        <SHORT-NAME>CP_TesterPresentReqRsp</SHORT-NAME>
        <PHYSICAL-DEFAULT-VALUE>1</PHYSICAL-DEFAULT-VALUE>
        <DATA-OBJECT-PROP-REF ID-REF="DOP_UDS_Uint32"/>
      </COMPARAM>
    </COMPARAMS>
    <DATA-OBJECT-PROPS>
      <DATA-OBJECT-PROP ID="DOP_UDS_Uint32">
        <SHORT-NAME>DOP_UDS_Uint32</SHORT-NAME>
        <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
        <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>32</BIT-LENGTH></DIAG-CODED-TYPE>
        <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
      </DATA-OBJECT-PROP>
    </DATA-OBJECT-PROPS>
  </COMPARAM-SUBSET>
</ODX>
"""

COMPARAM_SPEC_XML = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ODX MODEL-VERSION="2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="odx.xsd">
  <COMPARAM-SPEC ID="CPS_MultiECU_UDS_on_CAN">
    <SHORT-NAME>MultiECU_CommParams</SHORT-NAME>
    <LONG-NAME>ISO 15765-3 UDS on ISO 15765-2 DoCAN Communication Stack</LONG-NAME>
    <PROT-STACKS>
      <PROT-STACK ID="PS_ISO_15765_3_on_CAN">
        <SHORT-NAME>ISO_15765_3_on_ISO_15765_2</SHORT-NAME>
        <LONG-NAME>UDS on High-Speed CAN (500 kbps, 11-bit Addressing)</LONG-NAME>
        <PDU-PROTOCOL-TYPE>ISO_15765_3_on_ISO_15765_2</PDU-PROTOCOL-TYPE>
        <PHYSICAL-LINK-TYPE>ISO_11898_2_DWCAN</PHYSICAL-LINK-TYPE>
        <COMPARAM-SUBSET-REFS>
          <COMPARAM-SUBSET-REF ID-REF="CS_ISO_11898_Raw_CAN" DOCREF="ISO_11898_Raw_CAN" DOCTYPE="COMPARAM-SUBSET"/>
          <COMPARAM-SUBSET-REF ID-REF="CS_ISO_15765_2" DOCREF="ISO_15765_2" DOCTYPE="COMPARAM-SUBSET"/>
          <COMPARAM-SUBSET-REF ID-REF="CS_ISO_15765_3_on_CAN" DOCREF="ISO_15765_3_on_CAN" DOCTYPE="COMPARAM-SUBSET"/>
        </COMPARAM-SUBSET-REFS>
      </PROT-STACK>
    </PROT-STACKS>
  </COMPARAM-SPEC>
</ODX>
"""


def build_ecu_variant_xml(ecu: dict) -> str:
    dtcs_xml = "\n".join(
        f"""                <DTC ID="{dtc_id}">
                  <SHORT-NAME>{sn}</SHORT-NAME>
                  <TROUBLE-CODE>{code}</TROUBLE-CODE>
                  <DISPLAY-TROUBLE-CODE>{disp}</DISPLAY-TROUBLE-CODE>
                  <TEXT>{text}</TEXT>
                </DTC>"""
        for dtc_id, sn, code, disp, text in ecu["dtcs"]
    )
    did_dops = []
    did_comms = []
    did_reqs = []
    did_resps = []
    for did_id, did_sn, did_val, sig_sn, bits in ecu["dids"]:
        eid = f"{ecu['short']}_{did_id}"
        did_dops.append(
            f"""            <DATA-OBJECT-PROP ID="DOP_{eid}">
              <SHORT-NAME>DOP_{did_sn}</SHORT-NAME>
              <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
              <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>{bits}</BIT-LENGTH></DIAG-CODED-TYPE>
              <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
            </DATA-OBJECT-PROP>"""
        )
        did_comms.append(
            f"""          <DIAG-SERVICE ID="DS_{eid}" SEMANTIC="CURRENTDATA">
            <SHORT-NAME>RDBI_{did_sn}</SHORT-NAME>
            <LONG-NAME>ReadDataByIdentifier 0x{did_val:04X} - {did_sn}</LONG-NAME>
            <REQUEST-REF ID-REF="REQ_{eid}"/>
            <POS-RESPONSE-REFS>
              <POS-RESPONSE-REF ID-REF="POS_{eid}"/>
            </POS-RESPONSE-REFS>
          </DIAG-SERVICE>"""
        )
        did_reqs.append(
            f"""          <REQUEST ID="REQ_{eid}">
            <SHORT-NAME>REQ_{did_sn}</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>SID</SHORT-NAME>
                <BYTE-POSITION>0</BYTE-POSITION>
                <CODED-VALUE>34</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="ID" xsi:type="CODED-CONST">
                <SHORT-NAME>DataIdentifier</SHORT-NAME>
                <BYTE-POSITION>1</BYTE-POSITION>
                <CODED-VALUE>{did_val}</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>16</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
            </PARAMS>
          </REQUEST>"""
        )
        did_resps.append(
            f"""          <POS-RESPONSE ID="POS_{eid}">
            <SHORT-NAME>POS_{did_sn}</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>RSID</SHORT-NAME>
                <BYTE-POSITION>0</BYTE-POSITION>
                <CODED-VALUE>98</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="ID" xsi:type="MATCHING-REQUEST-PARAM">
                <SHORT-NAME>DataIdentifier</SHORT-NAME>
                <BYTE-POSITION>1</BYTE-POSITION>
                <REQUEST-BYTE-POS>1</REQUEST-BYTE-POS>
                <BYTE-LENGTH>2</BYTE-LENGTH>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>{sig_sn}</SHORT-NAME>
                <BYTE-POSITION>3</BYTE-POSITION>
                <DOP-REF ID-REF="DOP_{eid}"/>
              </PARAM>
            </PARAMS>
          </POS-RESPONSE>"""
        )

    dtc_dop_id = f"DTC_DOP_{ecu['id']}"
    dtc_rec_struct_id = f"STRUCT_DTC_Rec_{ecu['id']}"
    dtc_eop_id = f"EOP_DTC_{ecu['id']}"
    ds_readdtc_id = f"DS_{ecu['id']}_ReadDTC_ByStatusMask"
    req_readdtc_id = f"REQ_{ecu['id']}_ReadDTC_ByStatusMask"
    pos_readdtc_id = f"POS_{ecu['id']}_ReadDTC_ByStatusMask"

    return f"""      <ECU-VARIANT ID="{ecu['id']}">
        <SHORT-NAME>{ecu['short']}</SHORT-NAME>
        <LONG-NAME>{ecu['long']}</LONG-NAME>
        <DESC><p>{ecu['desc']}</p></DESC>
        <DIAG-DATA-DICTIONARY-SPEC>
          <DTC-DOPS>
            <DTC-DOP ID="{dtc_dop_id}">
              <SHORT-NAME>{dtc_dop_id}</SHORT-NAME>
              <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>24</BIT-LENGTH></DIAG-CODED-TYPE>
              <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
              <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
              <DTCS>
{dtcs_xml}
              </DTCS>
            </DTC-DOP>
          </DTC-DOPS>
          <STRUCTURES>
            <STRUCTURE ID="{dtc_rec_struct_id}" BYTE-SIZE="4">
              <SHORT-NAME>DTCAndStatusRecord_{ecu['short']}</SHORT-NAME>
              <PARAMS>
                <PARAM SEMANTIC="DTC" xsi:type="VALUE">
                  <SHORT-NAME>DTCRecord</SHORT-NAME>
                  <BYTE-POSITION>0</BYTE-POSITION>
                  <DOP-REF ID-REF="{dtc_dop_id}"/>
                </PARAM>
                <PARAM SEMANTIC="DTCSTATUS" xsi:type="VALUE">
                  <SHORT-NAME>StatusOfDTC</SHORT-NAME>
                  <BYTE-POSITION>3</BYTE-POSITION>
                  <DOP-REF ID-REF="DOP_Uint8"/>
                </PARAM>
              </PARAMS>
            </STRUCTURE>
          </STRUCTURES>
          <END-OF-PDU-FIELDS>
            <END-OF-PDU-FIELD ID="{dtc_eop_id}">
              <SHORT-NAME>DTCAndStatusList_{ecu['short']}</SHORT-NAME>
              <MIN-NUMBER-OF-ITEMS>0</MIN-NUMBER-OF-ITEMS>
              <BASIC-STRUCTURE-REF ID-REF="{dtc_rec_struct_id}"/>
            </END-OF-PDU-FIELD>
          </END-OF-PDU-FIELDS>
          <DATA-OBJECT-PROPS>
{chr(10).join(did_dops)}
          </DATA-OBJECT-PROPS>
        </DIAG-DATA-DICTIONARY-SPEC>
        <DIAG-COMMS>
          <DIAG-SERVICE ID="{ds_readdtc_id}" SEMANTIC="FAULTMEMORY">
            <SHORT-NAME>FaultMemory_ReadDTCByStatusMask</SHORT-NAME>
            <LONG-NAME>UDS 0x19 02 - Read DTC By Status Mask ({ecu['short']})</LONG-NAME>
            <REQUEST-REF ID-REF="{req_readdtc_id}"/>
            <POS-RESPONSE-REFS>
              <POS-RESPONSE-REF ID-REF="{pos_readdtc_id}"/>
            </POS-RESPONSE-REFS>
          </DIAG-SERVICE>
{chr(10).join(did_comms)}
        </DIAG-COMMS>
        <REQUESTS>
          <REQUEST ID="{req_readdtc_id}">
            <SHORT-NAME>REQ_ReadDTCByStatusMask_{ecu['short']}</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>SID</SHORT-NAME>
                <BYTE-POSITION>0</BYTE-POSITION>
                <CODED-VALUE>25</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="CODED-CONST">
                <SHORT-NAME>SubFunction</SHORT-NAME>
                <BYTE-POSITION>1</BYTE-POSITION>
                <CODED-VALUE>2</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>DTCStatusMask</SHORT-NAME>
                <BYTE-POSITION>2</BYTE-POSITION>
                <PHYSICAL-DEFAULT-VALUE>9</PHYSICAL-DEFAULT-VALUE>
                <DOP-REF ID-REF="DOP_Uint8"/>
              </PARAM>
            </PARAMS>
          </REQUEST>
{chr(10).join(did_reqs)}
        </REQUESTS>
        <POS-RESPONSES>
          <POS-RESPONSE ID="{pos_readdtc_id}">
            <SHORT-NAME>POS_ReadDTCByStatusMask_{ecu['short']}</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>RSID</SHORT-NAME>
                <BYTE-POSITION>0</BYTE-POSITION>
                <CODED-VALUE>89</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="CODED-CONST">
                <SHORT-NAME>SubFunction</SHORT-NAME>
                <BYTE-POSITION>1</BYTE-POSITION>
                <CODED-VALUE>2</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>DTCStatusAvailabilityMask</SHORT-NAME>
                <BYTE-POSITION>2</BYTE-POSITION>
                <DOP-REF ID-REF="DOP_Uint8"/>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>DTCAndStatusRecord</SHORT-NAME>
                <BYTE-POSITION>3</BYTE-POSITION>
                <DOP-REF ID-REF="{dtc_eop_id}"/>
              </PARAM>
            </PARAMS>
          </POS-RESPONSE>
{chr(10).join(did_resps)}
        </POS-RESPONSES>
        <COMPARAM-REFS>
          <COMPARAM-REF ID-REF="CS_ISO_15765_2.CP_UniqueRespIdTable" DOCREF="ISO_15765_2" DOCTYPE="COMPARAM-SUBSET">
            <COMPLEX-VALUE>
              <SIMPLE-VALUE>5</SIMPLE-VALUE>
              <SIMPLE-VALUE>{ecu['phys_req']}</SIMPLE-VALUE>
              <SIMPLE-VALUE>0</SIMPLE-VALUE>
              <SIMPLE-VALUE>5</SIMPLE-VALUE>
              <SIMPLE-VALUE>{ecu['phys_resp']}</SIMPLE-VALUE>
              <SIMPLE-VALUE>0</SIMPLE-VALUE>
            </COMPLEX-VALUE>
          </COMPARAM-REF>
          <COMPARAM-REF ID-REF="CS_ISO_15765_2.CP_CanFuncReqId" DOCREF="ISO_15765_2" DOCTYPE="COMPARAM-SUBSET">
            <SIMPLE-VALUE>2015</SIMPLE-VALUE>
          </COMPARAM-REF>
        </COMPARAM-REFS>
        <PARENT-REFS>
          <PARENT-REF xsi:type="BASE-VARIANT-REF" ID-REF="BV_UDS_Base"/>
        </PARENT-REFS>
      </ECU-VARIANT>"""


def build_dlc_xml() -> str:
    variants_xml = "\n".join(build_ecu_variant_xml(e) for e in ECU_CONFIGS)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ODX MODEL-VERSION="2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="odx.xsd">
  <DIAG-LAYER-CONTAINER ID="DLC_MultiECU_Diagnostics">
    <SHORT-NAME>MultiECU_Diagnostics_Container</SHORT-NAME>
    <LONG-NAME>In-Vehicle Multi-ECU Diagnostic Description</LONG-NAME>
    <DESC><p>ASAM MCD-2D ODX 2.2.0 description for ECM, TCM, ABS/ESP, and BCM UDS diagnostics.</p></DESC>

    <PROTOCOLS>
      <PROTOCOL ID="PROTO_UDS_on_CAN">
        <SHORT-NAME>UDS_on_CAN</SHORT-NAME>
        <LONG-NAME>ISO 14229-1 Unified Diagnostic Services on High-Speed CAN (ISO 15765-2)</LONG-NAME>
        <COMPARAM-REFS>
          <COMPARAM-REF ID-REF="CS_ISO_11898.CP_Baudrate" DOCREF="ISO_11898_Raw_CAN" DOCTYPE="COMPARAM-SUBSET">
            <SIMPLE-VALUE>500000</SIMPLE-VALUE>
          </COMPARAM-REF>
          <COMPARAM-REF ID-REF="CS_ISO_15765_2.CP_CanFuncReqId" DOCREF="ISO_15765_2" DOCTYPE="COMPARAM-SUBSET">
            <SIMPLE-VALUE>2015</SIMPLE-VALUE>
          </COMPARAM-REF>
          <COMPARAM-REF ID-REF="CS_ISO_15765_3.CP_P2Max" DOCREF="ISO_15765_3_on_CAN" DOCTYPE="COMPARAM-SUBSET">
            <SIMPLE-VALUE>50000</SIMPLE-VALUE>
          </COMPARAM-REF>
          <COMPARAM-REF ID-REF="CS_ISO_15765_3.CP_P2Star" DOCREF="ISO_15765_3_on_CAN" DOCTYPE="COMPARAM-SUBSET">
            <SIMPLE-VALUE>5000000</SIMPLE-VALUE>
          </COMPARAM-REF>
        </COMPARAM-REFS>
        <COMPARAM-SPEC-REF ID-REF="CPS_MultiECU_UDS_on_CAN" DOCREF="MultiECU_CommParams" DOCTYPE="COMPARAM-SPEC"/>
        <PROT-STACK-SNREF SHORT-NAME="ISO_15765_3_on_ISO_15765_2"/>
      </PROTOCOL>
    </PROTOCOLS>

    <BASE-VARIANTS>
      <BASE-VARIANT ID="BV_UDS_Base">
        <SHORT-NAME>UDS_Base_Protocol</SHORT-NAME>
        <LONG-NAME>ISO 14229-1:2013 Base UDS Services</LONG-NAME>
        <DIAG-DATA-DICTIONARY-SPEC>
          <DATA-OBJECT-PROPS>
            <DATA-OBJECT-PROP ID="DOP_Uint8">
              <SHORT-NAME>DOP_Uint8</SHORT-NAME>
              <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
              <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
            </DATA-OBJECT-PROP>
            <DATA-OBJECT-PROP ID="DOP_Uint16">
              <SHORT-NAME>DOP_Uint16</SHORT-NAME>
              <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
              <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>16</BIT-LENGTH></DIAG-CODED-TYPE>
              <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
            </DATA-OBJECT-PROP>
            <DATA-OBJECT-PROP ID="DOP_Uint24">
              <SHORT-NAME>DOP_Uint24</SHORT-NAME>
              <COMPU-METHOD><CATEGORY>IDENTICAL</CATEGORY></COMPU-METHOD>
              <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>24</BIT-LENGTH></DIAG-CODED-TYPE>
              <PHYSICAL-TYPE BASE-DATA-TYPE="A_UINT32"/>
            </DATA-OBJECT-PROP>
            <DATA-OBJECT-PROP ID="DOP_SessionType">
              <SHORT-NAME>DOP_SessionType</SHORT-NAME>
              <COMPU-METHOD>
                <CATEGORY>TEXTTABLE</CATEGORY>
                <COMPU-INTERNAL-TO-PHYS>
                  <COMPU-SCALES>
                    <COMPU-SCALE><LOWER-LIMIT>1</LOWER-LIMIT><UPPER-LIMIT>1</UPPER-LIMIT><COMPU-CONST><VT>DefaultSession (0x01)</VT></COMPU-CONST></COMPU-SCALE>
                    <COMPU-SCALE><LOWER-LIMIT>2</LOWER-LIMIT><UPPER-LIMIT>2</UPPER-LIMIT><COMPU-CONST><VT>ProgrammingSession (0x02)</VT></COMPU-CONST></COMPU-SCALE>
                    <COMPU-SCALE><LOWER-LIMIT>3</LOWER-LIMIT><UPPER-LIMIT>3</UPPER-LIMIT><COMPU-CONST><VT>ExtendedDiagnosticSession (0x03)</VT></COMPU-CONST></COMPU-SCALE>
                  </COMPU-SCALES>
                </COMPU-INTERNAL-TO-PHYS>
              </COMPU-METHOD>
              <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              <PHYSICAL-TYPE BASE-DATA-TYPE="A_UNICODE2STRING"/>
            </DATA-OBJECT-PROP>
            <DATA-OBJECT-PROP ID="DOP_ResetType">
              <SHORT-NAME>DOP_ResetType</SHORT-NAME>
              <COMPU-METHOD>
                <CATEGORY>TEXTTABLE</CATEGORY>
                <COMPU-INTERNAL-TO-PHYS>
                  <COMPU-SCALES>
                    <COMPU-SCALE><LOWER-LIMIT>1</LOWER-LIMIT><UPPER-LIMIT>1</UPPER-LIMIT><COMPU-CONST><VT>HardReset (0x01)</VT></COMPU-CONST></COMPU-SCALE>
                    <COMPU-SCALE><LOWER-LIMIT>3</LOWER-LIMIT><UPPER-LIMIT>3</UPPER-LIMIT><COMPU-CONST><VT>SoftReset (0x03)</VT></COMPU-CONST></COMPU-SCALE>
                  </COMPU-SCALES>
                </COMPU-INTERNAL-TO-PHYS>
              </COMPU-METHOD>
              <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              <PHYSICAL-TYPE BASE-DATA-TYPE="A_UNICODE2STRING"/>
            </DATA-OBJECT-PROP>
          </DATA-OBJECT-PROPS>
        </DIAG-DATA-DICTIONARY-SPEC>

        <DIAG-COMMS>
          <DIAG-SERVICE ID="DS_DiagnosticSessionControl" SEMANTIC="SESSION">
            <SHORT-NAME>DiagnosticSessionControl</SHORT-NAME>
            <LONG-NAME>UDS 0x10 - Diagnostic Session Control</LONG-NAME>
            <REQUEST-REF ID-REF="REQ_DiagnosticSessionControl"/>
            <POS-RESPONSE-REFS><POS-RESPONSE-REF ID-REF="POS_DiagnosticSessionControl"/></POS-RESPONSE-REFS>
          </DIAG-SERVICE>
          <DIAG-SERVICE ID="DS_ECUReset" SEMANTIC="RESET">
            <SHORT-NAME>ECUReset</SHORT-NAME>
            <LONG-NAME>UDS 0x11 - ECU Reset</LONG-NAME>
            <REQUEST-REF ID-REF="REQ_ECUReset"/>
            <POS-RESPONSE-REFS><POS-RESPONSE-REF ID-REF="POS_ECUReset"/></POS-RESPONSE-REFS>
          </DIAG-SERVICE>
          <DIAG-SERVICE ID="DS_ClearDiagnosticInformation" SEMANTIC="FAULTMEMORY">
            <SHORT-NAME>ClearDiagnosticInformation</SHORT-NAME>
            <LONG-NAME>UDS 0x14 - Clear Diagnostic Information</LONG-NAME>
            <REQUEST-REF ID-REF="REQ_ClearDiagnosticInformation"/>
            <POS-RESPONSE-REFS><POS-RESPONSE-REF ID-REF="POS_ClearDiagnosticInformation"/></POS-RESPONSE-REFS>
          </DIAG-SERVICE>
          <DIAG-SERVICE ID="DS_ReadNumberOfDTCs" SEMANTIC="FAULTMEMORY">
            <SHORT-NAME>FaultMemory_ReadNumberOfDTCs</SHORT-NAME>
            <LONG-NAME>UDS 0x19 01 - Report Number Of DTCs By Status Mask</LONG-NAME>
            <REQUEST-REF ID-REF="REQ_ReadNumberOfDTCs"/>
            <POS-RESPONSE-REFS><POS-RESPONSE-REF ID-REF="POS_ReadNumberOfDTCs"/></POS-RESPONSE-REFS>
          </DIAG-SERVICE>
          <DIAG-SERVICE ID="DS_TesterPresent" SEMANTIC="TESTERPRESENT">
            <SHORT-NAME>TesterPresent</SHORT-NAME>
            <LONG-NAME>UDS 0x3E - Tester Present</LONG-NAME>
            <REQUEST-REF ID-REF="REQ_TesterPresent"/>
            <POS-RESPONSE-REFS><POS-RESPONSE-REF ID-REF="POS_TesterPresent"/></POS-RESPONSE-REFS>
          </DIAG-SERVICE>
        </DIAG-COMMS>

        <REQUESTS>
          <REQUEST ID="REQ_DiagnosticSessionControl">
            <SHORT-NAME>REQ_DiagnosticSessionControl</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>SID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>16</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="VALUE">
                <SHORT-NAME>DiagnosticSessionType</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION>
                <DOP-REF ID-REF="DOP_SessionType"/>
              </PARAM>
            </PARAMS>
          </REQUEST>
          <REQUEST ID="REQ_ECUReset">
            <SHORT-NAME>REQ_ECUReset</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>SID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>17</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="VALUE">
                <SHORT-NAME>ResetType</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION>
                <DOP-REF ID-REF="DOP_ResetType"/>
              </PARAM>
            </PARAMS>
          </REQUEST>
          <REQUEST ID="REQ_ClearDiagnosticInformation">
            <SHORT-NAME>REQ_ClearDiagnosticInformation</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>SID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>20</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>GroupOfDTC</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION>
                <PHYSICAL-DEFAULT-VALUE>16777215</PHYSICAL-DEFAULT-VALUE>
                <DOP-REF ID-REF="DOP_Uint24"/>
              </PARAM>
            </PARAMS>
          </REQUEST>
          <REQUEST ID="REQ_ReadNumberOfDTCs">
            <SHORT-NAME>REQ_ReadNumberOfDTCs</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>SID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>25</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="CODED-CONST">
                <SHORT-NAME>SubFunction</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION><CODED-VALUE>1</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>DTCStatusMask</SHORT-NAME><BYTE-POSITION>2</BYTE-POSITION>
                <PHYSICAL-DEFAULT-VALUE>9</PHYSICAL-DEFAULT-VALUE>
                <DOP-REF ID-REF="DOP_Uint8"/>
              </PARAM>
            </PARAMS>
          </REQUEST>
          <REQUEST ID="REQ_TesterPresent">
            <SHORT-NAME>REQ_TesterPresent</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>SID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>62</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="CODED-CONST">
                <SHORT-NAME>ZeroSubFunction</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION><CODED-VALUE>0</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
            </PARAMS>
          </REQUEST>
        </REQUESTS>

        <POS-RESPONSES>
          <POS-RESPONSE ID="POS_DiagnosticSessionControl">
            <SHORT-NAME>POS_DiagnosticSessionControl</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>RSID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>80</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="MATCHING-REQUEST-PARAM">
                <SHORT-NAME>DiagnosticSessionType</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION><REQUEST-BYTE-POS>1</REQUEST-BYTE-POS><BYTE-LENGTH>1</BYTE-LENGTH>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>P2ServerMax_ms</SHORT-NAME><BYTE-POSITION>2</BYTE-POSITION><DOP-REF ID-REF="DOP_Uint16"/>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>P2StarServerMax_10ms</SHORT-NAME><BYTE-POSITION>4</BYTE-POSITION><DOP-REF ID-REF="DOP_Uint16"/>
              </PARAM>
            </PARAMS>
          </POS-RESPONSE>
          <POS-RESPONSE ID="POS_ECUReset">
            <SHORT-NAME>POS_ECUReset</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>RSID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>81</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="MATCHING-REQUEST-PARAM">
                <SHORT-NAME>ResetType</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION><REQUEST-BYTE-POS>1</REQUEST-BYTE-POS><BYTE-LENGTH>1</BYTE-LENGTH>
              </PARAM>
            </PARAMS>
          </POS-RESPONSE>
          <POS-RESPONSE ID="POS_ClearDiagnosticInformation">
            <SHORT-NAME>POS_ClearDiagnosticInformation</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>RSID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>84</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
            </PARAMS>
          </POS-RESPONSE>
          <POS-RESPONSE ID="POS_ReadNumberOfDTCs">
            <SHORT-NAME>POS_ReadNumberOfDTCs</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>RSID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>89</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="CODED-CONST">
                <SHORT-NAME>SubFunction</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION><CODED-VALUE>1</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>DTCStatusAvailabilityMask</SHORT-NAME><BYTE-POSITION>2</BYTE-POSITION><DOP-REF ID-REF="DOP_Uint8"/>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>DTCFormatIdentifier</SHORT-NAME><BYTE-POSITION>3</BYTE-POSITION><DOP-REF ID-REF="DOP_Uint8"/>
              </PARAM>
              <PARAM SEMANTIC="DATA" xsi:type="VALUE">
                <SHORT-NAME>DTCCount</SHORT-NAME><BYTE-POSITION>4</BYTE-POSITION><DOP-REF ID-REF="DOP_Uint16"/>
              </PARAM>
            </PARAMS>
          </POS-RESPONSE>
          <POS-RESPONSE ID="POS_TesterPresent">
            <SHORT-NAME>POS_TesterPresent</SHORT-NAME>
            <PARAMS>
              <PARAM SEMANTIC="SERVICE-ID" xsi:type="CODED-CONST">
                <SHORT-NAME>RSID</SHORT-NAME><BYTE-POSITION>0</BYTE-POSITION><CODED-VALUE>126</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
              <PARAM SEMANTIC="SUBFUNCTION" xsi:type="CODED-CONST">
                <SHORT-NAME>ZeroSubFunction</SHORT-NAME><BYTE-POSITION>1</BYTE-POSITION><CODED-VALUE>0</CODED-VALUE>
                <DIAG-CODED-TYPE BASE-DATA-TYPE="A_UINT32" xsi:type="STANDARD-LENGTH-TYPE"><BIT-LENGTH>8</BIT-LENGTH></DIAG-CODED-TYPE>
              </PARAM>
            </PARAMS>
          </POS-RESPONSE>
        </POS-RESPONSES>

        <PARENT-REFS>
          <PARENT-REF xsi:type="PROTOCOL-REF" ID-REF="PROTO_UDS_on_CAN"/>
        </PARENT-REFS>
      </BASE-VARIANT>
    </BASE-VARIANTS>

    <ECU-VARIANTS>
{variants_xml}
    </ECU-VARIANTS>
  </DIAG-LAYER-CONTAINER>
</ODX>
"""


def build_vehicle_info_xml() -> str:
    links_xml = "\n".join(
        f"""          <LOGICAL-LINK ID="{e['link_id']}" xsi:type="MEMBER-LOGICAL-LINK">
            <SHORT-NAME>{e['link_id']}</SHORT-NAME>
            <LONG-NAME>{e['long']} (0x{e['phys_req']:03X}/0x{e['phys_resp']:03X})</LONG-NAME>
            <PHYSICAL-VEHICLE-LINK-REF ID-REF="PVL_CAN_Powertrain"/>
            <PROTOCOL-REF ID-REF="PROTO_UDS_on_CAN" DOCREF="MultiECU_Diagnostics_Container" DOCTYPE="CONTAINER"/>
            <BASE-VARIANT-REF ID-REF="BV_UDS_Base" DOCREF="MultiECU_Diagnostics_Container" DOCTYPE="CONTAINER"/>
            <LINK-COMPARAM-REFS>
              <LINK-COMPARAM-REF ID-REF="CS_ISO_15765_2.CP_UniqueRespIdTable" DOCREF="ISO_15765_2" DOCTYPE="COMPARAM-SUBSET">
                <COMPLEX-VALUE>
                  <SIMPLE-VALUE>5</SIMPLE-VALUE>
                  <SIMPLE-VALUE>{e['phys_req']}</SIMPLE-VALUE>
                  <SIMPLE-VALUE>0</SIMPLE-VALUE>
                  <SIMPLE-VALUE>5</SIMPLE-VALUE>
                  <SIMPLE-VALUE>{e['phys_resp']}</SIMPLE-VALUE>
                  <SIMPLE-VALUE>0</SIMPLE-VALUE>
                </COMPLEX-VALUE>
              </LINK-COMPARAM-REF>
              <LINK-COMPARAM-REF ID-REF="CS_ISO_15765_2.CP_CanFuncReqId" DOCREF="ISO_15765_2" DOCTYPE="COMPARAM-SUBSET">
                <SIMPLE-VALUE>2015</SIMPLE-VALUE>
              </LINK-COMPARAM-REF>
            </LINK-COMPARAM-REFS>
            <PROT-STACK-SNREF SHORT-NAME="ISO_15765_3_on_ISO_15765_2"/>
          </LOGICAL-LINK>"""
        for e in ECU_CONFIGS
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ODX MODEL-VERSION="2.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="odx.xsd">
  <VEHICLE-INFO-SPEC ID="VIS_MultiECU_VehicleInfo">
    <SHORT-NAME>MultiECU_VehicleInfo</SHORT-NAME>
    <LONG-NAME>Multi-ECU Powertrain &amp; Chassis CAN Topology</LONG-NAME>
    <VEHICLE-INFORMATIONS>
      <VEHICLE-INFORMATION>
        <SHORT-NAME>Powertrain_Body_Network_Vehicle</SHORT-NAME>
        <LONG-NAME>500 kbps High-Speed CAN Network (ECM, TCM, ABS/ESP, BCM)</LONG-NAME>
        <LOGICAL-LINKS>
          <LOGICAL-LINK ID="LL_UDS_Functional" xsi:type="MEMBER-LOGICAL-LINK">
            <SHORT-NAME>LL_UDS_Functional</SHORT-NAME>
            <LONG-NAME>UDS Functional Broadcast Request (0x7DF)</LONG-NAME>
            <PHYSICAL-VEHICLE-LINK-REF ID-REF="PVL_CAN_Powertrain"/>
            <PROTOCOL-REF ID-REF="PROTO_UDS_on_CAN" DOCREF="MultiECU_Diagnostics_Container" DOCTYPE="CONTAINER"/>
            <BASE-VARIANT-REF ID-REF="BV_UDS_Base" DOCREF="MultiECU_Diagnostics_Container" DOCTYPE="CONTAINER"/>
            <LINK-COMPARAM-REFS>
              <LINK-COMPARAM-REF ID-REF="CS_ISO_15765_2.CP_CanFuncReqId" DOCREF="ISO_15765_2" DOCTYPE="COMPARAM-SUBSET">
                <SIMPLE-VALUE>2015</SIMPLE-VALUE>
              </LINK-COMPARAM-REF>
            </LINK-COMPARAM-REFS>
            <PROT-STACK-SNREF SHORT-NAME="ISO_15765_3_on_ISO_15765_2"/>
          </LOGICAL-LINK>
{links_xml}
        </LOGICAL-LINKS>
        <PHYSICAL-VEHICLE-LINKS>
          <PHYSICAL-VEHICLE-LINK ID="PVL_CAN_Powertrain" TYPE="ISO_11898_2_DWCAN">
            <SHORT-NAME>CAN_Powertrain_500kbps</SHORT-NAME>
            <LONG-NAME>High-Speed CAN 500 kbps Bus</LONG-NAME>
          </PHYSICAL-VEHICLE-LINK>
        </PHYSICAL-VEHICLE-LINKS>
      </VEHICLE-INFORMATION>
    </VEHICLE-INFORMATIONS>
  </VEHICLE-INFO-SPEC>
</ODX>
"""


def main() -> None:
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    dlc_xml = build_dlc_xml()
    ODX_PATH.write_text(dlc_xml, encoding="utf-8")

    # Stage all ODX files into a temporary zip, load via odxtools, and write canonical PDX
    tmp_pdx = DIAG_DIR / "_tmp_stage.pdx"
    entries = [
        ("ISO_11898_Raw_CAN.odx-cs", "application/x-asam.odx.odx-cs", ISO_11898_CS),
        ("ISO_15765_2.odx-cs", "application/x-asam.odx.odx-cs", ISO_15765_2_CS),
        ("ISO_15765_3_on_CAN.odx-cs", "application/x-asam.odx.odx-cs", ISO_15765_3_CS),
        ("MultiECU_CommParams.odx-c", "application/x-asam.odx.odx-c", COMPARAM_SPEC_XML),
        ("MultiECU_VehicleInfo.odx-v", "application/x-asam.odx.odx-v", build_vehicle_info_xml()),
        ("MultiECU_Diagnostics_Container.odx-d", "application/x-asam.odx.odx-d", dlc_xml),
    ]
    ablocks = "\n".join(
        f"""    <ABLOCK UPD="UNCHANGED">
      <SHORT-NAME>{os.path.splitext(fn)[0]}</SHORT-NAME>
      <FILES><FILE CREATION-DATE="2026-11-19T15:25:00" MIME-TYPE="{mime}">{fn}</FILE></FILES>
    </ABLOCK>"""
        for fn, mime, _ in entries
    )
    idx_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CATALOG xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" F-DTD-VERSION="ODX-2.2.0" xsi:noNamespaceSchemaLocation="odx-cc.xsd">
  <SHORT-NAME>MultiECU_PDX_Catalog</SHORT-NAME>
  <ABLOCKS>
{ablocks}
  </ABLOCKS>
</CATALOG>
"""
    with zipfile.ZipFile(tmp_pdx, "w", zipfile.ZIP_DEFLATED) as zf:
        for fn, _, content in entries:
            zf.writestr(fn, content)
        zf.writestr("index.xml", idx_xml)

    db = odxtools.load_pdx_file(str(tmp_pdx))
    odxtools.write_pdx_file(str(PDX_PATH), db)
    tmp_pdx.unlink(missing_ok=True)

    # Full verification pass on final PDX
    vdb = odxtools.load_pdx_file(str(PDX_PATH))
    assert [p.short_name for p in vdb.protocols] == ["UDS_on_CAN"]
    for cfg in ECU_CONFIGS:
        ecu = vdb.ecus[cfg["short"]]
        assert ecu.get_can_baudrate() == 500000
        assert ecu.get_can_func_req_id() == 0x7DF
        assert ecu.get_can_receive_id() == cfg["phys_req"]
        assert ecu.get_can_send_id() == cfg["phys_resp"]
        dtc_service = ecu.services["FaultMemory_ReadDTCByStatusMask"]
        enc_req = dtc_service.encode_request(DTCStatusMask=0x09)
        assert bytes(enc_req) == b"\x19\x02\x09", enc_req
        dec_resp = ecu.decode(bytes([0x59, 0x02, 0x09]) + cfg["dtcs"][0][2].to_bytes(3, "big") + b"\x09")
        assert len(dec_resp) == 1 and len(dec_resp[0].param_dict["DTCAndStatusRecord"]) == 1
        dec_empty = ecu.decode(b"\x59\x02\x09")
        assert len(dec_empty) == 1 and dec_empty[0].param_dict["DTCAndStatusRecord"] == []
        tp_req = ecu.services["TesterPresent"].encode_request(ZeroSubFunction=0x00)
        assert bytes(tp_req) == b"\x3E\x00"
        dtcs = ecu.diag_data_dictionary_spec.dtc_dops[0].dtcs
        assert len(dtcs) == len(cfg["dtcs"])
        print(
            f"[OK] {ecu.short_name}: baud={ecu.get_can_baudrate()}, "
            f"func=0x{ecu.get_can_func_req_id():03X}, "
            f"rx=0x{ecu.get_can_receive_id():03X}, "
            f"tx=0x{ecu.get_can_send_id():03X}, "
            f"dtcs={len(dtcs)}, services={len(ecu.services)}"
        )


if __name__ == "__main__":
    main()
