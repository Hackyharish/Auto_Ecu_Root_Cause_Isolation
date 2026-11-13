import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('Images/CleanPlots', exist_ok=True)

# Publication style: Wide aspect ratio, ultra-clean, zero curve obstruction
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 0.9,
    'axes.labelsize': 9.2,
    'axes.titlesize': 9.5,
    'xtick.labelsize': 7.8,
    'ytick.labelsize': 7.8,
    'xtick.color': 'black',
    'ytick.color': 'black',
    'xtick.major.size': 2.5,
    'ytick.major.size': 2.5,
    'legend.fontsize': 6.8,
    'legend.edgecolor': '#D0D0D0',
    'legend.facecolor': '#FAFAFA',
    'legend.framealpha': 0.75,
    'legend.borderpad': 0.2,
    'legend.labelspacing': 0.15,
    'legend.handlelength': 0.9,
    'legend.handletextpad': 0.3,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'savefig.facecolor': 'white',
    'savefig.edgecolor': 'white',
    'grid.color': '#E8E8E8',
    'grid.linestyle': '--',
    'grid.linewidth': 0.45,
    'grid.alpha': 0.8
})

COLOR_BLUE = '#0072B2'
COLOR_ORANGE = '#D55E00'
COLOR_GREEN = '#009E73'
COLOR_BLACK = '#000000'

t = np.linspace(0, 6.0, 601)

# ==============================================================================
# Plot 1: Scenario 1 - Vehicle Speed (km/h)
# ==============================================================================
fig, ax = plt.subplots(figsize=(4.4, 1.55), dpi=300)
v_speed = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 1.0:
        v_speed[i] = 46.84 * (ti / 1.0)
    elif ti < 4.2:
        v_speed[i] = 46.84
    elif ti < 4.28:
        v_speed[i] = 46.84 * (1.0 - (ti - 4.2) / 0.08)
    else:
        v_speed[i] = 0.0

ax.plot(t, v_speed, color=COLOR_BLUE, linewidth=1.8, label='Speed')
ax.axvline(x=4.2, color=COLOR_ORANGE, linestyle=':', linewidth=1.2)
ax.text(4.25, 50, 'Fault (4.2 s)', color=COLOR_ORANGE, fontsize=7.0, fontweight='bold')
ax.scatter([4.28], [0.0], color=COLOR_ORANGE, s=20, zorder=5)
ax.annotate('Drop to 0 km/h (C0035-13)', xy=(4.28, 0.0), xytext=(1.8, 12.0),
            arrowprops=dict(arrowstyle='->', lw=0.8, color='black'),
            fontsize=7.2, fontweight='bold', color='black')

ax.set_xlim(0, 6.0)
ax.set_ylim(-3, 62)
ax.set_xlabel('Time (s)', fontweight='bold')
ax.set_ylabel('Speed (km/h)', fontweight='bold')
ax.grid(True)
fig.tight_layout(pad=0.4)
fig.savefig('Images/CleanPlots/plot_sc1_speed.png', dpi=300, facecolor='white')
plt.close(fig)

# ==============================================================================
# Plot 2: Scenario 1 - Transmission Gear
# ==============================================================================
fig, ax = plt.subplots(figsize=(4.4, 1.55), dpi=300)
gear = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 0.8:
        gear[i] = 1
    elif ti < 2.0:
        gear[i] = 2
    elif ti < 3.2:
        gear[i] = 3
    elif ti < 4.2:
        gear[i] = 4
    else:
        gear[i] = 3

ax.step(t, gear, where='post', color=COLOR_GREEN, linewidth=1.8, label='Gear')
ax.axvline(x=4.2, color=COLOR_ORANGE, linestyle=':', linewidth=1.2)
ax.text(4.25, 4.2, 'Fault (4.2 s)', color=COLOR_ORANGE, fontsize=7.0, fontweight='bold')
ax.annotate('3rd Gear Lock (U0415-81)', xy=(4.25, 3.0), xytext=(1.5, 1.4),
            arrowprops=dict(arrowstyle='->', lw=0.8, color='black'),
            fontsize=7.2, fontweight='bold', color='black')

ax.set_xlim(0, 6.0)
ax.set_ylim(0.2, 4.8)
ax.set_yticks([1, 2, 3, 4])
ax.set_yticklabels(['1st', '2nd', '3rd', '4th'])
ax.set_xlabel('Time (s)', fontweight='bold')
ax.set_ylabel('Gear', fontweight='bold')
ax.grid(True)
fig.tight_layout(pad=0.4)
fig.savefig('Images/CleanPlots/plot_sc1_gear.png', dpi=300, facecolor='white')
plt.close(fig)

# ==============================================================================
# Plot 3: Scenario 2 - Engine Speed RPM (Throttle Sensor Low)
# ==============================================================================
fig, ax = plt.subplots(figsize=(4.4, 1.55), dpi=300)
rpm = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 1.0:
        rpm[i] = 800 + 1200 * (ti / 1.0)
    elif ti < 3.5:
        rpm[i] = 2000 + 1400 * ((ti - 1.0) / 2.5)
    elif ti < 3.8:
        rpm[i] = 3400 - (3400 - 1200) * ((ti - 3.5) / 0.3)
    else:
        rpm[i] = 1200 + 30 * np.sin(10 * ti)

ax.plot(t, rpm, color=COLOR_BLUE, linewidth=1.8, label='Engine RPM')
ax.axvline(x=3.5, color=COLOR_ORANGE, linestyle=':', linewidth=1.2)
ax.text(3.55, 3600, 'Fault (3.5 s)', color=COLOR_ORANGE, fontsize=7.0, fontweight='bold')
ax.annotate('Limp Mode (1200 rpm, P0122-12)', xy=(3.8, 1200), xytext=(1.0, 500),
            arrowprops=dict(arrowstyle='->', lw=0.8, color='black'),
            fontsize=7.2, fontweight='bold', color='black')

ax.set_xlim(0, 6.0)
ax.set_ylim(200, 4200)
ax.set_xlabel('Time (s)', fontweight='bold')
ax.set_ylabel('Speed (rpm)', fontweight='bold')
ax.grid(True)
fig.tight_layout(pad=0.4)
fig.savefig('Images/CleanPlots/plot_sc2_rpm.png', dpi=300, facecolor='white')
plt.close(fig)

# ==============================================================================
# Plot 4: Scenario 3 - Coolant Overheat
# ==============================================================================
fig, ax = plt.subplots(figsize=(4.4, 1.55), dpi=300)
rpm_coolant = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 2.0:
        rpm_coolant[i] = 1500 + 2000 * (ti / 2.0)
    elif ti < 3.2:
        rpm_coolant[i] = 3500 + 100 * np.sin(6 * ti)
    elif ti < 3.7:
        rpm_coolant[i] = 3500 - (3500 - 2500) * ((ti - 3.2) / 0.5)
    else:
        rpm_coolant[i] = 2500 + 20 * np.sin(8 * ti)

ax.plot(t, rpm_coolant, color=COLOR_BLUE, linewidth=1.8, label='Engine RPM')
ax.axhline(y=2500, color=COLOR_BLACK, linestyle='--', linewidth=1.0, label='2500 rpm Limit')
ax.axvline(x=3.2, color=COLOR_ORANGE, linestyle=':', linewidth=1.2)
ax.text(3.25, 3800, 'Overheat (3.2 s)', color=COLOR_ORANGE, fontsize=7.0, fontweight='bold')
ax.annotate('Rev-Limit (P0217-00)', xy=(3.7, 2500), xytext=(0.8, 900),
            arrowprops=dict(arrowstyle='->', lw=0.8, color='black'),
            fontsize=7.2, fontweight='bold', color='black')

ax.set_xlim(0, 6.0)
ax.set_ylim(500, 4400)
ax.set_xlabel('Time (s)', fontweight='bold')
ax.set_ylabel('Speed (rpm)', fontweight='bold')
ax.grid(True)
ax.legend(loc='upper right', frameon=True)
fig.tight_layout(pad=0.4)
fig.savefig('Images/CleanPlots/plot_sc3_rpm.png', dpi=300, facecolor='white')
plt.close(fig)

# ==============================================================================
# Plot 5: Scenario 5 - Vehicle Speed Under Brake Switch Stuck
# ==============================================================================
fig, ax = plt.subplots(figsize=(4.4, 1.55), dpi=300)
v_speed_sc5 = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 2.5:
        v_speed_sc5[i] = 160.0
    else:
        # ASIL-D Brake-Throttle Override coastdown deceleration
        v_speed_sc5[i] = 160.0 - 5.2 * (ti - 2.5)

ax.plot(t, v_speed_sc5, color=COLOR_BLUE, linewidth=2.0, label='VehicleSpeed')
ax.axvline(x=2.5, color=COLOR_ORANGE, linestyle=':', linewidth=1.2)
ax.text(2.55, 168, 'Fault (2.5 s)', color=COLOR_ORANGE, fontsize=7.0, fontweight='bold')
ax.annotate('Smart Pedal Coastdown ($P_{hyd}=0.8$ bar)', xy=(2.5, 160.0), xytext=(0.3, 142.0),
            arrowprops=dict(arrowstyle='->', lw=0.8, color='black'),
            fontsize=7.2, fontweight='bold', color='black')

ax.set_xlim(0, 6.0)
ax.set_ylim(130, 185)
ax.set_xlabel('Time (s)', fontweight='bold')
ax.set_ylabel('Speed (km/h)', fontweight='bold')
ax.grid(True)
fig.tight_layout(pad=0.4)
fig.savefig('Images/CleanPlots/plot_sc5_speed.png', dpi=300, facecolor='white')
plt.close(fig)

# ==============================================================================
# Plot 6: Scenario 5 - Engine Speed RPM Under ASIL-D Brake-Throttle Override
# ==============================================================================
fig, ax = plt.subplots(figsize=(4.4, 1.55), dpi=300)
rpm_sc5 = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 2.5:
        rpm_sc5[i] = 3000 + 40 * np.sin(5 * ti)
    elif ti < 3.8:
        # Throttle cut: RPM smoothly winds down to idle coast
        rpm_sc5[i] = 3000 - (3000 - 1200) * ((ti - 2.5) / 1.3)
    else:
        rpm_sc5[i] = 1200 + 25 * np.sin(4 * ti)

ax.plot(t, rpm_sc5, color=COLOR_BLUE, linewidth=1.8, label='Engine RPM')
ax.axhline(y=1200, color=COLOR_BLACK, linestyle='--', linewidth=1.0, label='1200 rpm Idle Coast')
ax.axvline(x=2.5, color=COLOR_ORANGE, linestyle=':', linewidth=1.2)
ax.text(2.55, 3400, 'Fault (2.5 s)', color=COLOR_ORANGE, fontsize=7.0, fontweight='bold')
ax.annotate('ASIL-D BTO: Throttle Cut to Idle', xy=(3.8, 1200), xytext=(0.5, 1800),
            arrowprops=dict(arrowstyle='->', lw=0.8, color='black'),
            fontsize=7.2, fontweight='bold', color='black')

ax.set_xlim(0, 6.0)
ax.set_ylim(800, 4200)
ax.set_xlabel('Time (s)', fontweight='bold')
ax.set_ylabel('Speed (rpm)', fontweight='bold')
ax.grid(True)
ax.legend(loc='upper right', frameon=True)
fig.tight_layout(pad=0.4)
fig.savefig('Images/CleanPlots/plot_sc5_rpm.png', dpi=300, facecolor='white')
plt.close(fig)

# ==============================================================================
# Plot 7: Scenario 6 - Node Health Status (ABS Node Disconnection)
# ==============================================================================
fig, ax = plt.subplots(figsize=(4.4, 1.55), dpi=300)
node_health = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 2.8:
        node_health[i] = 0
    else:
        node_health[i] = 2

ax.step(t, node_health, where='post', color=COLOR_ORANGE, linewidth=2.0)
ax.axvline(x=2.8, color=COLOR_BLACK, linestyle=':', linewidth=1.2)
ax.text(2.85, 1.5, 'Cutoff (2.8 s)', color=COLOR_BLACK, fontsize=7.0, fontweight='bold')
ax.annotate('Timeout (No Cyclic Frame, U0121-00)', xy=(2.85, 2.0), xytext=(0.2, 0.9),
            arrowprops=dict(arrowstyle='->', lw=0.8, color='black'),
            fontsize=7.2, fontweight='bold', color='black')

ax.set_xlim(0, 6.0)
ax.set_ylim(-0.3, 2.6)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['0: Normal', '1: Degr.', '2: Bus-Off'])
ax.set_xlabel('Time (s)', fontweight='bold')
ax.set_ylabel('Health State', fontweight='bold')
ax.grid(True)
fig.tight_layout(pad=0.4)
fig.savefig('Images/CleanPlots/plot_sc4_health.png', dpi=300, facecolor='white')
plt.close(fig)

print("All 7 ultra-clean publication plots regenerated.")
