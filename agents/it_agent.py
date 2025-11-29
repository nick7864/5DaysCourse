import sys

sys.path.append("..")
from google.adk.a2a import a2a
from google.adk import LlmAgent
import uvicorn
from tools.it_tools import (
    create_email_account,
    assign_system_permissions,
    setup_vpn_access,
    reset_password,
    get_it_support_info,
)

# 建立IT代理
it_agent = LlmAgent(
    name="IT專員",
    description="專業IT專員,可以回答關於公司政策、福利、假期等問題",
    instructions="""你是企業入職協調助理，負責協助新員工順利完成入職流程。
                你的能力:
                1. 建立電子郵件帳號
                2. 分配系統權限
                3. 設定VPN存取權限
                4. 重置密碼
                5. 提供IT支援資訊

                執行任務時請:
                1.先分析任務需求
                2.依照能力列表選擇合適的工具
                3.依照工具的說明執行任務
                4.確認員工身分資訊(身分,部門)
                5.提供清晰操作指引
                6.記錄所有帳號變更
                7.強調資安注意事項
                """,
    model="gemini-2.0-flash-exp",
    tools=[
        create_email_account,
        assign_system_permissions,
        setup_vpn_access,
        reset_password,
        get_it_support_info,
    ],
)

# 啟動 A2A 服務（新寫法：直接用 a2a 包裝並啟動）
if __name__ == "__main__":
    # 這一行就全部搞定：包裝 Agent 成 A2A 服務 + 自動啟動 uvicorn
    a2a(
        it_agent,
        port=8002,
        host="0.0.0.0",
        title="公司內部 IT Agent",  # 可選：自訂 agent.json 的 title
        description="24小時專業IT助理",  # 可選：覆蓋 instruction 的 description
        version="1.0.0",  # 可選：版本號
    )
