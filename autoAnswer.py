import Utils, study
import json, os


DEFAULT_SCHOOL_NAME = ""
"""这个常量的作用是暂存学校名，当同时输入的多个帐号来自同一个学校，用此避免重复地输入学校名"""


def start(Parse, userExamPlanId, examPlanId, questionList):
    with open("questionData.json", "r", encoding="utf-8") as r:
        data = json.load(r)
    questionIndex = 1
    for q in questionList:
        questionId = q["id"]
        print(f'({questionIndex})[{q["typeLabel"]}]{q["title"]}', end="")
        questionIndex += 1
        optionList = q["optionList"]
        try:
            newOpt = False
            answer = data[questionId]
            answerIds = answer["answerIds"]
            optAnswerIds = []
            for opt in optionList:
                optAnswerIds.append(opt["id"])
            for answerId in answerIds:
                if answerId not in optAnswerIds:
                    newOpt = True
            if newOpt:
                print("")
                for option in optionList:
                    print(f"{optionList.index(option)}.{option['content']}")
                answerIndexs = str(input("选项未收录，请手动选择答案:"))
                answerIndexs = answerIndexs.split(",")
                for i in answerIndexs:
                    answerIds.append(optionList[int(i)]["id"])
        except:
            print("")
            answerIds = []
            for option in optionList:
                print(f"{optionList.index(option)}.{option['content']}")
            answerIndexs = str(input("题目未收录，请手动选择答案:"))
            answerIndexs = answerIndexs.split(",")
            for i in answerIndexs:
                answerIds.append(optionList[int(i)]["id"])
        answerIds = str(answerIds).replace("'", "").replace(" ", "")[1:-1:1]
        code = 1
        while code != 0:
            respose = Parse.recordQuestion(
                userExamPlanId, questionId, answerIds, examPlanId
            )
            code = int(respose["code"])
            if code == 0:
                print(" ok", end="\n\n")
            else:
                print(f"答题失败 {respose}")
    input("答题结束，提交试卷请按Enter")
    print("提交试卷中...")
    result = Parse.submitPaper(userExamPlanId)
    if int(result["code"]) == -1:
        print(f"提交失败 {result}")
    else:
        print(f'得分: {result["data"]["score"]}')


def main():
    global DEFAULT_SCHOOL_NAME
    print("输入学校名、帐号、密码，结束输入请按 Ctrl + C")
    schoolName = input(f"请输入学校名称(当前默认学校为 {DEFAULT_SCHOOL_NAME} ):")
    id = input("请输入学号:")
    password = input("请输入密码:")
    if schoolName == "":
        schoolName = DEFAULT_SCHOOL_NAME
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
                s = "y"
                if s in ["y", "Y"]:
                    study.study(
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
            print("若出现未收录，请于答题结束后运行importData或者importOneReviewPaper，以便及时更新题库。")
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
