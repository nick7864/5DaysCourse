from typing import Dict, Optional

# HR資料庫
HR_POLICIES = {
    "annual_leave": {
        "新進員工": "到職滿3個月後，享有依比例計算的特休",
        "年資1年": "7天特休",
        "年資2年": "10天特休",
        "年資3-5年": "14天特休",
        "年資5年以上": "每年增加1天，最多30天",
    },
    "benefits": {
        "健康保險": "公司提供團體保險，涵蓋員工及眷屬",
        "退休金": "依勞基法提撥6%",
        "績效獎金": "年度績效達標可獲2-4個月獎金",
        "員工旅遊": "年度國內或國外旅遊補助",
        "育兒補助": "每月3000元育兒津貼(最多至3歲)",
    },
    "work_hours": {
        "上班時間": "09:00 - 18:00",
        "午休": "12:00 - 13:00",
        "彈性工時": "可提早/延後1小時，需主管核准",
        "遠端工作": "每週最多2天WFH",
    },
}


def query_hr_policy(category: str, sub_category: Optional[str] = None) -> str:
    """
    查詢HR政策資訊

    Args:
        category: 政策類別，可選值:
            - "annual_leave" (年假/特休)
            - "benefits" (福利)
            - "work_hours" (工作時間)
        sub_category: 子類別，例如查詢特定年資的特休天數

    Returns:
        政策說明文字

    Examples:
        query_hr_policy("annual_leave") -> 回傳所有特休規定
        query_hr_policy("benefits", "健康保險") -> 回傳健康保險說明
    """

    if category not in HR_POLICIES:
        return f"未找到類別{category}的政策,可用類別{'、'.join(HR_POLICIES.keys())}"
    policy_data = HR_POLICIES[category]
    if sub_category:
        if sub_category in policy_data:
            return policy_data[sub_category]
        else:
            return f"未找到子類別{sub_category}的政策,可用子類別{'、'.join(policy_data.keys())}"
    else:
        # 回傳全部類別資訊
        result = ""
        for key, value in policy_data.items():
            result += f"{key}: {value}\n"
        return result


def get_onboarding_checklist(employee_name: str) -> Dict:
    """
    取得新員工入職檢查清單

    Args:
        employee_name: 新員工姓名

    Returns:
        入職檢查清單字典
    """
    return {
        "employee": employee_name,
        "checklist": [
            {"item": "HR政策諮詢", "status": "未完成"},
            {"item": "IT帳號申請", "status": "未完成"},
            {"item": "福利申請", "status": "未完成"},
            {"item": "工作環境設定", "status": "未完成"},
            {"item": "工作流程熟悉", "status": "未完成"},
        ],
    }


def search_employee_handbook(keyword: str) -> str:
    """
    搜尋員工手冊

    Args:
        keyword: 搜尋關鍵字,例如 "請假", "加班", "出差"

    Returns:
        相關規定說明
    """
    handbook = {
        "請假": "請假需提前3天申請，病假當日通知主管即可。特休需經主管核准。",
        "加班": "加班需事前申請，平日加班費為1.33倍，假日為1.66倍。",
        "出差": "國內出差補助每日1000元，國外出差依地區有不同標準。",
        "考核": "每半年進行一次績效考核，評分影響年終獎金及升遷。",
    }
    if keyword in handbook:
        return handbook[keyword]
    else:
        return f"未找到關鍵字{keyword}的手冊,可用關鍵字{'、'.join(handbook.keys())}"
