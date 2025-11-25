import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent


load_dotenv()

# 建立遠端Agent代理
hr_remote = RemoteA2aAgent(
    name="人資專員",
    url=os.getenv("HR_AGENT_URL", "http://localhost:8001"),
    description="專業人力資源專員,可以回答關於公司政策、福利、假期等問題",
)

it_remote = RemoteA2aAgent(
    name="IT專員",
    url=os.getenv("IT_AGENT_URL", "http://localhost:8002"),
    description="專業IT專員,可以回答關於IT帳號、密碼、權限等問題",
)

# 建立主要代理
coordinator = LlmAgent(
    name="協調專員",
    description="專業協調專員,可以回答關於公司政策、福利、假期等問題",
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
    tools=[hr_remote, it_remote],
)

# 建立持久記憶體
session_service = DatabaseSessionService(db_path="onboarding_sessions.db")

# 建立Runner
runner = Runner(
    agent=coordinator,
    session_service=session_service,
)


async def main():
    session_id = "onboarding_session_001"

    while True:
        try:
            user_input = input("\n 您: ").strip()

            if user_input.lower() in ["exit", "quit", "結束", "離開"]:
                print("\n 感謝使用入職協作系統，祝您工作順利！")
                break

            if not user_input:
                continue

            # 執行對話
            print("\n 系統處理中...\n")
            async for chunk in runner.run_async(
                session_id=session_id, new_message=user_input
            ):
                # 即時顯示回應
                if chunk.content:
                    print(chunk.content, end="", flush=True)

            print()  # 換行

        except KeyboardInterrupt:
            print("\n\n 系統已中斷，再見！")
            break
        except Exception as e:
            print(f"\n發生錯誤: {e}")


if __name__ == "__main__":
    asyncio.run(main())
