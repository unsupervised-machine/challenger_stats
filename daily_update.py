import schedule
import time
from datetime import datetime, timedelta
import asyncio
from backend.app.services.services import (update_league_data, update_player_ids_data, update_match_ids,
                                           update_match_detail, update_player_match_history,
                                           update_player_summarized_stats, update_ladder_data)


def update_database():
    try:
        # Your database update logic here
        asyncio.run(update_league_data())
        asyncio.run(update_player_ids_data())
        asyncio.run(update_match_ids())
        asyncio.run(update_match_detail())
        asyncio.run(update_player_match_history())
        asyncio.run(update_player_summarized_stats())
        asyncio.run(update_ladder_data())
        # Simulate a database update operation
        # Replace this with your actual database update code
    except Exception as e:
        print(f"Error updating database: {e}")

### FOR TESTING
# Run schedule in job in 1 minute
# Calculate the time for one minute from now
future_time = datetime.now() + timedelta(minutes=1)
formatted_time = future_time.strftime("%H:%M")

# Schedule the update function to run in 1 minute
schedule.every().day.at(formatted_time).do(update_database)
### END TESTING


# Schedule the update function to run once a day at a specific time
# schedule.every().day.at("00:00").do(update_database)  # Adjust the time as needed

if __name__ == "__main__":
    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(300)  # Sleep for a bit to prevent high CPU usage
