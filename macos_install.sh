#!/bin/bash

# 语言选项
echo "请选择语言 / Please select language:"
echo "1) 中文 (Chinese) "
echo "2) English"
read -p "输入选择 (Enter choice) [1/2]:  " lang_choice

# 根据用户选择设置语言
if [ "$lang_choice" -eq 1 ]; then
    export lang="zh"
    prompt_server_port="请输入服务端口（默认是 8188）： "
    project_not_exist="项目目录不存在"
    clone_success="克隆成功"
    commands="可用命令: comfy init, comfy start, comfy stop, comfy restart, comfy dlmodels, comfy update, comfy logs, comfy status"
elif [ "$input_choice" -eq 2 ]; then
    export lang="en"
    project_not_exist="Project directory does not exist"
    clone_success="Clone successful"
    commands="Available commands: comfy init, comfy start, comfy stop, comfy restart, comfy dlmodels, comfy update, comfy logs, comfy status"
else
    echo "输入无效，默认使用英语 / Invalid input, defaulting to English."
    export lang="en"
    prompt_server_port="Please enter the server port (default is 8188): "
    project_not_exist="Project directory does not exist"
    clone_success="Clone successful"
    commands="Available commands: comfy init, comfy start, comfy stop, comfy restart, comfy dlmodels, comfy update, comfy logs, comfy status"
fi

read -p "$prompt_server_port" server_port
server_port=${server_port:-8188}
export server_port="$server_port" lang="$lang"

if [ -d "$HOME/WhaleComfy" ]; then
    cd "$HOME/WhaleComfy" || { echo "$project_not_exist"; exit 1; }
    git pull origin main
else
    git clone https://github.com/pictorialink/WhaleComfy.git "$HOME/WhaleComfy"
    echo "$clone_success"
fi

cd "$HOME/WhaleComfy" || { echo "$project_not_exist"; exit 1; }

chmod +x scripts/run_mac.sh

# 目标目录
BIN_DIR="/usr/local/bin"

# 判断目录是否存在
if [ ! -d "$BIN_DIR" ]; then
    echo "目录不存在，正在创建 $BIN_DIR ..."
    sudo mkdir -p "$BIN_DIR"  # 使用 -p 选项以确保创建父目录
else
    echo "目录 $BIN_DIR 已存在，直接继续 ..."
fi

tee ~/.bash_profile >/dev/null <<EOF
export server_port="$server_port"
export lang="$lang"
EOF


echo '#!/bin/bash' | sudo tee "$BIN_DIR/comfy"
echo "bash \"$HOME/WhaleComfy/scripts/run_mac.sh\" \"\$@\"" | sudo tee -a "$BIN_DIR/comfy"
sudo chmod +x "$BIN_DIR/comfy"

sudo chmod +x $BIN_DIR/comfy && source ~/.zshrc
comfy init
comfy start 

echo "$commands"
