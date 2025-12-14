import sys

sys.path.append("..")
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
import uvicorn
from tools.hr_tools import (
    query_hr_policy,
    get_onboarding_checklist,
    search_employee_handbook,
)
from google.adk.a2a.utils.agent_to_a2a import to_a2a

load_dotenv()  # 加載 .env 文件中的 API Key


# 建立HR代理
hr_agent = LlmAgent(
    name="HR專員",
    description="專業人力資源專員,可以回答關於公司政策、福利、假期等問題",
    instruction="""你是專業的人力資源專員 (HR Agent)，負責回答員工關於公司政策、福利、假期等問題，以及提供入職檢查清單。

                你的能力:
                1. 查詢公司HR政策 (年假、福利、工時等)
                2. 提供新員工入職檢查清單
                3. 搜尋員工手冊

                工作流程:
                - 當收到查詢政策請求時，使用 `query_hr_policy` 工具。
                - 當收到入職檢查清單請求時，使用 `get_onboarding_checklist` 工具。
                - 當收到搜尋手冊請求時，使用 `search_employee_handbook` 工具。

                互動原則:
                - 回答應準確引用政策內容。
                - 態度親切專業。
                - 若無法回答，請引導員工聯繫 HR 部門。

                請使用繁體中文回應。""",
    model="gemini-2.0-flash",
    tools=[query_hr_policy, get_onboarding_checklist, search_employee_handbook],
)

# 啟動 A2A 服務
if __name__ == "__main__":
    PORT = 8001
    # 使用 to_a2a 將 Agent 轉換為 A2A 服務（需指定 port 以生成正確的 RPC URL）
    app = to_a2a(
        hr_agent,
        host="localhost",
        port=PORT,
    )

    # 使用 uvicorn 啟動服務
    uvicorn.run(app, host="0.0.0.0", port=PORT)
