# Azure Local Stack

This project simulates Azure services locally using Docker Compose and Python. It is designed to be cross-platform and easy to use for development and testing purposes.

## Features
- Simulates multiple Azure services locally.
- Uses Docker Compose for service orchestration.
- Python-based management script for easy setup and control.
- Cross-platform compatibility.

## Updated Project Structure

```
azure-local-stack/
├── docker-compose.template.yml   # Template for Docker Compose, edited by user
├── docker-compose.yml            # Generated Docker Compose file (do not edit directly)
├── ports.json                    # Host/container port mappings for all services
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore rules (should include .env, secrets, etc.)
├── scripts/                      # Python scripts for managing the stack
│   ├── manage_stack.py           # Main management script (start/stop stack)
│   ├── generate_compose.py       # Generates docker-compose.yml from template and ports.json
│   └── ...                       # (Other utility scripts, if any)
├── services/                     # Directory for service-specific configs (optional)
│   ├── storage/                  # Example: Azure Storage Emulator
│   ├── cosmosdb/                 # Example: Azure Cosmos DB Emulator
│   └── ...                       # Add more services as needed
└── reports/                      # Directory for storing scan reports (optional)
    └── <repository_name>/        # Subdirectories for each repository
        └── <timestamp>/          # Timestamped directories for each scan
            ├── <tool>.json       # Individual tool reports
            └── summary.html      # Summary report
```

- **Edit only** `docker-compose.template.yml` and `ports.json` for configuration.
- **Never edit** `docker-compose.yml` directly; it is auto-generated.
- Use `scripts/manage_stack.py` to start/stop the stack and generate the compose file.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.8 or higher.

### Setup

#### Installing Python Dependencies

Before running the Python scripts, ensure you have installed the required dependencies. 
Use the following command:

```bash
pip install -r requirements.txt
```

#### Optional: Setting Up a Virtual Environment

It is recommended to create a Python virtual environment to isolate dependencies. Follow these steps:

1. Create a virtual environment:
   ```bash
    python3 -m venv ~/venvs/azure-local-stack

   ```

2. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source ~/venvs/azure-local-stack/bin/activate
     ```
   - On Windows:
     ```bash
     C:\Users\YourName\venvs\azure-local-stack\Scripts\activate.bat

     # For Powershell
     # C:\Users\YourName\venvs\azure-local-stack\Scripts\Activate.ps1
     ```

3. Install any required dependencies (if applicable):
   ```bash
   pip install -r requirements.txt
   ```

3. Optional, when needed: Deactivate environment

     ```bash
     deactivate
     ```

#### Setup the service

1. To start the stack with the default configuration:
   ```bash
   python scripts/manage_stack.py
   ```

   1. To use MongoDB as a replacement for Cosmos DB:
      ```bash
      python scripts/manage_stack.py --mongodb-as-cosmosdb
      ```

2. Optional, when needed: stop 

```bash
python scripts/manage_stack.py --stop 
```

### Environment Modes

The script supports two modes of operation:

1. **Development Mode**:
   - Uses Azurite for local development.
   - No additional setup is required for Azurite.
   - Default configuration:
     - `STORAGE_ACCOUNT_NAME`: `devstoreaccount1`
     - `STORAGE_ACCOUNT_KEY`: `Eby8vdM02xNOcqFeqCUzHQ==`
     - `STORAGE_ACCOUNT_ENDPOINT`: `http://127.0.0.1:10000/devstoreaccount1`

2. **Production Mode**:
   - Uses Azure Blob Storage for production.
   - Requires the following environment variables to be set:
     - `STORAGE_ACCOUNT_NAME`: Your Azure storage account name.
     - `STORAGE_ACCOUNT_KEY`: Your Azure storage account key.
     - `STORAGE_ACCOUNT_ENDPOINT`: Derived from the account name (e.g., `https://mystorageaccount.blob.core.windows.net`).

### Environment Variables for Both Environments

The script uses the following environment variables for both development and production environments:

1. **`STORAGE_ACCOUNT_NAME`**:
   - **Development**: `devstoreaccount1`
   - **Production**: Your Azure storage account name (e.g., `mystorageaccount`).

2. **`STORAGE_ACCOUNT_KEY`**:
   - **Development**: `Eby8vdM02xNOcqFeqCUzHQ==`
   - **Production**: Your Azure storage account key (e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`).

3. **`STORAGE_ACCOUNT_ENDPOINT`**:
   - **Development**: `http://127.0.0.1:10000/devstoreaccount1`
   - **Production**: Automatically derived from the account name (e.g., `https://mystorageaccount.blob.core.windows.net`).

Set these variables before running the script to ensure proper configuration for the selected environment.

##### On Linux/macOS
You can set environment variables temporarily in the terminal:

```bash
export STORAGE_ACCOUNT_NAME="your_account_name"
export STORAGE_ACCOUNT_KEY="your_account_key"
```

To make these changes permanent, add them to your shell configuration file (e.g., `~/.bashrc` or `~/.zshrc`):

```bash
echo 'export STORAGE_ACCOUNT_NAME="your_account_name"' >> ~/.bashrc
echo 'export STORAGE_ACCOUNT_KEY="your_account_key"' >> ~/.bashrc
source ~/.bashrc
```


#### Updating the Docker Compose File with Platform Information

Before starting the services, ensure the `docker-compose.yml` file is updated with the correct platform information for your system. Run the following command:

```bash
python scripts/update_docker_compose.py
```

This script detects your system's platform (e.g., `linux/amd64` or `linux/arm64/v8`) and updates the `platform` field in the `docker-compose.yml` file accordingly.


### Managing the Azure Local Stack

You can use the `manage_stack.py` script to configure and run the Azure Local Stack. This script automates the following:
- Configures `docker-compose.yml` based on your requirements.
- Runs `docker-compose up --build` to start the stack.
- Checks the status of all containers and reports any issues.
- Provides an option to use MongoDB as a replacement for Cosmos DB.

### Example Services
- **Azure Storage Emulator**: Simulates Azure Blob, Queue, and Table storage.
- **Azure Cosmos DB Emulator**: Simulates Azure Cosmos DB.

## Software and Libraries Used

The Azure Local Stack project uses the following software and libraries:

1. **Azure Storage Emulator (Azurite)**:
   - Image: `mcr.microsoft.com/azure-storage/azurite`
   - Simulates Azure Blob, Queue, and Table storage.

2. **Azure Cosmos DB Emulator**:
   - Image: `mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator`
   - Simulates Azure Cosmos DB.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

#### On Windows
You can set environment variables temporarily in the Command Prompt:

```cmd
set AZURE_STORAGE_ACCOUNT_NAME=your_account_name
set AZURE_STORAGE_ACCOUNT_KEY=your_account_key
```

To make these changes permanent, use the System Properties:

1. Open the Start Menu and search for "Environment Variables."
2. Click "Edit the system environment variables."
3. In the System Properties window, click "Environment Variables."
4. Under "System variables," click "New" and add:
   - Variable name: `AZURE_STORAGE_ACCOUNT_NAME`
   - Variable value: `your_account_name`
5. Repeat for `AZURE_STORAGE_ACCOUNT_KEY`.
6. Click "OK" to save the changes.

### Updated Environment Variables for Azurite

The following environment variables are used for Azurite in development mode:

1. **`STORAGE_ACCOUNT_NAME`**:
   - Default: `devstoreaccount1`
   - Example: `export STORAGE_ACCOUNT_NAME="devstoreaccount1"`

2. **`STORAGE_ACCOUNT_KEY`**:
   - Default: `Eby8vdM02xNOcqFeqCUzHQ==`
   - Example: `export STORAGE_ACCOUNT_KEY="Eby8vdM02xNOcqFeqCUzHQ=="`

3. **`STORAGE_ACCOUNT_ENDPOINT`**:
   - Default: `http://127.0.0.1:10000/devstoreaccount1`
   - Example: `export STORAGE_ACCOUNT_ENDPOINT="http://127.0.0.1:10000/devstoreaccount1"`

These variables should be set before running the stack to ensure proper configuration. For example:

```bash
export STORAGE_ACCOUNT_NAME="devstoreaccount1"
export STORAGE_ACCOUNT_KEY="Eby8vdM02xNOcqFeqCUzHQ=="
export STORAGE_ACCOUNT_ENDPOINT="http://127.0.0.1:10000/devstoreaccount1"
```

To make these changes permanent, add them to your shell configuration file (e.g., `~/.bashrc` or `~/.zshrc`).


### Services and PORTS

You can check the ports in use in `docker-compose.yml`


We are using...

* For MongoDB as Cosmos DB -> 8082 (given that Cosmos DB emulator uses 8081)
* For Azurite -> 10000, 10001 and 10002

## Workflow: How to Use This Project

1. **Edit Ports**
   - Open `ports.json` and set the desired host ports for each service.
   - The format is:
     ```json
     {
       "mongodb": { "host": 28017, "container": 27017 },
       "cosmosdb": [
         { "host": 8081, "container": 8081 },
         ...
       ],
       "storage": [
         { "host": 10000, "container": 10000 },
         ...
       ]
     }
     ```
   - Only change the `host` value; the `container` value must match the service's expected port.

2. **Edit the Compose Template (Optional)**
   - To add or remove services, or change service configuration, edit `docker-compose.template.yml`.
   - Do not edit `docker-compose.yml` directly; it is auto-generated.

3. **Generate and Start the Stack**
   - Run the management script:
     ```bash
     python scripts/manage_stack.py
     ```
   - This will:
     - Validate your `ports.json` for errors or conflicts.
     - Generate `docker-compose.yml` from the template and port mappings.
     - Start the main services (`cosmosdb` and `azurite`).

4. **If You Have Issues with CosmosDB Emulator**
   - You can use MongoDB as a CosmosDB replacement:
     ```bash
     python scripts/manage_stack.py --mongodb-as-cosmosdb
     ```
   - This will start `mongodb-as-cosmosdb` and `azurite` instead.

5. **Stopping and Cleaning Up**
   - To stop all containers and remove the generated compose file:
     ```bash
     python scripts/manage_stack.py --stop
     ```

6. **Best Practices**
   - Never edit `docker-compose.yml` directly; always use the template and scripts.
   - Document any changes to the template or port mappings for your team.

For more details, see comments in each file and the rest of this README.