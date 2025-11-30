# 企業入職協調系統

這是一個使用 Google ADK (Agent Development Kit) 框架開發的 AI 代理展示專案，旨在模擬企業新員工入職時的問答與協調流程。

## 專案架構

本專案採用多代理 (Multi-Agent) 架構，由一個主要代理協調兩個功能性代理來完成任務：

1.  **協調專員 (Coordinator)**:
    *   使用者直接互動的主要代理。
    *   負責理解使用者問題，並將其分派給對應的專業代理。
    *   由 `main.py` 啟動。

2.  **人資專員 (HR Agent)**:
    *   作為一個獨立的遠端服務運行。
    *   專門處理與人力資源相關的問題 (如：公司政策、福利、假期申請等)。
    *   由 `agents/hr_agent.py` 實現。

3.  **IT 專員 (IT Agent)**:
    *   作為另一個獨立的遠端服務運行。
    *   專門處理 IT 相關問題 (如：帳號建立、權限設定、VPN 問題等)。
    *   由 `agents/it_agent.py` 實現。

## 技術棧

*   **AI 代理框架**: `google-adk`
*   **語言模型**: `google-genai` (Gemini)
*   **Web 服務**: `fastapi` & `uvicorn`
*   **環境變數管理**: `python-dotenv`

## 如何運行

請遵循以下步驟來啟動完整的系統。

### 1. 前置作業

*   確認您已安裝 Python 3.9 或更高版本。
*   建議建立並啟用虛擬環境：
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # on Windows, use `.venv\Scripts\activate`
    ```

### 2. 安裝依賴

在專案根目錄下，執行以下指令：

```bash
pip install -r requirements.txt
```

### 3. 設定環境變數

複製範例環境變數檔案，並填寫您的 Google Gemini API 金鑰。

```bash
# 在 Linux 或 macOS 上
cp .env.example .env

# 在 Windows 上
copy .env.example .env
```

接著，編輯 `.env` 檔案，將 `your_gemini_api_key_here` 替換成您自己的金鑰。

```
GOOGLE_API_KEY=your_gemini_api_key_here
HR_AGENT_URL=http://localhost:8001
IT_AGENT_URL=http://localhost:8002
```

### 4. 啟動代理服務

您需要開啟 **3 個**獨立的終端機視窗，並分別在每個視窗中啟用虛擬環境 (`source .venv/bin/activate`)。

*   **終端機 1: 啟動 HR 代理**
    ```bash
    uvicorn agents.hr_agent:app --port 8001
    ```

*   **終端機 2: 啟動 IT 代理**
    ```bash
    uvicorn agents.it_agent:app --port 8002
    ```

*   **終端機 3: 啟動主協調程式**
    ```bash
    python main.py
    ```

### 5. 開始互動

當三個服務都成功啟動後，您可以在執行 `main.py` 的那個終端機中，開始與入職協調系統進行對話。
輸入 `exit` 或 `離開` 來結束對話。

### 6. 連動google sheet

需設置google sheet的憑證，並在專案根目錄下：

1. 建立`credentials.json`
2. 建立`.env`，並填寫您的 Google Gemini API 金鑰

```python
# --- Google Sheets 連線設定 ---
# 服務帳號金鑰
SERVICE_ACCOUNT_FILE = "credentials.json"
# 您要操作的 Google Sheet 名稱
SHEET_NAME = "your_google_sheet_name"
# 您要操作的工作表名稱 (通常是第一個)
WORKSHEET_NAME = "your_worksheet_name"

SHEET_ID = 'your_google_sheet_id'
```






