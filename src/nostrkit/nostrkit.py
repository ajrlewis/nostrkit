import json
import ssl
import time

from loguru import logger
from nostr.event import Event,EventKind
from nostr.filter import Filter, Filters
from nostr.key import PrivateKey, PublicKey
from nostr.message_type import ClientMessageType
from nostr.relay_manager import RelayManager

RELAYS = [
    # "wss://nostr-pub.wellorder.net/",
    # "wss://nostr.wine/",
    # "wss://purplepag.es/",
    # "wss://relay.primal.net/",
    # "wss://relay.snort.social/",
    # "wss://nos.lol/",
    # "wss://nostr.bitcoiner.social/",
    # "wss://relay.primal.net",
    # "wss://relay.damus.io/",
    # "wss://nostr.orangepill.dev/",
    # "wss://relay.current.fyi/",
    # "wss://relay.nostr.band/",
    # "wss://nostr01.counterclockwise.io"
    "wss://nostr.mom"
]


def get_private_public_keys(nsec: str = "") -> tuple[PrivateKey, PublicKey]:
    if nsec:
        logger.info(f"Generating private key from supplied {nsec = } ...")
        private_key = PrivateKey.from_nsec(nsec)
    else:
        private_key = PrivateKey()
    public_key = private_key.public_key
    logger.info(f"{private_key.bech32() = }")
    logger.info(f"{public_key.bech32() = }")
    return private_key, public_key


def connect_to_relay() -> RelayManager:
    relay_manager = RelayManager()
    for relay in RELAYS:
        relay_manager.add_relay(relay)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    # time.sleep(1.25)  # allow the connections to open
    time.sleep(2.0)  # allow the connections to open
    logger.info(f"{relay_manager = }")
    return relay_manager


def disconnect_relay(relay_manager: RelayManager):
    relay_manager.close_connections()


def get_events(
    private_key: str,
    content: str = "Hello World!",
    kind: int = 1,
    tags: list[list[str]] = [],
):
    relay_manager = connect_to_relay()
    event = Event(content, kind=kind, tags=tags)
    # event = Event(content, kind=kind, tags=tags)
    logger.debug(f"{event = }")
    private_key.sign_event(event)
    logger.debug(f"{event = }")
    relay_manager.publish_event(event)
    # time.sleep(1.0)  # allow the messages to send
    time.sleep(2.0)  # allow the messages to send

    disconnect_relay(relay_manager)


def post_event(
    private_key: str,
    content: str = "Hello World!",
    kind: int = 1,
    tags: list[list[str]] = [],
):
    relay_manager = connect_to_relay()
    event = Event(content, kind=kind, tags=tags)
    # event = Event(content, kind=kind, tags=tags)
    logger.debug(f"{event = }")
    private_key.sign_event(event)
    logger.debug(f"{event = }")
    relay_manager.publish_event(event)
    # time.sleep(1.0)  # allow the messages to send
    time.sleep(2.0)  # allow the messages to send

    disconnect_relay(relay_manager)

def get_events():

    filters = Filters([Filter(authors=[<a nostr pubkey in hex>], kinds=[EventKind.TEXT_NOTE])])
    subscription_id = <a string to identify a subscription>
    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())

relay_manager = RelayManager()
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_subscription(subscription_id, filters)
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25) # allow the connections to open

message = json.dumps(request)
relay_manager.publish_message(message)
time.sleep(1) # allow the messages to send

while relay_manager.message_pool.has_events():
  event_msg = relay_manager.message_pool.get_event()
  print(event_msg.event.content)
  
relay_manager.close_connections()



def main():
    # private_key, public_key = generate_private_public_keys()
    # logger.debug(f"{private_key = }")
    # publish_event(private_key)
    private_key = "nsec1uw0att3s0yasmyw3m3q2p8ws9qxzdkeh6u743c7u9gn5ynjmlulszjusfx"

    # nsec1uw0att3s0yasmyw3m3q2p8ws9qxzdkeh6u743c7u9gn5ynjmlulszjusfx
    # npub19ccv5fe7rn22cwasygsjkd5f0l64wv3fsw5jxtemvukfznfjtfvq0jmwsh
    # https://satellite.earth/@npub19ccv5fe7rn22cwasygsjkd5f0l64wv3fsw5jxtemvukfznfjtfvq0jmwsh

    private_key, public_key = get_private_public_keys(nsec=private_key)
    logger.debug(f"{private_key.bech32() = }")
    logger.debug(f"{public_key.bech32() = }")


if __name__ == "__main__":
    main()
