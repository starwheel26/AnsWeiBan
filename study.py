import toolUtils
import time, requests


def get_project_id(user_id, tenant_code, token: str) -> str:
    url = "https://weiban.mycourse.cn/pharos/index/listMyProject.do"
    headers = {
        "X-Token": token,
        "ContentType": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
    }
    data = {"tenantCode": tenant_code, "userId": user_id, "ended": 2}
    data = requests.post(url=url, headers=headers, data=data).json()["data"]
    if len(data) <= 0:
        print("已完成全部")
        exit(1)
    else:
        return data[0]["userProjectId"]


def study(tenant_code, userId, token):
    main = toolUtils.main(
        tenant_code,
        userId,
        token,
        get_project_id(userId, tenant_code, token),
    )
    # 初始化
    main.init()
    # 获取列表
    for chooseType in [2, 3]:
        finishIdList = main.getFinishIdList(chooseType)
        num = len(finishIdList)
        index = 1
        for i in main.getCourse(chooseType):
            print(f"{index} / {num}")
            main.start(i)
            time.sleep(12)
            main.finish(i, finishIdList[i])
            index = index + 1
    print("刷课完成")
