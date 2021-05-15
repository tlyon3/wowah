import pandas as pd
import requests
from datetime import datetime

class API():
    CLIENT_ID = '94feb4d068d34ab19bbb490bdb470cb4'
    SECRET = "rvi1q5YPAit7JZd81veKj71fFpC2gsET"
    TOKEN = "USIICRrJ0RO43HcCg6Js8agV1K8eBHsimn"
    TOKEN_REFRESH_COMMAND = f"curl -u {CLIENT_ID}:{SECRET} -d grant_type=client_credentials https://us.battle.net/oauth/token"
    ZULJIN = 61
    STORMRAGE = 60
    
    def __init__(self):
        TOKEN = self.refresh_token()
    
    def refresh_token(self):
        resp = requests.post("https://us.battle.net/oauth/token", auth=(CLIENT_ID, SECRET), params={'grant_type': "client_credentials"})
        return resp.json()['access_token']
    
    def get_auctions_for_realm(self, realm_id):
        full_url = base_url + ah_path.format(connectedRealmId = realm_id)
        resp = requests.get(full_url, params=query_params)
        auction_list = resp.json()['auctions']
        auctions = []
        for auction in auction_list:
            auctions.append({
                'auction_id': auction['id'],
                'item_id': auction['item']['id'],
                'bid': auction['bid'] if 'bid' in auction else np.nan,
                'buyout': auction['buyout'] if 'buyout' in auction else np.nan,
                'quantity': auction['quantity'],
                'time_left': auction['time_left']
            })
        df = pd.DataFrame.from_records(auctions)
        df['dt'] = datetime.utcnow()
        return df
        
        
    def get_item_info(self, item_id):
        qp = copy.copy(query_params)
        qp['namespace'] = 'static-us'
        full_url = base_url + f"/data/wow/item/{item_id}"
        resp = requests.get(full_url, params=qp)
        raw = resp.json()
        item = {
            "id": item_id,
            'sell_price': raw['sell_price'],
            'name': raw['name'],
            'item_class': raw['item_class']['name'],
            'item_subclass': raw['item_subclass']['name'],
            'purchase_price': raw['purchase_price'],
            'ilvl': raw['level'],
            'quality': raw['quality']['name']
        }
        return item
        
    def get_all_items_info(self, item_ids):
        items = []
        for id in item_ids:
            items.append(self.get_item_info(id))
        
        return pd.DataFrame.from_records(items)