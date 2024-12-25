import os
import time
from qbittorrentapi import Client
from utils.logger import main_logger

class QBittorrentClient:
    """
    使用 qbittorrent-api 实现的精简版客户端，添加了种子状态检查功能。
    """

    def __init__(self):
        """
        初始化客户端，自动从环境变量中加载配置。
        """
        self.host = os.getenv("QB_API_URL", "http://127.0.0.1:8080")
        self.username = os.getenv("QB_USERNAME", "admin")
        self.password = os.getenv("QB_PASSWORD", "adminadmin")

        try:
            self.client = Client(host=self.host, username=self.username, password=self.password)
            self.client.auth_log_in()
            main_logger.info(f"成功连接到 qBittorrent API: {self.host}")
        except Exception as e:
            raise ConnectionError(f"连接 qBittorrent API 失败: {e}")

    def pause_all(self):
        """
        暂停所有种子任务，并检查是否全部暂停成功。
        """
        try:
            self.client.torrents.pause.all()
            main_logger.info("已发出暂停所有种子任务的指令。")

            # 等待 30 秒，确保种子状态更新
            main_logger.info("等待 30 秒以确保种子开始暂停...")
            time.sleep(30)

            # 检查是否还有不是 "paused", "pausedDL", "pausedUP" 状态的种子
            not_paused = self._check_not_in_status(["paused", "pausedDL", "pausedUP", "stalledDL"])
            if not_paused:
                main_logger.error("以下种子未成功暂停：")
                for torrent in not_paused:
                    main_logger.error(f"种子名称: {torrent.name} - 状态: {torrent.state}")
                # raise RuntimeError("部分种子任务未能正确暂停，请检查日志！")
            else:
                main_logger.info("所有种子任务已成功暂停。")
        except Exception as e:
            main_logger.error(f"暂停种子任务失败: {e}")
            raise RuntimeError(f"暂停种子任务失败: {e}")

    def resume_all(self):
        """
        恢复所有种子任务，并检查是否全部恢复成功。
        """
        try:
            self.client.torrents.resume.all()
            main_logger.info("已发出恢复所有种子任务的指令。")

            # 等待 30 秒，确保种子状态更新
            main_logger.info("等待 30 秒以确保种子开始恢复...")
            time.sleep(30)

            # 检查是否还有 "paused", "pausedDL", "pausedUP" 状态的种子
            still_paused = self._check_in_status(["paused", "pausedDL", "pausedUP"])
            if still_paused:
                main_logger.error("以下种子未成功恢复：")
                for torrent in still_paused:
                    main_logger.error(f"种子名称: {torrent.name} - 状态: {torrent.state}")
                main_logger.error("请手动检查并恢复这些种子。")
                # raise RuntimeError("部分种子任务未能正确恢复，请检查日志！")
            else:
                main_logger.info("所有种子任务已成功恢复。")
        except Exception as e:
            main_logger.error(f"恢复种子任务失败: {e}")
            raise RuntimeError(f"恢复种子任务失败: {e}")

    def _check_not_in_status(self, statuses):
        """
        检查种子状态是否不在指定状态列表中。
        :param statuses: 预期的状态列表
        :return: 状态不符合的种子列表
        """
        try:
            torrents = self.client.torrents_info(status_filter=None)  # 获取所有种子
            not_matching = [torrent for torrent in torrents if torrent.state not in statuses]
            return not_matching
        except Exception as e:
            main_logger.error(f"检查种子状态失败: {e}")
            raise RuntimeError(f"检查种子状态失败: {e}")

    def _check_in_status(self, statuses):
        """
        检查种子状态是否在指定状态列表中。
        :param statuses: 预期的状态列表
        :return: 状态符合的种子列表
        """
        try:
            torrents = self.client.torrents_info(status_filter=None)  # 获取所有种子
            matching = [torrent for torrent in torrents if torrent.state in statuses]
            return matching
        except Exception as e:
            main_logger.error(f"检查种子状态失败: {e}")
            raise RuntimeError(f"检查种子状态失败: {e}")


# 测试代码
if __name__ == "__main__":
    # 初始化客户端
    qb_client = QBittorrentClient()

    print("\n=== 测试暂停所有种子任务 ===")
    try:
        qb_client.pause_all()
    except Exception as e:
        print(f"暂停任务失败: {e}")

    print("\n=== 测试恢复所有种子任务 ===")
    try:
        qb_client.resume_all()
    except Exception as e:
        print(f"恢复任务失败: {e}")