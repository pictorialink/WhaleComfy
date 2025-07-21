#!/bin/bash
#
## start ComfyUI Server
if [ -f "custom_nodes/ComfyUI-Custom-Node-Config/files/config.sh" ]; then
    sh custom_nodes/ComfyUI-Custom-Node-Config/files/config.sh
fi 
/ComfyUI/venv/bin/python /app/scripts/get_repo_tags.py

/ComfyUI/venv/bin/python main.py --listen
