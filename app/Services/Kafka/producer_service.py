import json
from kafka import KafkaProducer
from typing import Any, Dict
from functools import lru_cache
import os

class KafkaProducerService:

    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(","),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda v: v.encode("utf-8") if isinstance(v, str) else v
        )

    def publish(self, topic: str, key: str, value: Dict[str, Any]):
        try:
            future = self._producer.send(topic, key=key, value=value)
            future.get(timeout=10)
        except Exception as ex:
            # In a production system: log, raise, or send to DLQ
            print(f"Kafka publish failed: {ex}")
            raise

    def flush(self):
        self._producer.flush()

@lru_cache() #TODO: Ensure that this is thread safe and creates only one instance in a multi-threaded environment
def get_kafka_producer() -> KafkaProducerService:
    return KafkaProducerService()
