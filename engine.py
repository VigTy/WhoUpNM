from scrapling import DynamicFetcher
import json
import time

def count_abq_flights():
    print("Connecting to ABQ Sunport...")
    url = "https://www.abqsunport.com/arrival-departures/"

    try:
        # THE FIX: Move headless=False here, inside the .fetch() call
        response = DynamicFetcher.fetch(url, headless=False, network_idle=True)

        if not response or response.status != 200:
            print(f"Engine Error: Bad response ({response.status if response else 'No response'})")
            return 0

        iframe_element = response.css('iframe[src*="fids"]').first
        if not iframe_element:
            print("Engine Error: Could not find the flight board iframe.")
            return 0

        frame_url = iframe_element.attrib.get('src')
        print(f"Found flight board. Loading dynamic data...")

        # Again, set headless=False here so you can see the table load
        frame_response = DynamicFetcher.fetch(frame_url, headless=False, network_idle=True)

        # Count rows, subtract 1 for the header
        flights = frame_response.css("tr").getall()
        flight_count = max(0, len(flights) - 1)

        if flight_count > 0:
            people_estimate = flight_count * 150

            # Merge into your existing JSON so we don't delete Transit data
            try:
                with open("city_pulse.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            data["active_flights"] = flight_count
            data["travelers_estimate"] = people_estimate
            data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

            with open("city_pulse.json", "w") as f:
                json.dump(data, f, indent=4)

            print(f"\n--- SUCCESS! ---")
            print(f"Found {flight_count} flights. Estimated {people_estimate:,} travelers.")
            return flight_count
        else:
            print("Engine Warning: Found 0 flights. Is the table visible in the window?")
            return 0

    except Exception as e:
        print(f"Engine Error: {e}")
        return 0

if __name__ == "__main__":
    count_abq_flights()