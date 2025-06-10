#!/bin/bash
#
## start ComfyUI Server
if [ -f "custom_nodes/ComfyUI-Custom-Node-Config/files/config.sh" ]; then
    sh custom_nodes/ComfyUI-Custom-Node-Config/files/config.sh
fi 
python3 main.py --listen
