#!/usr/bin/python
# -*- coding: utf-8 -*-
# pip install hvac
import configparser
import hvac
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

def main():
    client = hvac.Client(url=config.get('VAULT', 'host'),
                         token=config.get('VAULT', 'token'))
    client.is_authenticated()
    result = client.secrets.kv.v2.read_secret_version(mount_point='devops', path='test_path')
    print(result['data']['data'])
    

if __name__ == '__main__':
    main()
