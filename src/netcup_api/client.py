# src/netcup_api/client.py
import os
from netcup_webservice import NetcupWebservice

# 从环境变量中读取凭证
NETCUP_CUSTOMER_ID = os.getenv("NETCUP_CUSTOMER_ID")
NETCUP_API_PASSWORD = os.getenv("NETCUP_API_PASSWORD")
DEFAULT_VSERVER = os.getenv("DEFAULT_VSERVER")

if not NETCUP_CUSTOMER_ID or not NETCUP_API_PASSWORD or not DEFAULT_VSERVER:
    raise ValueError("请确保 .env 文件中已正确配置 NETCUP_CUSTOMER_ID、NETCUP_API_PASSWORD 和 DEFAULT_VSERVER")

# 初始化 Netcup 客户端
client = NetcupWebservice(
    loginname=NETCUP_CUSTOMER_ID,
    password=NETCUP_API_PASSWORD
)

def get_client():
    """返回初始化的 Netcup 客户端"""
    return client