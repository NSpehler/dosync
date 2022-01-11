import os
import json
import requests

from datetime import datetime
from dataclasses import dataclass

from dosync.decorators import delay, should_update


@dataclass
class DosyncClient:
    """Dosync client used to fetch and update information to the remote REST API"""
    session = requests.Session()
    last_updated_at = None


    def update(self, data):
        """Update specific campaign by ID"""
        self.update_campaign(
            campaign_id=data['id'],
            data=data.to_mongo().to_dict()
        )

        for adset in data.adsets:
            self.update_adset(
                campaign_id=data['id'],
                adset_id=adset['id'],
                data=adset.to_mongo().to_dict()
            )

            for keyword in adset.keywords:
                self.update_keyword(
                    campaign_id=data['id'],
                    adset_id=adset['id'],
                    keyword_id=keyword['id'],
                    data=keyword.to_mongo().to_dict()
                )

            for ad in adset.ads:
                self.update_ad(
                    campaign_id=data['id'],
                    adset_id=adset['id'],
                    ad_id=ad['id'],
                    data=ad.to_mongo().to_dict()
                )

        return True


    def get_campaigns(self):
        """Get all campaigns"""
        path = "campaigns"
        return self.query(method="GET", path=path)

    
    def get_campaign(self, campaign_id):
        """Get specific campaign by ID"""
        path = "campaigns/{}".format(campaign_id)
        return self.query(method="GET", path=path)


    @should_update
    def update_campaign(self, campaign_id, data):
        """Update specific campaign by ID"""
        print("⏫ Sync campaign {} to remote API".format(campaign_id))
        path = "campaigns/{}".format(campaign_id)
        return self.query(method="PUT", path=path, data=data)
        

    def get_adsets(self, campaign_id):
        """Get all adsets for a specific campaign ID"""
        path = "campaigns/{}/Adsets".format(campaign_id)
        return self.query(method="GET", path=path)


    @should_update
    def update_adset(self, campaign_id, adset_id, data):
        """Update specific adset by ID"""
        print("⏫ Sync adset {} to remote API".format(adset_id))
        path = "campaigns/{}/Adsets/{}".format(campaign_id, adset_id)
        return self.query(method="PUT", path=path, data=data)


    def get_keywords(self, campaign_id, adset_id):
        """Get all keywords for a specific campaign and adset ID"""
        path = "campaigns/{}/Adsets/{}/keywords".format(campaign_id, adset_id)
        return self.query(method="GET", path=path)


    @should_update
    def update_keyword(self, campaign_id, adset_id, keyword_id, data):
        """Update specific keyword by ID"""
        print("⏫ Sync keyword {} to remote API".format(keyword_id))
        path = "campaigns/{}/Adsets/{}/keywords/{}".format(campaign_id, adset_id, keyword_id)
        return self.query(method="PUT", path=path, data=data)


    def get_ads(self, campaign_id, adset_id):
        """Get all ads for a specific campaign and adset ID"""
        path = "campaigns/{}/Adsets/{}/ads".format(campaign_id, adset_id)
        return self.query(method="GET", path=path)


    @should_update
    def update_ad(self, campaign_id, adset_id, ad_id, data):
        """Update specific ad by ID"""
        print("⏫ Sync ad {} to remote API".format(ad_id))
        path = "campaigns/{}/Adsets/{}/ads/{}".format(campaign_id, adset_id, ad_id)
        return self.query(method="PUT", path=path, data=data)


    @delay
    def query(self, method, path, data = {}):
        path = "{}/{}".format(os.environ['API_URL'], path) 

        try:
            r = self.session.request(method, path, data=data)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        results = r.json()
        return results