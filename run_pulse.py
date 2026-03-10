import subprocess
import time

# How often to refresh the data (in seconds). 300 = every 5 minutes.
REFRESH_INTERVAL = 300

def run_all_engines():
    print(f"\n--- Pulse Update: {time.ctime()} ---")

    steps = [
        ("Flight Data (ABQ Sunport)",   ["python", "engine.py"]),
        ("Transit Data (CABQ)",          ["python", "transit_pulse.py"]),
        ("NM Grid Calculation",          ["python", "generate_nm_grid.py"]),
    ]

    for label, cmd in steps:
        print(f"  → {label}...")
        result = subprocess.run(cmd, capture_output=False)
        if result.returncode != 0:
            print(f"  ⚠️  {label} exited with error code {result.returncode}. Continuing...")

    print(f"  ✓ Update complete. Next refresh in {REFRESH_INTERVAL // 60} minutes.")
    print(f"  ↳ Open index.html in a browser (via `python -m http.server 8000`) to see the live grid.")

if __name__ == "__main__":
    print("=== Who Up? NM Pulse — Starting Live Update Loop ===")
    print(f"    Refreshing every {REFRESH_INTERVAL // 60} minutes. Press Ctrl+C to stop.\n")

    while True:
        try:
            run_all_engines()
            time.sleep(REFRESH_INTERVAL)
        except KeyboardInterrupt:
            print("\n\nStopped by user. city_pulse.json has your last data.")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}. Retrying in 60 seconds...")
            time.sleep(60)
