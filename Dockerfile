FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 安装依赖工具和系统包（sqlite3）
RUN apt update && apt install -y --no-install-recommends \
  sqlite3 \
  && apt clean && rm -rf /var/lib/apt/lists/*

# 复制项目文件（先复制依赖声明文件用于缓存优化）
COPY pyproject.toml .
COPY README.md .  
RUN pip install --upgrade pip
RUN pip install .

# 再复制剩余源代码
COPY . .

# 启动应用
ENTRYPOINT [ "python", "./jabagram.py" ]

