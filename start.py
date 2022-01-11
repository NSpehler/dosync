from dotenv import load_dotenv

from dosync.models import Campaign
from dosync.decorators import database
from dosync.client import DosyncClient
from dosync.manager import DosyncManager
from dosync.utils import color

load_dotenv()


@database
def start():
    client = DosyncClient()

    # Sync campaigns from remote API to database
    sync_down(client=client)

    # Sync local changes in database to remote API
    sync_up(client=client)

    print(color.BOLD + "🏁 Sync successful" + color.END)
    return True


@database
def sync_down(client):
    print(color.BOLD + "⏬ Sync remote API to database" + color.END)
    
    manager = DosyncManager()
    manager.last_updated_at = manager.sync_down()
    campaigns = client.get_campaigns()

    for campaign in campaigns:
        manager.update(client=client, data=campaign)

    return True


@database
def sync_up(client):
    print(color.BOLD + "⏫ Sync database to remote API" + color.END)

    manager = DosyncManager()
    client.last_updated_at = manager.sync_up()

    for campaign in Campaign.objects:
        client.update(data=campaign)

    return True


if __name__ == "__main__":
    start()