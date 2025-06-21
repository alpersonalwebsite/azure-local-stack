import argparse
import os
import platform
import subprocess
import time
import yaml
from dotenv import load_dotenv

DOCKER_COMPOSE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../docker-compose.yml")
GENERATE_COMPOSE_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_compose.py")

# Load environment variables from .env file if it exists
load_dotenv()

def is_windows():
    """Check if the operating system is Windows."""
    return platform.system().lower() == "windows"

def get_docker_compose_command():
    """Get the Docker Compose command based on the operating system."""
    return "docker-compose" if not is_windows() else "docker compose"

def is_valid_yaml(file_path):
    """Check if the given file path exists and is a valid YAML file."""
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        return True
    except Exception:
        return False

def ensure_compose_file():
    """Ensure the docker-compose.yml file exists and is valid. If not, generate it from the template."""
    if not os.path.exists(DOCKER_COMPOSE_FILE) or not is_valid_yaml(DOCKER_COMPOSE_FILE):
        print("docker-compose.yml not found or invalid. Generating from template...")
        subprocess.run(["python", GENERATE_COMPOSE_SCRIPT], check=True)

def run_docker_compose(services):
    """Run Docker Compose for the given services, building images if necessary."""
    ensure_compose_file()
    if not is_valid_yaml(DOCKER_COMPOSE_FILE):
        print("docker-compose.yml is invalid. Aborting docker-compose up.")
        return
    try:
        print(f"Starting Docker Compose for services: {services}...")
        subprocess.run([get_docker_compose_command(), "up", "--build", "-d"] + services, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running docker-compose: {e}")
        exit(1)

def stop_and_cleanup():
    """Stop and remove all containers defined in the stack, and delete the docker-compose.yml file."""
    if os.path.exists(DOCKER_COMPOSE_FILE):
        if is_valid_yaml(DOCKER_COMPOSE_FILE):
            try:
                subprocess.run([get_docker_compose_command(), "down"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running docker-compose down: {e}")
        else:
            print("docker-compose.yml is invalid. Skipping docker-compose down.")
        os.remove(DOCKER_COMPOSE_FILE)
        print("docker-compose.yml deleted.")
    else:
        print("docker-compose.yml not found. Nothing to stop or delete.")

def main():
    """Main entry point of the script. Parse arguments and manage the Azure Local Stack."""
    parser = argparse.ArgumentParser(description="Manage the Azure Local Stack.")
    parser.add_argument(
        "--mongodb-as-cosmosdb",
        action="store_true",
        help="Use MongoDB as a replacement for Cosmos DB.",
    )
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop and remove all containers defined in the stack.",
    )
    args = parser.parse_args()

    if args.stop:
        stop_and_cleanup()
        return

    if args.mongodb_as_cosmosdb:
        subprocess.run(["python", GENERATE_COMPOSE_SCRIPT], check=True)
        run_docker_compose(["mongodb-as-cosmosdb", "azurite"])
    else:
        subprocess.run(["python", GENERATE_COMPOSE_SCRIPT], check=True)
        run_docker_compose(["cosmosdb", "azurite"])
        print("\nIf you are having issues with the CosmosDB Emulator, you can set up MongoDB as CosmosDB with:\n  python scripts/manage_stack.py --mongodb-as-cosmosdb\n")

if __name__ == "__main__":
    main()
