import json
import logging
import sys

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# SDK Client
client = GreengrassCoreIPCClientV2()

def lambda_handler(event, context):
    # TODO1: Get your data
    # TODO2: Calculate max CO2 emission
    maxCounter = 0.0
    for record in event:
        CO2_val = float(record['vehicle_CO2'])
        vehicle_stat = record['vehicle_id'] 

        if CO2_val > maxCounter:
            maxCounter = CO2_val
        
    # TODO3: Return the result
    client.publish_to_iot_core(
        topic_name="iot/Vehicle_" + vehicle_stat,
        qos="1",
        payload=json.dumps({"max_CO2": maxCounter}).encode("utf-8"),
    )

    return

def _on_stream_event(event) -> None:
    raw = event.message.payload
    payload = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
    lambda_handler(payload, None)


if __name__ == "__main__":
    client.subscribe_to_iot_core(
        topic_name="emissions",
        qos="1",
        on_stream_event=_on_stream_event,
    )
    while True:
        time.sleep(10)
