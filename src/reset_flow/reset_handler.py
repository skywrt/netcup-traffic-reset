from qbittorrent_api.client import QBittorrentClient
from netcup_api.power_cycle import acpi_reboot_server
from utils.logger import main_logger  # 引入日志模块

def reset_server_flow():
    """
    执行重置流程：
    1. 暂停 qBittorrent 的种子任务。
    2. 重启服务器。
    3. 恢复种子任务。
    """
    qb_client = QBittorrentClient()  # 初始化 qBittorrent 客户端

    try:
        # 暂停所有种子任务
        main_logger.info("暂停所有种子任务...")
        qb_client.pause_all()

        # 执行服务器重启
        main_logger.info("执行服务器重启...")
        acpi_reboot_server()

        # 恢复所有种子任务
        main_logger.info("恢复所有种子任务...")
        qb_client.resume_all()

        main_logger.info("重置流程完成！")

    except Exception as e:
        # 捕获异常并记录日志
        main_logger.error(f"重置流程失败：{e}")