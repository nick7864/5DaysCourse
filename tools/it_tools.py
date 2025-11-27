"""IT部門專用工具函式"""

import random
import string
from typing import Dict, List

# 模擬IT帳號資料庫
EMPLOYEE_ACCOUNTS = {
    "new_employee": {
        "email": "new_employee@example.com",
        "password": "default_password",
        "vpn": "vpn12345",
        "permissions": ["read", "write"],
    },
    "other_employee": {
        "email": "other_employee@example.com",
        "password": "default_password",
        "vpn": "vpn67890",
        "permissions": ["read", "write", "admin"],
    },
}


# 建立員工郵件帳號
def create_email_acount(employee_name: str, dept: str) -> Dict:
    """
    為新員工建立公司郵件帳號

    Args:
        employee_name: 員工姓名 (中文或英文)
        department: 部門名稱 (例如: "Engineering", "Sales", "HR")

    Returns:
        包含帳號資訊的字典

    Example:
        create_email_account("張小明", "Engineering")
        -> {"email": "xiaoming.zhang@company.com", "initial_password": "Temp1234!"}
    """

    username = employee_name.lower().replace(" ", "_")
    email = f"{username}@company.com"
    temp_password = (
        "".join(random.choices(string.ascii_letters + string.digits, k=8)) + "!"
    )

    EMPLOYEE_ACCOUNTS[username] = {
        "email": email,
        "password": temp_password,
        "status": "active",
    }

    return {
        "email": email,
        "initial_password": temp_password,
        "message": "Account created successfully",
    }


# 權限分配工具
def assign_system_permission(email: str, systems: List[str]) -> Dict:
    """
    分配系統存取權限

    Args:
        email: 員工郵件地址
        systems: 需要存取的系統清單，例如 ["ERP", "CRM", "GitLab", "Jira"]

    Returns:
        權限分配結果
    """
    if email not in EMPLOYEE_ACCOUNTS:
        return {
            "success": False,
            "message": "Employee not found, please create account first",
        }

    EMPLOYEE_ACCOUNTS[email]["permissions"] = systems
    return {
        "success": True,
        "email": email,
        "granted_systems": systems,
        "message": "Permissions assigned successfully",
    }


def setup_vpn_access(email: str) -> Dict:
    """
    設定VPN遠端存取權限

    Args:
        email: 員工郵件地址

    Returns:
        VPN設定指引
    """
    if email not in EMPLOYEE_ACCOUNTS:
        return {"success": False, "message": "郵件帳號不存在"}

    vpn_config = {
        "success": True,
        "email": email,
        "vpn_server": "vpn.company.com",
        "protocol": "OpenVPN",
        "download_link": "https://company.com/downloads/vpn-client.exe",
        "instructions": [
            "1. 下載並安裝VPN客戶端",
            "2. 使用公司郵件帳號登入",
            "3. 選擇伺服器: vpn.company.com",
            "4. 首次連線需進行雙因素驗證",
        ],
    }

    EMPLOYEE_ACCOUNTS[email]["vpn_enabled"] = True
    return vpn_config


def reset_password(email: str) -> Dict:
    """
    重設帳號密碼

    Args:
        email: 員工郵件地址

    Returns:
        新的臨時密碼
    """
    if email not in EMPLOYEE_ACCOUNTS:
        return {"success": False, "message": "郵件帳號不存在"}

    new_temp_password = (
        "".join(random.choices(string.ascii_letters + string.digits, k=8)) + "!"
    )
    EMPLOYEE_ACCOUNTS[email]["password"] = new_temp_password

    return {
        "success": True,
        "email": email,
        "new_password": new_temp_password,
        "message": "密碼已重設，請立即登入並修改",
    }


def get_it_support_info(issue_type: str) -> str:
    """
    取得IT支援資訊

    Args:
        issue_type: 問題類型，例如 "硬體", "軟體", "網路"

    Returns:
        支援聯絡方式或解決方案
    """
    support_info = {
        "硬體": "硬體問題請撥打分機1234或寄信至 it-support@company.com",
        "軟體": "軟體授權問題請聯繫 software@company.com",
        "網路": "網路連線問題請確認VPN設定，或聯繫網管分機5678",
        "帳號": "帳號相關問題請提供員工編號至 accounts@company.com",
    }

    return support_info.get(
        issue_type, "請撥打IT服務台總機: 1234，或寄信至 it-support@company.com"
    )
