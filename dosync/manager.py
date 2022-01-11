from datetime import datetime
from dataclasses import dataclass

from dosync.models import Campaign, Adset, Metadata
from dosync.decorators import database, should_update


@dataclass
class DosyncManager:
    """Dosync manager used to fetch and update information to the local database"""
    last_updated_at = None

    
    @should_update
    def update(self, client, data):
        """Update campaign in database from remote API"""
        print("⏬ Sync campaign {} to database".format(data['id']))
        
        adsets = client.get_adsets(campaign_id=data['id'])
        for idx, adset in enumerate(adsets):
            keywords = client.get_keywords(campaign_id=data['id'], adset_id=adset['id'])
            ads = client.get_ads(campaign_id=data['id'], adset_id=adset['id'])
            adset = Adset(**adset, keywords=keywords, ads=ads)
            adsets[idx] = adset

        campaign = Campaign(**data, adsets=adsets)
        campaign.save()
        return True


    def sync_down(self):
        """Update sync down datetime in database and return previous value"""
        return self.sync_update(field="syncDownAt")


    def sync_up(self):
        """Update sync up datetime in database and return previous value"""
        return self.sync_update(field="syncUpAt")


    @database
    def sync_update(self, field):
        """Update sync datetime in database and return previous value"""
        data = {}
        data[field] = datetime.now()
        result = Metadata._get_collection().find_one_and_update(
            filter={'_id': 1},
            update={'$set': data},
            upsert=True
        )

        if result and field in result:
            return result[field]

        return None