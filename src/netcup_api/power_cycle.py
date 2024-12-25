# src/netcup_api/power_cycle.py
import os
import time

from netcup_api.client import get_client
from utils.logger import main_logger

# 从环境变量中读取默认 vServer 名称
DEFAULT_VSERVER = os.getenv("DEFAULT_VSERVER")

import re

def parse_uptime(uptime_str):
    """
    使用正则表达式解析运行时间字符串为秒数。
    示例：'0 minutes' -> 0, '5 minutes' -> 300, '120 seconds' -> 120

    Args:
        uptime_str (str): 从 API 返回的运行时间字符串。

    Returns:
        int: 运行时间（秒）。如果解析失败，返回 -1 表示错误。
    """
    # 检查是否是 SOAP 错误信息
    if uptime_str.startswith("SOAP Fault occurred"):
        main_logger.error(f"运行时间获取失败：{uptime_str}")
        return -1  # 返回 -1 表示错误

    # 使用正则表达式提取数值和单位
    match = re.match(r"(\d+)\s+(minute|second)s?", uptime_str)
    if match:
        value, unit = match.groups()
        value = int(value)  # 转为整数
        if unit == "minute":
            return value * 60  # 转换为秒
        elif unit == "second":
            return value
    else:
        main_logger.error(f"无法解析运行时间字符串：{uptime_str}")
        return -1  # 返回 -1 表示解析失败

def acpi_reboot_server(vserver_name=None, initial_wait=60, check_interval=30, timeout=300):
    """
    对指定的 vServer 执行 ACPI 重启，并检查是否已成功运行至少 1 分钟。

    :param vserver_name: 要重启的 vServer 名称。如果未提供，使用 DEFAULT_VSERVER。
    :param initial_wait: 发送重启指令后等待的初始时间（秒）。
    :param check_interval: 检查重启状态的间隔时间（秒）。
    :param timeout: 等待重启完成的最大时间（秒）。
    :raises: ValueError 如果 vServer 名称未提供或未配置。
    :raises: RuntimeError 如果在超时时间内服务器未成功运行至少 1 分钟。
    """
    client = get_client()

    # 如果没有指定 vserver_name，使用默认的
    vserver_name = vserver_name or DEFAULT_VSERVER
    if not vserver_name:
        main_logger.error("未指定 vServer 名称，请确保 DEFAULT_VSERVER 已正确配置")
        raise ValueError("未指定 vServer 名称，请确保 DEFAULT_VSERVER 已正确配置")

    # 触发 ACPI 重启
    main_logger.info(f"正在对 vServer: {vserver_name} 执行 ACPI 重启...")
    client.acpi_reboot_vserver(vserver_name)
    main_logger.info(f"vServer {vserver_name} 已触发 ACPI 重启。")

    # 初始等待时间
    main_logger.info(f"等待 {initial_wait} 秒，以便服务器完成初始重启...")
    time.sleep(initial_wait)

    # 检查服务器的运行时间
    main_logger.info(f"开始检查 vServer: {vserver_name} 的运行时间...")
    start_time = time.time()

    while True:
        # 获取当前时间
        elapsed_time = time.time() - start_time

        # 查询服务器的运行时间
        uptime_str = client.get_vserver_uptime(vserver_name)
        main_logger.info(f"当前 vServer 运行时间: {uptime_str}")

        # 将运行时间解析为秒数
        uptime = parse_uptime(uptime_str)

        # 检查解析结果
        if uptime == -1:
            main_logger.error(f"无法获取 vServer {vserver_name} 的运行时间：{uptime_str}")
            raise RuntimeError(f"无法获取 vServer {vserver_name} 的运行时间：{uptime_str}")

        if uptime >= 60:
            main_logger.info(f"vServer {vserver_name} 已成功运行至少 1 分钟。")
            break

        if elapsed_time > timeout:
            main_logger.error(f"vServer {vserver_name} 在 {timeout} 秒内未能成功运行至少 1 分钟，重启失败。")
            raise RuntimeError(f"vServer {vserver_name} 在 {timeout} 秒内未能成功运行至少 1 分钟，重启失败。")

        # 等待一段时间后重试
        main_logger.info(f"vServer {vserver_name} 尚未达到 1 分钟运行时间，等待 {check_interval} 秒后重试...")
        time.sleep(check_interval)