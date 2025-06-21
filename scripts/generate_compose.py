import json
import re
import os

TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), '../docker-compose.template.yml')
PORTS_FILE = os.path.join(os.path.dirname(__file__), '../ports.json')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../docker-compose.yml')

def validate_ports(ports):
    """Validate ports.json for duplicate host ports and required fields."""
    host_ports = set()
    errors = []
    for service, port_list in ports.items():
        if isinstance(port_list, dict):
            # Single port mapping (e.g., mongodb)
            host = port_list.get('host')
            container = port_list.get('container')
            if host is None or container is None:
                errors.append(f"Missing host/container for {service}")
            if host in host_ports:
                errors.append(f"Duplicate host port {host} for {service}")
            host_ports.add(host)
        elif isinstance(port_list, list):
            for port_map in port_list:
                host = port_map.get('host')
                container = port_map.get('container')
                if host is None or container is None:
                    errors.append(f"Missing host/container for {service}")
                if host in host_ports:
                    errors.append(f"Duplicate host port {host} for {service}")
                host_ports.add(host)
    return errors

def main():
    with open(TEMPLATE_FILE, 'r') as f:
        template = f.read()
    with open(PORTS_FILE, 'r') as f:
        ports = json.load(f)

    errors = validate_ports(ports)
    if errors:
        print("Error(s) in ports.json:")
        for err in errors:
            print(f"  - {err}")
        exit(1)

    mapping = {}
    # MongoDB as CosmosDB
    if 'mongodb' in ports and isinstance(ports['mongodb'], dict):
        mapping['MONGODB_AS_COSMOSDB_PORT'] = f"{ports['mongodb']['host']}:{ports['mongodb']['container']}"
        mapping['MONGODB_PORT'] = f"{ports['mongodb']['host']}:{ports['mongodb']['container']}"  # for backward compatibility
    # Storage
    for i, port_map in enumerate(ports.get('storage', []), 1):
        mapping[f'STORAGE_PORT_{i}'] = f"{port_map['host']}:{port_map['container']}"
    # CosmosDB
    for i, port_map in enumerate(ports.get('cosmosdb', []), 1):
        mapping[f'COSMOSDB_PORT_{i}'] = f"{port_map['host']}:{port_map['container']}"

    # Replace placeholders
    def replacer(match):
        key = match.group(1)
        return mapping.get(key, match.group(0))

    result = re.sub(r'\{\{(.*?)\}\}', replacer, template)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(result)
    print(f"Generated {OUTPUT_FILE} from template.")
    print("Port mappings used:")
    for k, v in mapping.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
