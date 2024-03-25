# 使用官方的 Python 运行时作为父镜像
FROM python:3.8-slim

# 在容器中设置工作目录
WORKDIR /server

# 将当前目录中的内容复制到容器中的 /server 目录下
COPY . /server

# 安装 requirements.txt 中指定的所有依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 设置时区为上海时间
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 当容器启动时运行 app.py
CMD ["python", "app.py"]
