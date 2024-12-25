# Netcup Traffic Reset

[English Version](README_EN.md) | 中文版本

## Netcup Traffic Reset

本项目是一个用于自动化管理 **Netcup vServer** 和 **qBittorrent** 下载任务的工具，通过调用 Netcup API 和 qBittorrent API，实现服务器的自动重启以及种子任务的暂停/恢复。

---

## 环境变量配置

在运行项目之前，请按照以下步骤配置环境变量：

1. 将 `env.example` 文件复制为 `.env` 文件：

    ```bash
    cp .env.example .env
    ```

2. 根据实际需求编辑 `.env` 文件，填写正确的配置信息：

    ```plaintext
    # Netcup的客户ID
    NETCUP_CUSTOMER_ID=your_customer_id
    # Netcup 的网页 API 密码并非您的登录密码。
    # 该密码需要在 Netcup SCP 后台右上角的“Options”选项中找到，具体为“Webservice”部分的“Webservice Password”。
    # 同时，请确保启用“Activate Webservice”功能，并保存设置。
    NETCUP_API_PASSWORD=your_api_password
    # Netcup 的 VServer ID，同样在 SCP 控制台的“Server”列表中查看
    DEFAULT_VSERVER=your_default_vserver
    # qBittorrent Web API 的地址
    QB_API_URL=http://127.0.0.1:8080
    # qBittorrent 登录用户名
    QB_USERNAME=admin
    # qBittorrent 登录密码
    QB_PASSWORD=admin
    # 定义每天任务的时间（24 小时制，格式：HH:MM）
    DAILY_TASK_TIME=04:00
    ```

---

## Docker 部署

### Git Clone 仓库自行构建

1. **构建镜像**

    首先，克隆本项目仓库到本地：

    ```bash
    git clone https://github.com/kafuuchino-s/netcup-traffic-reset
    cd netcup-traffic-reset
    ```

    然后，使用以下命令构建 Docker 镜像：

    ```bash
    docker build -t netcup-traffic-reset:latest .
    ```

2. **运行容器**

    构建完成后，使用以下命令运行容器，并挂载 `.env` 配置文件：

    ```bash
    docker run --rm -d \
      --env-file .env \
      --name netcup-traffic-reset \
      netcup-traffic-reset:latest
    ```

### 使用 kafuuchino520/netcup-traffic-reset 镜像直接启动

可以直接使用 Docker Hub 上提供的预构建镜像来运行：

```bash
docker run --rm -d \
  --env-file .env \
  --name netcup-traffic-reset \
  kafuuchino520/netcup-traffic-reset:latest
```

---

## 功能说明

1. **自动化重置流程**
    -   暂停 qBittorrent 的种子任务。
    -   重启 Netcup vServer（通过 Power Cycle 或 ACPI 重启）。
    -   检查网络状态恢复后，重新启动种子任务。
2. **定时任务支持**
    -   通过 `.env` 文件中的 `DAILY_TASK_TIME` 设置定时任务时间，默认为每天凌晨 4 点。
3. **轻量化部署**
    -   使用官方 Docker 镜像快速部署，无需安装复杂的依赖环境。

---

## 常见问题

1. **无法连接 qBittorrent API？**
    -   检查 `.env` 文件中 `QB_API_URL` 是否填写正确。
    -   确保 qBittorrent 的 Web API 已启用，并设置了正确的用户名和密码。
2. **Netcup API 调用失败？**
    -   检查 `.env` 文件中 `NETCUP_CUSTOMER_ID` 和 `NETCUP_API_PASSWORD` 是否正确。
    -   确保您已在 Netcup SCP 后台启用“Activate Webservice”功能，并使用正确的 Webservice 密码。
3. **定时任务未生效？**
    -   确保 `.env` 文件中 `DAILY_TASK_TIME` 格式正确。
    -   若修改了 `.env`，请重新启动容器。

---

## 总结

-   **配置简单**：通过 `.env` 文件集中管理所有配置项。
-   **部署便捷**：使用官方 Docker 镜像，无需额外构建。
-   **自动化流程**：支持定时任务，轻松实现服务器流量重置和种子任务管理。

## 项目引用

-   [mihneamanolache/netcup-webservice](https://github.com/mihneamanolache/netcup-webservice)
-   [qbittorrent-api](https://pypi.org/project/qbittorrent-api/)

如有疑问或建议，欢迎提交 Issue！
