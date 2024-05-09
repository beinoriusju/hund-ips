import redis
import json
import sys
import subprocess

def restart_service(service_name):
    try:
        # Uses systemctl to restart the service
        result = subprocess.run(['service', service_name, 'restart'], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Service {service_name} restarted successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Handles cases where the restart command fails
        print(f"Failed to restart service {service_name}. Error: {e.stderr}")
    except Exception as e:
        # Generic exception handling for other unexpected errors
        print(f"An unexpected error occurred: {e}")

def block_ip(ip_address):
    # Ensure the directory exists and handle cases where it might not
    try:
        with open("/etc/banip/banip.blocklist", "a") as file:
            file.write(ip_address + "\n")
        restart_service('banip')
    except Exception as e:
        print(f"Failed to append IP to blocklist: {e}", file=sys.stderr)


# Connect to Redis
redis_host = "192.168.1.50"
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Key name where Suricata logs are pushed
list_key = 'suricata'

# Continuously read and print logs
try:
    while True:
        # Retrieve log from Redis list (blocking operation)
        log = r.blpop(list_key, timeout=0)
        event = json.loads(log[1])
        if event['event_type'] != 'alert' or event['alert']['severity'] > 2:
            continue;
 
        print(json.dumps(event, indent=4))
        
        if event['alert']['severity'] == 1:    
            print("Blocking IP {}".format(event['src_ip']))
            block_ip(event['src_ip'])
except KeyboardInterrupt:
    print("Stopped by the user.")

except Exception as e:
    print(f"An error occurred: {e}")

