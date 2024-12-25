from reset_flow.reset_handler import reset_server_flow
from utils.logger import main_logger
import time
from datetime import datetime, timedelta
import os


def get_daily_task_time():
    """从环境变量读取每天任务执行时间"""
    daily_task_time = os.getenv("DAILY_TASK_TIME", "04:00")  # 默认时间为 04:00
    try:
        # 解析时间（格式：HH:MM）
        hour, minute = map(int, daily_task_time.split(":"))
        return hour, minute
    except ValueError:
        raise ValueError("环境变量 DAILY_TASK_TIME 格式错误，应为 HH:MM（例如 04:00）")


def get_next_run_time(hour, minute):
    """计算下次运行的时间点"""
    now = datetime.now()
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # 如果当前时间已经过了今天的运行时间，设置为明天
    if now >= next_run:
        next_run += timedelta(days=1)

    return next_run


def main():
    """主任务执行逻辑"""
    # 从环境变量读取每天任务时间
    hour, minute = get_daily_task_time()
    main_logger.info(f"任务每天定时运行时间: {hour:02d}:{minute:02d}")

    while True:
        # 计算距离下次运行的时间
        next_run = get_next_run_time(hour, minute)
        main_logger.info(f"下一次任务运行时间: {next_run}")

        # 计算需要等待的秒数
        sleep_seconds = (next_run - datetime.now()).total_seconds()
        main_logger.info(f"距离下一次任务运行还有 {sleep_seconds} 秒...")

        # 等待到指定时间
        time.sleep(sleep_seconds)

        # 执行任务
        main_logger.info("开始执行重置流程...")
        reset_server_flow()


if __name__ == "__main__":
    main()