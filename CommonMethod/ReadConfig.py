# -*- coding: utf-8 -*-
import configparser
import os
import sys


class Read_config:
    """
    读取配置文件数据
    """
    def __init__(self):
        """
        获取配置文件地址
        """
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        self.cf = configparser.ConfigParser()
        path = os.path.join(rootPath, 'config.ini')
        self.cf.read(path, encoding="utf-8")

    def Read_mysql(self):
        """
        读取配置文件，数据库信息
        :return:
        """
        host = self.cf.get("Mysql-Database", "host")
        port = self.cf.get("Mysql-Database", "port")
        user = self.cf.get("Mysql-Database", "user")
        password = self.cf.get("Mysql-Database", "password")
        database = self.cf.get("Mysql-Database", "database")
        charset = self.cf.get("Mysql-Database", "charset")
        return host, port, user, password, database, charset

    def Read_header(self, app_name):
        """
        读取配置文件，数据库信息
        :return:
        """
        modular = self.cf.get("headers", app_name)
        return modular

    def Read_header1(self):
        """
        读取配置文件，数据库信息
        :return:
        """
        modular = self.cf.get("gwmgr", "modular")
        client = self.cf.get("gwmgr", "client")
        version = self.cf.get("gwmgr", "version")
        Content_Type = self.cf.get("gwmgr", "Content-Type")
        return modular, client, version, Content_Type

    def Read_redis(self):
        """
        读取配置文件，数据库信息
        :return:
        """
        host = self.cf.get("Redis_dev", "host")
        port = self.cf.get("Redis_dev", "port")
        password = self.cf.get("Redis_dev", "password")
        db = self.cf.get("Redis_dev", "db")
        return host, port, password, db





