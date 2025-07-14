import os
import json
import subprocess
import requests
from packaging import version as pkg_version
from packaging.specifiers import SpecifierSet
from pathlib import Path

REPO_URL = 'https://github.com/pictorialink/Picto-workflow.git'
REPO_DIR = 'Picto-workflow'

# 自动下载仓库或更新到最新
if not os.path.exists(REPO_DIR):
    print(f"未检测到 {REPO_DIR} 目录，正在自动下载仓库...")
    result = subprocess.run(['git', 'clone', REPO_URL], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"git clone 失败：{result.stderr}")
        exit(1)
    print(f"仓库下载完成！")
else:
    print(f"检测到 {REPO_DIR} 目录，正在执行 git pull 更新到最新版本...")
    result = subprocess.run(['git', '-C', REPO_DIR, 'pull'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"git pull 失败：{result.stderr}")
        exit(1)
    print(f"仓库已更新到最新版本！")

# 需要遍历的两个目录
BASE_DIRS = [
    os.path.join(REPO_DIR, 'cuda'),
    os.path.join(REPO_DIR, 'common'),
]

def get_github_tags(repo_id):
    if not repo_id or '/' not in repo_id:
        return []
    url = f'https://api.github.com/repos/{repo_id}/tags'
    tags = []
    page = 1
    while True:
        paged_url = f'{url}?per_page=100&page={page}'
        try:
            response = requests.get(paged_url, timeout=10)
            if response.status_code == 200:
                page_tags = [tag['name'] for tag in response.json()]
                if not page_tags:
                    break
                tags.extend(page_tags)
                if len(page_tags) < 100:
                    break
                page += 1
            else:
                break
        except Exception as e:
            break
    return tags

def caret_to_range(version_spec):
    # 只处理以^开头的
    if not version_spec or not version_spec.startswith('^'):
        return version_spec
    parts = version_spec[1:].split('.')
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    if major > 0:
        upper = f"<{major+1}.0.0"
    elif minor > 0:
        upper = f"<0.{minor+1}.0"
    else:
        upper = f"<0.0.{patch+1}"
    lower = f">={major}.{minor}.{patch}"
    return f"{lower},{upper}"

def pick_latest_tag(tags, version_spec):
    # 修正 ^ 语法为区间表达式
    spec = caret_to_range(version_spec)
    try:
        spec_set = SpecifierSet(spec)
    except Exception:
        spec_set = SpecifierSet('')
    valid_tags = []
    for tag in tags:
        tag_clean = tag.lstrip('v')
        try:
            v = pkg_version.parse(tag_clean)
            if v in spec_set:
                valid_tags.append((v, tag))
        except Exception:
            continue
    if not valid_tags:
        return None
    latest = max(valid_tags, key=lambda x: x[0])
    return latest[1]


def get_repo_info_from_node_json(base_dir):
    results = set()
    if not os.path.isdir(base_dir):
        return results
    for subdir in os.listdir(base_dir):
        sub_path = os.path.join(base_dir, subdir)
        node_json_path = os.path.join(sub_path, 'node.json')
        if os.path.isfile(node_json_path):
            try:
                with open(node_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                nodes = data.get('nodes', [])
                for node in nodes:
                    repo_id = node.get('repo_id', None)
                    version = node.get('version', None)
                    if repo_id and version:
                        results.add((repo_id, version))
            except Exception as e:
                print(f"读取 {node_json_path} 失败: {e}")
    return results

def main():
    unique_repo_version = set()
    save_dir = '/ComfyUI/custom_nodes'
    for base_dir in BASE_DIRS:
        unique_repo_version.update(get_repo_info_from_node_json(base_dir))
    # 输出结果
    print(f"{'repo_id':<40} {'version':<20} {'latest_tag'}")
    for repo_id, version in sorted(unique_repo_version):
        tags = get_github_tags(repo_id)
        latest_tag = pick_latest_tag(tags, version)
        print(f"{repo_id:<40} {version:<20} {latest_tag}")
        local_dir = repo_id.split('/')[-1]
        target_path = os.path.join(save_dir, local_dir)
        if os.path.exists(target_path):
            print(f"{target_path} 已存在，执行 git pull 更新到 {latest_tag}")
            subprocess.run(['git', '-C', target_path, 'fetch', '--all'])
            subprocess.run(['git', '-C', target_path, 'checkout', latest_tag])
            subprocess.run(['git', '-C', target_path, 'pull'])
            # 检查 requirements.txt 并安装
            requirements_file = Path(target_path) / "requirements.txt"
            if requirements_file.exists():
                print(f"检测到 {requirements_file}，正在安装依赖...")
                subprocess.run(
                    ["/ComfyUI/venv/bin/pip", "install", "-r", str(requirements_file), "--timeout", "600"],
                    check=True
                )
        else:
            subprocess.run(['git', 'clone', '--branch', latest_tag, f'https://github.com/{repo_id}', target_path])
            # 克隆后同样检查 requirements.txt 并安装
            requirements_file = Path(target_path) / "requirements.txt"
            if requirements_file.exists():
                print(f"检测到 {requirements_file}，正在安装依赖...")
                subprocess.run(
                    ["/ComfyUI/venv/bin/pip", "install", "-r", str(requirements_file), "--timeout", "600"],
                    check=True
                )


if __name__ == '__main__':
    main()
