#!/usr/bin/env python3
"""
Real-Time Dynamic Engine Sound Synthesizer
==========================================
Simulates internal combustion engine (ICE) acoustics strictly synchronized
with accelerator pedal, transmission gear, and vehicle speed from CANoe.
"""

import sys
import os
import math
import struct
import time
import argparse

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

def sync_engine_audio():
    """
    Plays realistic engine audio synchronized in real time with Sim_AcceleratorPedal,
    vehicle speed, and transmission gear.
    Stops immediately when accelerator pedal is released (active == 0) or brake pressed.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ctl_file = os.path.normpath(os.path.join(script_dir, "engine_sound_ctl.txt"))
    pid_file = os.path.normpath(os.path.join(script_dir, "engine_sound.pid"))
    
    my_pid = str(os.getpid())
    try:
        with open(pid_file, "w") as f:
            f.write(my_pid)
    except Exception:
        pass
    
    def read_ctl():
        if not os.path.exists(ctl_file):
            return 0, 0.0, 1, 0.0
        try:
            with open(ctl_file, "r") as f:
                parts = f.readline().strip().split()
                if len(parts) >= 4:
                    return int(parts[0]), float(parts[1]), int(parts[2]), float(parts[3])
                elif len(parts) >= 1:
                    return int(parts[0]), 0.0, 1, 0.0
        except Exception:
            pass
        return 0, 0.0, 1, 0.0

    active, pedal, gear, speed = read_ctl()
    if active == 0:
        return

    current_gear = max(1, min(5, gear))
    gear_wavs = {
        1: os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_gear1.wav")),
        2: os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_gear2.wav")),
        3: os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_gear3.wav")),
        4: os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_gear4.wav")),
        5: os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_gear5.wav")),
    }
    decel_wav = os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_decel.wav"))
    fallback_wav = os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_accel_gearchange.wav"))

    # Select starting gear file
    wav_path = gear_wavs.get(current_gear, fallback_wav)
    if not os.path.exists(wav_path):
        wav_path = fallback_wav

    if HAS_WINSOUND and os.path.exists(wav_path):
        winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    start_time = time.time()
    last_gear = current_gear

    while True:
        time.sleep(0.06) # 60ms polling
        
        # Check if newer process took over
        try:
            if os.path.exists(pid_file):
                with open(pid_file, "r") as f:
                    if f.read().strip() != my_pid:
                        break
        except Exception:
            pass
            
        active, pedal, gear, speed = read_ctl()
        
        # Throttle released or brake pressed -> CUT ACCELERATION AUDIO IMMEDIATELY!
        if active == 0:
            if HAS_WINSOUND:
                winsound.PlaySound(None, 0) # Halt rev immediately
                if os.path.exists(decel_wav):
                    winsound.PlaySound(decel_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    time.sleep(0.7)
                    winsound.PlaySound(None, 0)
            break
            
        # Gear shifted -> switch to new gear audio seamlessly
        new_gear = max(1, min(5, gear))
        if new_gear != last_gear:
            last_gear = new_gear
            wav_path = gear_wavs.get(new_gear, fallback_wav)
            if HAS_WINSOUND and os.path.exists(wav_path):
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                start_time = time.time()

        # If audio reached end of track but pedal still pressed, loop current gear
        if time.time() - start_time > 3.4:
            if HAS_WINSOUND and os.path.exists(wav_path):
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                start_time = time.time()

    # Clean up pid file if still owned
    try:
        if os.path.exists(pid_file):
            with open(pid_file, "r") as f:
                if f.read().strip() == my_pid:
                    os.remove(pid_file)
    except Exception:
        pass

def play_pregenerated_audio(wav_path=None):
    if wav_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        wav_path = os.path.normpath(os.path.join(script_dir, "..", "Audio", "engine_accel_gearchange.wav"))
    
    if os.path.exists(wav_path):
        if HAS_WINSOUND:
            try:
                import wave
                with wave.open(wav_path, "rb") as w:
                    duration = w.getnframes() / float(w.getframerate())
            except Exception:
                duration = 20.0
            
            try:
                if sys.stdout is not None:
                    print(f"[AUDIO] Playing engine acceleration track ({duration:.1f}s): {wav_path}")
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                time.sleep(duration)
                winsound.PlaySound(None, 0)
                return True
            except Exception:
                pass
        
        try:
            import subprocess
            cmd = f"$p = [System.Media.SoundPlayer]::new('{wav_path}'); $p.PlaySync()"
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", cmd], check=True)
            return True
        except Exception:
            pass
    return False

def simulate_realtime_revs():
    """Generates real-time sound curve simulation for terminal demonstration."""
    print("=" * 65)
    print("  AUTOMOTIVE ENGINE SOUND SYNTHESIZER - 5-GEAR ACCELERATION")
    print("=" * 65)
    
    gears = [
        (1, 0, 25, 850, 3200, 3.0),
        (2, 25, 50, 1800, 3200, 3.2),
        (3, 50, 75, 1900, 3200, 3.5),
        (4, 75, 100, 2000, 3200, 3.8),
        (5, 100, 130, 2200, 2800, 2.5),
    ]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wav_path = os.path.join(script_dir, "..", "Audio", "engine_accel_gearchange.wav")
    
    if os.path.exists(wav_path) and HAS_WINSOUND:
        winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    start_time = time.time()
    for gear, min_spd, max_spd, min_rpm, max_rpm, dur in gears:
        steps = 15
        dt = dur / steps
        for s in range(steps):
            frac = s / float(steps)
            curr_rpm = min_rpm + frac * (max_rpm - min_rpm)
            curr_spd = min_spd + frac * (max_spd - min_spd)
            bar = "#" * int(curr_rpm / 120)
            sys.stdout.write(f"\r[GEAR {gear}] Speed: {curr_spd:5.1f} km/h | RPM: {curr_rpm:6.1f} [{bar:<30}]")
            sys.stdout.flush()
            time.sleep(dt)
        print(f"\n >>> SHIFT POINT: Gear {gear} -> {gear+1} | RPM drop: {max_rpm} -> {gears[min(gear, 4)][3]} RPM")
        time.sleep(0.25)
        
    print("\n[AUDIO] Vehicle reached cruising state. Coasting to idle.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-Time Engine Sound Generator")
    parser.add_argument("--sync", action="store_true", help="Synchronize audio with pedal/gear state file")
    parser.add_argument("--play", action="store_true", help="Play audio file immediately")
    parser.add_argument("--sim", action="store_true", help="Simulate gear acceleration profile with sound")
    args = parser.parse_args()
    
    if args.sync:
        sync_engine_audio()
    elif args.play:
        play_pregenerated_audio()
    elif args.sim:
        simulate_realtime_revs()
    else:
        sync_engine_audio()
