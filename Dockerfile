# 使用官方 Python 基础镜像
FROM python:3.10-slim

# 设置时区为中国东八区（Asia/Shanghai）
ENV TZ=Asia/Shanghai
RUN apt-get update && apt-get install -y tzdata && apt-get clean
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置工作目录为 src
WORKDIR /app/src

# 复制项目文件到容器
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r /app/requirements.txt

# 拷贝 entrypoint 脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 启动容器时运行 entrypoint 脚本
ENTRYPOINT ["/entrypoint.sh"]