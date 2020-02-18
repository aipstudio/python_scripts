#!/usr/bin/python
# -*- coding: utf-8 -*-
import psutil

for x in range(3):
    print(psutil.cpu_percent(interval=1, percpu=True))
