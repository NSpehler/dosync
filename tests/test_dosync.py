import unittest

from datetime import datetime
from dotenv import load_dotenv
from mongoengine import connect, disconnect

from dosync.client import DosyncClient
from dosync.manager import DosyncManager
from dosync.models import Campaign

load_dotenv()


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')


    @classmethod
    def tearDownClass(cls):
       disconnect()


    def test_sync_down(self):
        client = DosyncClient()
        campaigns = client.get_campaigns()

        assert isinstance(campaigns, list)
        assert len(campaigns) != 0

        manager = DosyncManager()
        manager.update(client=client, data=campaigns[0])

        count = Campaign.objects().count()
        assert count == 1

        campaign = Campaign.objects().first()
        assert campaign.name == campaigns[0]['name']

        assert isinstance(campaign.adsets, list)
        assert len(campaign.adsets) != 0

        assert isinstance(campaign.adsets[0].keywords, list)
        assert len(campaign.adsets[0].keywords) != 0

        assert isinstance(campaign.adsets[0].ads, list)
        assert len(campaign.adsets[0].ads) != 0


    def test_sync_up(self):
        campaign_name = "nemo est voluptatum"
        Campaign.objects().first().update(
            name=campaign_name,
            updatedAt=datetime.now()
        )

        campaign = Campaign.objects().first()
        assert campaign.name == campaign_name

        client = DosyncClient()
        client.update(data=campaign)
        
        campaign = client.get_campaign(campaign_id=campaign['id'])
        assert campaign['name'] == campaign_name