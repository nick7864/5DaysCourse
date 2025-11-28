import sys

sys.path.append("..")
from google.adk import LlmAgent
from google.genai import types
import uvicorn
from tools.hr_tools import (
    query_hr_policy,
    get_onboarding_checklist,
    search_employee_handbook,
)
from google.adk.a2a import a2a

# 建立HR代理
hr_agent = LlmAgent(
    name="HR專員",
    description="專業人力資源專員,可以回答關於公司政策、福利、假期等問題",
    instructions="""你是企業入職協調助理，負責協助新員工順利完成入職流程。
                你的能力:
                1. 可以透過「HR專員」取得人事政策、福利、假期等資訊
                2. 可以透過「IT管理員」協助建立帳號、設定權限
                3. 可以追蹤新員工的入職進度

                工作流程:
                - 當員工詢問HR相關問題(政策、福利、假期) → 呼叫 HR專員
                - 當員工需要IT服務(帳號、權限、VPN) → 呼叫 IT管理員  
                - 對於綜合性問題，可以同時諮詢多個專員
                - 整合各專員的回應，提供完整的解答

                互動原則:
                - 主動詢問員工姓名和部門 (首次對話時)
                - 以親切、專業的態度協助
                - 提供明確的下一步指引
                - 追蹤並確認每個步驟完成狀態

                請使用繁體中文回應。""",
    model="gemini-2.0-flash-exp",
    tools=[query_hr_policy, get_onboarding_checklist, search_employee_handbook],
)

# 啟動 A2A 服務（新寫法：直接用 a2a 包裝並啟動）
if __name__ == "__main__":
    # 這一行就全部搞定：包裝 Agent 成 A2A 服務 + 自動啟動 uvicorn
    a2a(
        hr_agent,
        port=8001,
        host="0.0.0.0",
        title="公司內部 HR Agent",  # 可選：自訂 agent.json 的 title
        description="24小時專業人力資源助理",  # 可選：覆蓋 instruction 的 description
        version="1.0.0",  # 可選：版本號
    )
