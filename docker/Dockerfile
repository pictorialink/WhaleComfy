FROM ubuntu:22.04


WORKDIR /ComfyUI


RUN apt-get update && apt-get install gcc  python3-venv build-essential git git-lfs libgl1 libgl1-mesa-glx ffmpeg libglib2.0-0 libsm6 libxrender1 libxext6 wget -y


RUN git config --global http.lowSpeedLimit 0 && git config --global http.lowSpeedTime 999999 &&git config --global http.postBuffer 1048576000
RUN git config --global http.version HTTP/1.1
RUN git config --global http.sslVerify false

RUN git clone --branch v0.3.43  https://github.com/comfyanonymous/ComfyUI.git .
RUN python3 -m venv venv 
ENV PATH="/ComfyUI/venv/bin/:${PATH}"


RUN /ComfyUI/venv/bin/pip install --default-timeout=600 -r requirements.txt


COPY scripts/ /app/scripts/
COPY ../configs/ /app/configs/
RUN chmod +x /app/scripts/entrypoint.sh


RUN /ComfyUI/venv/bin/python /app/scripts/get_repo_tags.py


EXPOSE 8188


ENTRYPOINT ["/app/scripts/entrypoint.sh"]
