import sys
import subprocess
import os
import json

# 自动安装 huggingface_hub
try:
    from huggingface_hub import hf_hub_download
except ImportError:
    pip_path = "/ComfyUI/venv/bin/pip"
    subprocess.check_call([pip_path, "install", "huggingface_hub"])
    from huggingface_hub import hf_hub_download

from huggingface_hub import snapshot_download

comfyui_dir = "/ComfyUI"
custom_nodes_dir = f"{comfyui_dir}/custom_nodes"

# 遍历 custom_nodes 下的所有子目录
for subdir in os.listdir(custom_nodes_dir):
    subdir_path = os.path.join(custom_nodes_dir, subdir)
    models_json_path = os.path.join(subdir_path, "models.json")
    if os.path.isdir(subdir_path) and os.path.exists(models_json_path):
        print(f"发现 models.json: {models_json_path}")
        with open(models_json_path, "r", encoding="utf-8") as f:
            models_data = json.load(f)
        # 只处理 common 和 cuda
        for key in ["common", "cuda"]:
            if key not in models_data:
                continue
            for model in models_data[key]:
                repo_id = model["repo_id"]
                local_path = os.path.join(comfyui_dir, model["local_path"])
                os.makedirs(local_path, exist_ok=True)
                files = model.get("files")
                if files:
                    for file_name in files:
                        print(f"下载 {repo_id} 的 {file_name} 到 {local_path}")
                        try:
                            hf_hub_download(
                                repo_id=repo_id,
                                filename=file_name,
                                local_dir=local_path,
                                local_dir_use_symlinks=False
                            )
                        except Exception as e:
                            print(f"下载失败: {repo_id}/{file_name}，错误：{e}")
                else:
                    print(f"{repo_id} 未指定 files 字段，下载整个仓库到 {local_path}")
                    try:
                        snapshot_download(
                            repo_id=repo_id,
                            local_dir=local_path,
                            local_dir_use_symlinks=False
                        )
                    except Exception as e:
                        print(f"下载仓库失败: {repo_id}，错误：{e}")
