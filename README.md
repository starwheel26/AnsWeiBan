# AnsWeiBan
相关项目: [安全微伴题库](https://github.com/pooneyy/WeibanQuestionsBank) | [安全微伴自动刷课助手](https://github.com/Coaixy/weiban-tool)


## 说明

* 本项目在题库的基础上加入了自动答题，同时杂糅了自动刷课的项目
* 本项目仅供学习交流

## 使用方法

1. 安装 python
2. 执行 `pip install -r requirements.txt`
3.  * 运行  
        * `python autoAnswer.py` 自动答题
        * 导入数据
            * `python importData.py` 登录的方式导入数据
            * `python importOneReviewPaper.py` 导入 data.json 的数据，[详见](https://github.com/pooneyy/WeibanQuestionsBank#%E5%AF%BC%E5%87%BA%E9%A2%98%E5%BA%93)
        * `python exportData.py` 导出 Html/Markdown 格式的数据

