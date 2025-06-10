# WhaleComfy

## Project Overview
WhaleComfy is a containerized deployment solution based on Docker, designed to simplify the deployment and management process of applications.

## Directory Structure
```
WhaleComfy/
├── docker/
├── scripts/
├── linux_install.sh
├── macos_install.sh
├── README_zh.md
└── README.md
```

## Requirements
- NVIDIA VRAM: 12GB or more
- GPU supporting CUDA 12.1 or higher
- Docker 20.10.0 or higher
- Docker Compose 2.0.0 or higher
- Linux/Unix environment (for running shell/python scripts)

## Installation
### Quick Installation (Ubuntu/Debian/RHEL/CentOS)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/pictorialink/WhaleComfy/main/linux_install.sh)"
```
### Quick Installation (Macos M1/M2/M3)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/pictorialink/WhaleComfy/main/linux_install.sh)"
```
#### Usage Instructions
- Initialize: `comfy init`
- Start service: `comfy start`
- Stop service: `comfy stop`
- Restart service: `comfy restart`
- Check status: `comfy status`
- View logs: `comfy logs`

### Manual Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/pictorialink/WhaleComfy.git
cd WhaleComfy
```

#### 2. Run the Deployment Script
```bash
chmod +x ./scripts/run_docker.sh
./scripts/run_docker.sh
```

#### 3. Usage Instructions

##### Main Commands
- Initialize: `./scripts/run_docker.sh init`
- Start service: `./scripts/run_docker.sh start`
- Stop service: `./scripts/run_docker.sh stop`
- Restart service: `./scripts/run_docker.sh restart`
- Check status: `./scripts/run_docker.sh status`
- View logs: `./scripts/run_docker.sh logs`

## Common Issues
1. If you encounter permission issues, ensure `run_docker.sh` has execution permissions.
2. Make sure the Docker service is running.
3. Check if the network connection is stable.

## Contributing
Contributions are welcome! Please submit Issues and Pull Requests to help improve the project.

## License
[MIT License](LICENSE)

## Contact
For any questions, please contact us through:
- Submit an Issue
- Send email to: your.email@example.com 