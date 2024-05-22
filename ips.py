import redis
import time
import sys
from util import restart_service

def block_ips(ip_addresses):
    unique_ips = list(set(ip_addresses))  # Convert list to set to remove duplicates, then back to list
    if unique_ips:  # Only proceed if there are unique IPs to block
        try:
            with open("/etc/banip/banip.blocklist", "a") as file:
                for ip_address in unique_ips:
                    file.write(ip_address + "\n")
            restart_service('banip')
            print(f"Blocked {len(unique_ips)} unique IPs and restarted the service.")
        except Exception as e:
            print(f"Failed to append IPs to blocklist: {e}", file=sys.stderr)
            
# Connect to Redis
redis_host = "192.168.1.50"
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

list_key = 'router-block'
batch_time = 5  # Batch processing time in seconds

try:
    ip_batch = []
    last_time = time.time()
    
    while True:
        if (time.time() - last_time) >= batch_time and len(ip_batch):
            block_ips(ip_batch)
            ip_batch = []  # Clear the current batch
            last_time = time.time()  # Reset timer after processing

        log = r.blpop(list_key, timeout=1)  # Short timeout for blpop
        if log:
            ip_batch.append(log[1])
            print("Queued IP for blocking: {}".format(log[1]))

except KeyboardInterrupt:
    print("Stopped by the user.")
    if ip_batch:  # Ensure to block remaining IPs before exiting
        block_ips(ip_batch)
except Exception as e:
    print(f"An error occurred: {e}")
