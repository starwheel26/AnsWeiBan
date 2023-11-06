# cython: language_level=3
import Utils, autoXue
import json, os, time

sleepTimeMin = 2.5


def start(Parse, userExamPlanId, examPlanId, questionList):
    with open("questionData.json", "r", encoding="utf-8") as r:
        data = json.load(r)
    for q in questionList:
        questionId = q["id"]
        print(f'[{q["typeLabel"]}]{q["title"]}', end="")
        try:
            answer = data[questionId]
            answerIds = answer["answerIds"]
        except:
            print("")
            optionList = q["optionList"]
            answerIds = []
            for option in optionList:
                print(f"{optionList.index(option)}.{option['content']}")
            answerIndexs = str(input("题目未收录，请手动选择答案:"))
            answerIndexs = answerIndexs.split(",")
            for i in answerIndexs:
                answerIds.append(optionList[int(i)]["id"])
        answerIds = str(answerIds).replace("'", "").replace(" ", "")[1:-1:1]
        Parse.recordQuestion(userExamPlanId, questionId, answerIds, examPlanId)
        print(": ok", end="\n\n")
    input("答题结束，提交试卷请按Enter")
    # print(f"答题结束，{sleepTimeMin}分钟后提交试卷")
    # time.sleep(sleepTimeMin * 60)
    print("提交试卷中...")
    result = Parse.submitPaper(userExamPlanId)
    if int(result["code"]) == -1:
        print(f"提交失败 {result}")
    else:
        print(f'得分: {result["data"]["score"]}')


def main():
    print("输入学校名、帐号、密码，结束输入请按 Ctrl + C")
    schoolNameDEFAULT_SCHOOL_NAME = "西安石油大学"
    schoolName = input(f"请输入学校名称(当前默认学校为 {schoolNameDEFAULT_SCHOOL_NAME} ):")
    id = input("请输入学号:")
    password = input("请输入密码:")
    if schoolName == "":
        schoolName = schoolNameDEFAULT_SCHOOL_NAME
    account = {"id": id, "password": password, "schoolName": schoolName}
    login_State = Utils.get_Login_State(account)
    while True:
        AnsParse = Utils.Parse(login_State)
        projects = AnsParse.listMyProject()
        print("-1.退出登录")
        for i in projects:
            print(f"{projects.index(i)}.{i['projectName']}: {i['studyStateLabel']}")
        projectIndex = int(input("请选择一个项目:"))
        if projectIndex == -1:
            break
        project = projects[projectIndex]
        userProjectId = project["userProjectId"]
        listPlan = AnsParse.listPlan(userProjectId)
        print("-1.退出登录")
        for i in listPlan:
            print(f"{listPlan.index(i)}.{i['examPlanName']}")
        planIndex = int(input("请选择一个考试:"))
        if planIndex == -1:
            break
        plan = listPlan[planIndex]
        userExamPlanId = plan["id"]
        examPlanId = plan["examPlanId"]
        preparePaper = AnsParse.preparePaper(userExamPlanId)
        if int(preparePaper["code"]) == -1:
            print(f"获取考试失败: {preparePaper['msg']}")
            if preparePaper["msg"] == "课程学习未完成":
                s = input("是否自动刷课(y/n):")
                if s in ["y", "Y"]:
                    autoXue.study(
                        login_State["tenantCode"],
                        login_State["userId"],
                        login_State["token"],
                    )
                    continue
                else:
                    break
            else:
                continue
        print(preparePaper["data"]["realName"], preparePaper["data"]["userIDLabel"])
        print(
            f'共{preparePaper["data"]["questionNum"]}道题, 限时{preparePaper["data"]["answerTime"]}分钟，总分{preparePaper["data"]["paperScore"]}分'
        )
        s = input("是否开始考试(y/n):")
        if s in ["y", "Y"]:
            questionList = AnsParse.startPaper(userExamPlanId)["questionList"]
            start(AnsParse, userExamPlanId, examPlanId, questionList)
        else:
            continue


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\n程序已退出")
            break
        except Exception as e:
            print(f"程序出错: {e}")
    os.system("pause")
