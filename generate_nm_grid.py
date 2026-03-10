import json
from datetime import datetime

def get_time_based_percentages():
    """
    Returns (work_pct, leisure_pct) based on the current hour in Mountain Time.
    These are rough approximations of NM workforce activity patterns.
    """
    hour = datetime.now().hour  # Local machine time (run this in MDT/MST)

    if 0 <= hour < 6:       # Late night / early morning
        return 0.02, 0.88   # Almost nobody working, most asleep (leisure bucket)
    elif 6 <= hour < 9:     # Morning commute
        return 0.25, 0.50
    elif 9 <= hour < 17:    # Core work hours
        return 0.60, 0.25
    elif 17 <= hour < 20:   # Evening wind-down
        return 0.20, 0.55
    else:                   # Late evening (8 PM – midnight)
        return 0.05, 0.75

def calculate_nm_pulse():
    # Load live scraped data
    try:
        with open("city_pulse.json", "r") as f:
            live_data = json.load(f)
    except FileNotFoundError:
        print("city_pulse.json not found — run engine.py and transit_pulse.py first!")
        return
    except json.JSONDecodeError:
        print("city_pulse.json is corrupted. Re-run the scrape engines.")
        return

    total_pop = 665000  # ABQ + Rio Rancho combined estimate

    travelers = live_data.get("travelers_estimate", 0)
    commuters = live_data.get("commute_estimate", 0)
    total_traveling = travelers + commuters

    work_pct, leisure_pct = get_time_based_percentages()

    working = int(total_pop * work_pct)
    eating_chores = int(total_pop * 0.05)
    leisure = int(total_pop * leisure_pct)
    # Remaining people are "other" — caregiving, errands, etc.
    # We clamp to avoid negatives if travel is unusually high
    traveling_clamped = min(total_traveling, total_pop - working - eating_chores - leisure)

    now_str = datetime.now().strftime("%I:%M %p")

    print(f"\n--- WHO UP: NEW MEXICO EDITION ({now_str}) ---")
    print(f"Total Population:   {total_pop:,}")
    print(f"------------------------------------------")
    print(f"💼 Work:    {working:,} people ({work_pct*100:.0f}%)")
    print(f"✈️  Travel:  {traveling_clamped:,} people")
    print(f"🍔 Eating:  {eating_chores:,} people")
    print(f"🎮 Leisure: {leisure:,} people ({leisure_pct*100:.0f}%)")

    # Write updated grid data back to city_pulse.json for the HTML dashboard
    live_data["grid"] = {
        "work":    working // 1000,
        "travel":  traveling_clamped // 1000,
        "eating":  eating_chores // 1000,
        "leisure": leisure // 1000,
        "total":   total_pop // 1000
    }

    with open("city_pulse.json", "w") as f:
        json.dump(live_data, f, indent=4)

    print(f"\nGrid data written to city_pulse.json ✓")

if __name__ == "__main__":
    calculate_nm_pulse()
