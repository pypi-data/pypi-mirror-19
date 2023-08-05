# -*- coding: utf-8 -*-
import random

#generates id
def generate(index):
    temp_gen_num = hex((100000 * (index + 1)) + random.randint(0,10000))
    temp_gen_id = temp_gen_num[2:]
    print (temp_gen_id)
    return temp_gen_id