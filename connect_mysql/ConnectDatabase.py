# -*- coding: utf-8 -*-
from typing import Any, Union
import pymysql
# 打开数据库连接
from pymysql.cursors import Cursor
import CommonMethod.ReadConfig as Rf


class ConnectMysql :
    """
    连接数据库，操作数据库
    """
    def __init__(self) :
        host, port, user, password, database, charset = Rf.Read_config().Read_mysql()
        self.db = pymysql.connect(host=host, port=int(port), user=user, password=password,
                                  database=database, charset=charset)

    def MysqlRead(self) :
        """
        连接数据库，获取查询操作
        :return: 输入游标
        """
        # 使用cursor()方法获取操作游标
        cursor: Union[Cursor, Any] = self.db.cursor()
        # 执行sql语句
        return cursor

    def MysqlWrite(self) :
        """
        连接数据库，获取写入数据库操作
        :return: 输入游标
        """
        # 使用cursor()方法获取操作游标
        cursor: Union[Cursor, Any] = self.db.cursor()
        # 执行sql语句
        return self.db

    def MysqlReadingWrite(self) :
        """
        连接数据库，获取读写数据库操作
        :return: 输入游标
        """
        # 使用cursor()方法获取操作游标
        cursor: Union[Cursor, Any] = self.db.cursor()
        # 执行sql语句
        return cursor, self.db


# a , b = ConnectMysql().MysqlReadingWrite()
# sql = "ALTER TABLE `api_case` CHANGE response response TEXT;"
# a.execute(sql)
# b.commit()  # 不能省，必须要加commit来提交到mysql中去确认执行



