# CUDA 지원 Ubuntu 기반 이미지 사용
FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# NVIDIA Container Toolkit 설치
RUN distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | apt-key add - \
    && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

RUN apt-get update && apt-get install -y nvidia-container-toolkit

# Ollama 설치
RUN curl -fsSL https://ollama.com/install.sh | sh

# 작업 디렉토리 설정
WORKDIR /app

# EEVE 모델 다운로드
RUN wget https://huggingface.co/teddylee777/EEVE-Korean-Instruct-10.8B-v1.0-gguf/resolve/main/EEVE-Korean-Instruct-10.8B-v1.0-Q5_K_M.gguf

# Modelfile 생성
RUN echo "FROM /app/EEVE-Korean-Instruct-10.8B-v1.0-Q5_K_M.gguf" > /app/Modelfile

# Python 패키지 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY ./src/main.py .
COPY ./src/persona.py .
COPY ./src/recommendation.py .
COPY ./src/utils.py .
COPY ./src/organize.py .

# Ollama 서비스 시작 및 모델 생성을 위한 스크립트
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama service..."\n\
ollama serve &\n\
sleep 10\n\
echo "Creating eeve model..."\n\
CUDA_VISIBLE_DEVICES=0 ollama create eeve:latest -f /app/Modelfile\n\
echo "Model creation completed"\n\
echo "Verifying model..."\n\
ollama list\n\
echo "Starting FastAPI application..."\n\
uvicorn main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# 포트 8000 노출
EXPOSE 8000

# 컨테이너 시작 시 실행할 명령
CMD ["/app/start.sh"]

#build, run할 때 메모리 제한과 GPU 사용을 위한 명령어
#docker build -t llm_server_gpu .
#docker run --memory=16g --gpus all -p 8000:8000 llm_server_gpu
