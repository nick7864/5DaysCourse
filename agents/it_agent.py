import sys
sys.path.append("..")
from dotenv import load_dotenv
load_dotenv()  # 加載 .env 文件中的 API Key

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import LlmAgent
import uvicorn
from tools.it_tools import (
    create_email_acount,
    assign_system_permission,
    setup_vpn_access,
    reset_password,
    get_it_support_info,
)

# 建立IT代理
it_agent = LlmAgent(
    name="IT專員",
    description="專業IT專員,可以回答關於公司政策、福利、假期等問題",
    instruction="""你是企業入職協調助理，負責協助新員工順利完成入職流程。
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
    model="gemini-2.0-flash",
    tools=[
        create_email_acount,
        assign_system_permission,
        setup_vpn_access,
        reset_password,
        get_it_support_info,
    ],
)

# 啟動 A2A 服務
if __name__ == "__main__":
    PORT = 8002
    # 使用 to_a2a 將 Agent 轉換為 A2A 服務（需指定 port 以生成正確的 RPC URL）
    app = to_a2a(
        it_agent,
        host="localhost",
        port=PORT,
    )

    # 使用 uvicorn 啟動服務
    uvicorn.run(app, host="0.0.0.0", port=PORT)
