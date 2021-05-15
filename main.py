from api import API
from sqlalchemy import create_engine
from datetime import datetime

if __name__ == "__main":
    # TODO: Connect to db
    conn = create_engine()
    
    # Create API object
    api = API()
    
    # Get current auctions
    auctions = api.get_auctions_for_realm(api.ZULJIN)
    
    # Upload auctions to db
    # auctions.to_sql("auctions", conn)
    
    # Write to csv file
    auctions.to_csv(f"{datetime.utcnow().strftime("mm-dd-YYYY-HH:MM")}-ZULZIN.csv")

    # TODO: Check db for item info
    # TODO: Get item info for new items
    # items = api.get_all_items_info(auctions.item_id.unique())