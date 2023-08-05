# -*- coding: utf-8 -*-
"""
@author: weber.juche@gmail.com
@time: 2017/1/4 14:10

    “库表元模型”建表函数封装
    ~~~~~~~~~~~~~~~~~~~~~~
"""
import sys
from weberFuncs import PrintTimeMsg,GetCurrentTime
from schemaFuncs import GenerateListOfCreateSqlFmDB
from CDBConnection import CDBConnection
from CDBCursor import CDBCursor

def ProcessCursorFunc(dictEngine,sDbName,cbDealFunc):
    """
        执行回调函数并返回结果
    """
    with CDBConnection(dictEngine=dictEngine,sDbName = sDbName) as dbConn:
        with CDBCursor(dbConn) as (conn,cursor):
            return cbDealFunc(dbConn, conn, cursor)

def ProcessCursorTxFunc(dictEngine,sDbName,cbDealFunc):
    """
        采用事务执行回调函数并返回结果
    """
    with CDBConnection(dictEngine=dictEngine,sDbName = sDbName) as dbConn:
        with CDBCursor(dbConn) as (conn,cursor):
            try:
                if cbDealFunc(dbConn, conn, cursor):
                    conn.commit()
                    PrintTimeMsg('ProcessCursorTxFunc.commit!')
                    return True
            except Exception as e:
                PrintTimeMsg('ProcessCursorTxFunc.e=(%s)' % (str(e)))
            conn.rollback()
            PrintTimeMsg('ProcessCursorTxFunc.rollback!')
            return False

def DoCreateTablesInDBSchema(dictEngine,sDbName,dictSchemaDB):
    """
        执行“库表元模型”建表操作, 返回结果字典
    """
    def cbCreateTable(dbConn, conn, cursor):
        listSQL = GenerateListOfCreateSqlFmDB(dictSchemaDB, dbConn.getEngine())
        for sSQL in listSQL:
            try:
                ret = cursor.execute(sSQL)
                PrintTimeMsg("DoCreateTablesInDB.sSQL=(%s)=%s" %(sSQL,ret))
            except Exception as e:
                if dbConn.checkIsTabCrtEXT(e):
                    PrintTimeMsg("DoCreateTablesInDB.sSQL=(%s)=TabCrtEXT" %(sSQL))
                    continue
                # PrintTimeMsg("CDBConnection.e=(%s)" % str(e))
        dictOK = {"errno":0, "errmsg":"create table (%s) OK" % sDbName}
        return dictOK
    ProcessCursorFunc(dictEngine,sDbName,cbCreateTable)

#--------------------------------------
def TestDoCreateTablesInDBSchema():
    from testDictParam import ReturnMysqlDictParamDB,ReturnDBSchemaOfTest
    from exampleSchema import ReturnSchemaExample
    dictSchemaExample = ReturnSchemaExample()
    DoCreateTablesInDBSchema(dictEngine=ReturnMysqlDictParamDB(),sDbName = "test",
                             dictSchemaDB=dictSchemaExample)
    DoCreateTablesInDBSchema(dictEngine=ReturnMysqlDictParamDB(),sDbName = "test",
                             dictSchemaDB=ReturnDBSchemaOfTest())

#--------------------------------------
if __name__ == '__main__':
    TestDoCreateTablesInDBSchema()
