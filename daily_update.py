import schedule
import time
from datetime import datetime, timedelta
import asyncio
from backend.app.services.services import update_match_detail


def update_database():
    try:
        # Your database update logic here
        asyncio.run(update_match_detail())
        # Simulate a database update operation
        # Replace this with your actual database update code
    except Exception as e:
        print(f"Error updating database: {e}")

### FOR TESTING
# Calculate the time for one minute from now
future_time = datetime.now() + timedelta(minutes=1)
formatted_time = future_time.strftime("%H:%M")

# Schedule the update function to run in 1 minute
# schedule.every().day.at(formatted_time).do(update_database)
### END TESTING


# Schedule the update function to run once a day at a specific time
schedule.every().day.at("00:00").do(update_database)  # Adjust the time as needed

if __name__ == "__main__":
    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(300)  # Sleep for a bit to prevent high CPU usage
