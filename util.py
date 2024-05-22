import subprocess

def restart_service(service_name):
    try:
        # Uses systemctl to restart the service
        result = subprocess.run(['service', service_name, 'restart'], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Service {service_name} restarted successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Handles cases where the restart command fails
        print(e)
        print(f"Failed to restart service {service_name}. Error: {e.stderr}")
    except Exception as e:
        # Generic exception handling for other unexpected errors
        print(f"An unexpected error occurred: {e}")