#!/bin/bash

# 语言选项
echo "请选择语言 / Please select language:"
echo "1) 中文 (Chinese) "
echo "2) English"
read -p "输入选择 (Enter choice) [1/2]:  " lang_choice

# 根据用户选择设置语言
if [ "$lang_choice" -eq 1 ]; then
    export lang="zh"
    install_condition="请使用root用户安装"
    prompt_clone_dir="请输入要克隆到的目录（默认是 /data）： "
    prompt_server_port="请输入服务端口（默认是 8188）： "
    project_not_exist="项目目录不存在"
    clone_success="克隆成功"
    commands="可用命令: comfy init, comfy start, comfy stop, comfy restart, comfy dlmodels, comfy update, comfy logs, comfy status"
elif [ "$input_choice" -eq 2 ]; then
    export lang="en"
    install_condition="Please use the root user to install"
    prompt_clone_dir="Please enter the directory to clone to (default is /data): "
    project_not_exist="Project directory does not exist"
    clone_success="Clone successful"
    commands="Available commands: pictorialink init, pictorialink start, pictorialink stop, pictorialink restart, pictorialink dlmodels, pictorialink update, pictorialink logs, pictorialink status"
else
    echo "输入无效，默认使用英语 / Invalid input, defaulting to English."
    export lang="en"
    install_condition="Please use the root user to install"
    prompt_clone_dir="Please enter the directory to clone to (default is /data): "
    prompt_server_port="Please enter the server port (default is 8188): "
    project_not_exist="Project directory does not exist"
    clone_success="Clone successful"
    commands="Available commands: comfy init, comfy start, comfy stop, comfy restart, comfy dlmodels, comfy update, comfy logs, comfy status"
fi

echo "$install_condition"
read -p "$prompt_server_port" server_port
read -p "$prompt_clone_dir" clone_dir

server_port=${server_port:-8188}
clone_dir=${clone_dir:-/data}
export CLONE_DIR="$clone_dir" server_port="$server_port" lang="$lang"

tee /etc/profile.d/custom_vars.sh >/dev/null <<EOF
#!/bin/sh
export CLONE_DIR="$clone_dir"
export server_port="$server_port"
export lang="$lang"
EOF

chmod +x /etc/profile.d/custom_vars.sh
source /etc/profile

if [ ! -d "$clone_dir" ]; then
    mkdir -p "$clone_dir"
fi


if [ -d "$clone_dir/WhaleComfy" ]; then
    cd "$clone_dir/WhaleComfy" || { echo "$project_not_exist"; exit 1; }
    git pull origin main
else
    git clone --branch v1.0.0 https://github.com/pictorialink/WhaleComfy.git "$clone_dir/WhaleComfy"
    echo "$clone_success"
fi


cd "$clone_dir/WhaleComfy" || { echo "$project_not_exist"; exit 1; }


chmod +x scripts/run_docker.sh


echo '#!/bin/bash' > /usr/local/bin/comfy
echo "source /etc/profile.d/custom_vars.sh" >> /usr/local/bin/comfy
echo "bash \"$clone_dir/WhaleComfy/scripts/run_docker.sh\" \"\$@\"" >> /usr/local/bin/comfy

chmod +x /usr/local/bin/comfy 


comfy init ||  exit 1
comfy start 


echo "$commands"
