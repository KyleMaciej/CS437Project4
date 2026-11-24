import json
import logging
import sys
import time

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# SDK Client
client = GreengrassCoreIPCClientV2()

def lambda_handler(event, context):
    # TODO1: Get your data
    raw_output = event.message.payload
    possible_payload = json.loads(raw_output.decode("utf-8") if isinstance(raw_output, bytes) else str(raw_output))
    
    if isinstance(possible_payload, str):
        possible_payload = json.loads(possible_payload)

    rows = possible_payload if isinstance(possible_payload, list) else [possible_payload]
    # TODO2: Calculate max CO2 emission
    maxCounter = 0.0
    vehicle_stat = None
    for record in rows:
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
    lambda_handler(event, None)


if __name__ == "__main__":
    client.subscribe_to_iot_core(
        topic_name="vehicle/emission/data",
        qos="1",
        on_stream_event=_on_stream_event,
    )
    while True:
        time.sleep(10)
