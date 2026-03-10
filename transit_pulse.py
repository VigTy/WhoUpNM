from scrapling.fetchers import Fetcher
import json
import time

# Fetcher.get() is the correct class-method style for one-off HTTP requests.
# No need to instantiate — Fetcher handles it internally.

def get_transit_pulse():
    print("Checking ABQ Transit Index...")
    url = "https://data.cabq.gov/transit/realtime/"

    try:
        response = Fetcher.get(url, stealthy_headers=True)

        if not response or response.status != 200:
            print(f"Transit Error: Bad response ({response.status if response else 'No response'})")
            return 0

        # Count .html links in the directory index as a proxy for active route reports
        stations = response.css("a[href$='.html']").getall()
        station_count = len(stations)

        # Each active station report ~ 50 people commuting nearby
        commute_est = station_count * 50

        # Merge into city_pulse.json without overwriting flight data
        try:
            with open("city_pulse.json", "r") as f:
                pulse_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pulse_data = {}

        pulse_data["active_stations"] = station_count
        pulse_data["commute_estimate"] = commute_est
        pulse_data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

        with open("city_pulse.json", "w") as f:
            json.dump(pulse_data, f, indent=4)

        print(f"Found {station_count} active station reports. Commute estimate: {commute_est:,}. Data saved!")
        return station_count

    except Exception as e:
        print(f"Transit Error: {e}")
        return 0

if __name__ == "__main__":
    get_transit_pulse()
