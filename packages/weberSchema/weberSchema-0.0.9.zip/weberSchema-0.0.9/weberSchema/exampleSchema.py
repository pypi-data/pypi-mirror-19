# -*- coding: utf-8 -*-
"""
@author: weber.juche@gmail.com
@time: 2016/12/30 13:27

    设计并提供“库表元模型”定义示例
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

版本变更：
    2013年8月 提出数据库表元模型概念，并实现第一版本；
    2016年12月 改造完善实现第二版本；

“库表元模型”指的是，借助字典对象形式，将某个应用的数据库相关表的元数据集中定义；

表schema示例，此文档最新，WeiYF.20130829
schema_db_sample= {
    "dbname": "dbname",   # 留下数据库参数，方面将来进行数据库属性扩充
    "dbmemo": "例子库",   # 库备注
    "tables": [
    {
        "tabname": "example",   # 表名
        "tabmemo": "例子表",    # 表备注
        "fields":[              # 字段列表
            {   # 最完整说明
                "name":"operid",# 字段名
                "type":"idnew", # 字段类型，取值说明
                                # 字符串:c=char,vc=varchar,
                                # 日期：date=c(8),time=c(15)
                                # 数值：int=integer,byte=sint,float=DECIMAL(12,2),
                                # 文本：text=text,
                                # 标识：新创建标识 idnew=serial,关联标识 idval=int
                "lens":"12",    # 长度串，格式：存储长度,显示长度(缺省=存储长度)
                "title":"操作员标识", # 显示标题
                "hint":"由系统自动生成", # 录入格式提示,可以没有
                "memo":"用于标识某实体", # 字段含义说明,可以没有，用于进一步描述该字段
                "link":"tab.id", # 关联表字段描述,可以没有
                "enum":{         # 枚举型字段描述，可以没有
                  "kind":"x_LC", # 取值，L=单选，C=多选;
                                 # 采用list来描述后续参数，保持有序状态
                  "list":["A=name_A","B=name_B"]  # 枚举型取值列表说明，固定翻译参数FixParam
                  "list":"@GCODE=<GCODE>;@MNAME=<MNAME>" # @MNAME缺省取值为mname;还可以为param1,param2
                                      # GCODE=定义在usysparam表中的翻译参数标识串,mcode=mname
                                      # 利用isinstance(s,str)来区分这种可变参数情况
                },
                "initval":"x_val",  # 插入时缺省取值，若无则是必填字段；特殊取值：
                                    # "=instime"代表插入时间；"=modtime"代表最后修改时间；
                                    # "=insoper"代表插入工号；"=modoper"代表最后修改工号；
                                    # 模型里建议，每个资源有四个缺省字段: instime,insoper,modtime,modoper
                                    # 这里的工号指的工号标识operid。"link":"oper.eoperator.operid"
                                    # 特殊取值: *开始表示该字段不能被REST服务GET(也不能EDIT)
                                    #           #开始表示该字段不能被REST服务EDIT
            }
        ],
        
        "indexs":{  # 索引列表，I唯一索引,i重复索引
            "I0":"operid",        # I0决定REST服务的资源标识
            "i1":"opcode,operst"  #
        },
        "params":{  #附加参数，可以没有
            "recordnum":"1000",   # 估计记录数
        },
        # WeiYF.20161230 如下参数待考虑去留
        "resourceName":"examples",# REST资源标识串，若无则表示该表不支持REST服务
        "restFlags":"NODELETE,ONLYGET,",  # 表一级REST特殊标记，逗号分隔串；取值说明如下:
                                          # NODELETE:不提供REST风格删除DEL服务
                                          # ONLYGET:仅提供REST风格查询GET服务
        "MiddleVariable": {     # 存放dbConnection使用的sFieldListGet等中间变量
           "sFieldId":"",       # ID字段名；对于无ID、多字段联合唯一索引，则为'.'分隔开的多个字段;
           "sFieldListGet":"",  # GET返回资源的字段列表，包括ID
           "sFieldListIns":"",  # Insert插入资源的字段列表,允许为空的字段可以不列入
           "dictFieldPost":"",  # POST创建资源的初值字段字典，这些字段无需提供初值;UPDATE修改也不能修改这些字段
        },        
    }
    ],    
}

"""
###########################################################

def ReturnSchemaExample():
    """ 返回 库表元模型 示例 """
    return   {
        "dbname": "dbname",   # 留下数据库参数，方面将来进行数据库属性扩充
        "dbmemo": "例子库",   # 库备注
        "tables": [{
            "tabname": "testtab",
            "tabmemo": "测试表",
            "fields":[
                { "name":"testid", "type":"idnew", "lens":"12", "title":"测试标识" },
                { "name":"opcode", "type":"vc", "lens":"32", "title":"操作员工号", "hint":"由英文字母数字和@_符号" },
                { "name":"operst", "type":"c", "lens":"1,8", "title":"操作员状态","initval":"0",
                  "enum":{ "kind":"L", "list":["0=待改密码","A=正常使用","X=暂停使用"] }   },
                { "name":"shapasswd", "type":"vc", "lens":"40", "title":"密码", "hint":"SHA算法加密后的密码", "initval":"*" },
                { "name":"nickname", "type":"vc", "lens":"32", "title":"昵称", "hint":"中英文字母数字串", "initval":"" },
                { "name":"logincnt", "type":"int", "lens":"12", "title":"正常登录次数", "memo":"正常登录次数<=0，才可以删除改工号","initval":"#0" },
                { "name":"insoper", "type":"idval", "lens":"12", "title":"插入工号", "link":"oper.eoperator.operid", "initval":"=insoper"},
                { "name":"instime", "type":"time", "lens":"15", "title":"插入时间", "hint":"注册时间(YYYYMMDD-hhnnss)", "initval":"=instime"},
                { "name":"modoper", "type":"idval", "lens":"12", "title":"修改工号", "link":"oper.eoperator.operid", "initval":"=modoper"},
                { "name":"modtime", "type":"time", "lens":"15", "title":"修改时间", "hint":"修改时间(YYYYMMDD-hhnnss)", "initval":"=modtime"},
            ],
            "indexs":{
                "I0":"testid",
                "I1":"opcode"
            },
        },
        ]
    }

#--------------------------------------
def testReturnSchemaExample():
    from weberFuncs import PrettyPrintObj
    dictSchemaExample = ReturnSchemaExample()
    PrettyPrintObj(dictSchemaExample,'dictSchemaExample')

#--------------------------------------
if __name__ == '__main__':    
    testReturnSchemaExample()
    
