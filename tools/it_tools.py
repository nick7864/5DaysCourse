"""IT部門專用工具函式"""

import os
import random
import string
from typing import Dict, List

import gspread
from dotenv import load_dotenv

load_dotenv()


def _get_credentials_path() -> str:
    """取得 credentials.json 的絕對路徑"""
    service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")
    if not service_account_file:
        return ""

    # 如果已經是絕對路徑，直接返回
    if os.path.isabs(service_account_file):
        return service_account_file

    # 否則相對於專案根目錄（.env 所在的目錄，即 tools 的上層目錄）
    current_file = os.path.abspath(__file__)  # 取得當前檔案的絕對路徑
    project_root = os.path.dirname(os.path.dirname(current_file))  # tools 的上層
    return os.path.join(project_root, service_account_file)


def _load_employee_data_from_sheet() -> Dict:
    """從 Google Sheet 載入員工資料"""
    try:
        service_account_file = _get_credentials_path()
        sheet_id = os.getenv("SHEET_ID")
        sheet_name = os.getenv("SHEET_NAME")
        worksheet_name = os.getenv("WORKSHEET_NAME")

        if not service_account_file:
            print("Warning: Google Sheet credentials not found in .env")
            return {}

        gc = gspread.service_account(filename=service_account_file)

        if sheet_id:
            sh = gc.open_by_key(sheet_id)
        elif sheet_name:
            sh = gc.open(sheet_name)
        else:
            print("Warning: Neither SHEET_ID nor SHEET_NAME found in .env")
            return {}

        # 嘗試開啟指定的工作表，如果沒指定則開第一個
        if worksheet_name:
            worksheet = sh.worksheet(worksheet_name)
        else:
            worksheet = sh.sheet1

        records = worksheet.get_all_records()

        accounts = {}
        for row in records:
            # 假設 Sheet 欄位: username, email, password, vpn, permissions
            email = row.get("email")
            if not email:
                continue

            permissions_str = row.get("permissions", "")
            permissions = (
                [p.strip() for p in permissions_str.split(",")]
                if permissions_str
                else []
            )

            accounts[email] = {
                "username": row.get("username"),
                "email": email,
                "password": row.get("password"),
                "vpn": row.get("vpn"),
                "permissions": permissions,
            }
        return accounts
    except Exception as e:
        print(f"Error loading data from Google Sheet: {e}")
        return {}


def _append_to_sheet(employee_data: Dict) -> bool:
    """將新員工資料寫入 Google Sheet"""
    try:
        # 讀取環境變數
        service_account_file = _get_credentials_path()
        sheet_id = os.getenv("SHEET_ID")
        sheet_name = os.getenv("SHEET_NAME")
        worksheet_name = os.getenv("WORKSHEET_NAME")

        # 檢查環境變數是否設定
        if not service_account_file:
            print("Warning: Google Sheet credentials not found in .env")
            return False

        gc = gspread.service_account(filename=service_account_file)

        if sheet_id:
            sh = gc.open_by_key(sheet_id)
        elif sheet_name:
            sh = gc.open(sheet_name)
        else:
            print("Warning: Neither SHEET_ID nor SHEET_NAME found in .env")
            return False

        if worksheet_name:
            worksheet = sh.worksheet(worksheet_name)
        else:
            worksheet = sh.sheet1

        # 將 permissions 轉換為逗號分隔的字串
        permissions_str = ",".join(employee_data.get("permissions", []))

        # 準備要寫入的資料行（對應 Sheet 欄位順序）
        row_data = [
            employee_data.get("username", ""),
            employee_data.get("email", ""),
            employee_data.get("password", ""),
            employee_data.get("vpn", ""),
            permissions_str,
        ]

        # 附加到 Sheet 的最後一行
        worksheet.append_row(row_data)
        print(
            f"Successfully added employee {employee_data.get('email')} to Google Sheet"
        )
        return True

    except Exception as e:
        print(f"Error writing to Google Sheet: {e}")
        return False


# 模擬IT帳號資料庫 (改為從 Sheet 讀取)
EMPLOYEE_ACCOUNTS = _load_employee_data_from_sheet()


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

    # 準備新帳號資料
    new_account = {
        "username": username,
        "email": email,
        "password": temp_password,
        "status": "active",
        "permissions": [],
    }

    # 寫入 Google Sheet
    sheet_success = _append_to_sheet(new_account)

    # 同時更新記憶體中的資料（使用 email 作為 key）
    EMPLOYEE_ACCOUNTS[email] = new_account

    return {
        "email": email,
        "initial_password": temp_password,
        "message": "Account created successfully"
        + (
            " and synced to Google Sheet"
            if sheet_success
            else " (failed to sync to sheet)"
        ),
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
