#randomOrg.py
import os
import requests
import random
import pickle as cPickle
import uuid
from dotenv import load_dotenv

load_dotenv()

def get_rarity(argument):
    def common():
        return ["common",80,1,18,1,16,0]
    def uncommon():
        return ["uncommon",75,1,18,0,8,1]
    def rare():
        return ["rare",90,1,20,2,16,0]
    def epic():
        return ["epic",85,1,19,1,17,2]
    def legendary():
        return ["legendary",99,2,20,3,17,1]
    def ultimate():
        return ["ultimate",94,2,20,2,17,3]

    switcher = {
    0: common(),
    1: uncommon(),
    2: rare(),
    3: epic(),
    4: legendary(),
    5: ultimate(),
    }

    return switcher.get(argument, "Invalid rarity")

def generate_block():
    myblock = ['','','','','','']
    mycode = uuid.uuid4()
    mycode = str(mycode)
    translation_table = dict.fromkeys(map(ord, '-'), None)
    mycode = mycode.translate(translation_table)

    z = 0
    for l in mycode:
        if len(myblock[z]) > 5:
            z+=1
        myblock[z]+=l

    for num in range(len(myblock)):
        myblock[num] = int(myblock[num],16)

    return myblock

def generate_char(block, count=5, first_rare=0, args=[.49,.31,.144,.04,.012,.004]):
    output = [0,0,0,0,0,0]
    for n in range(min(count,5)):
        flag=0
        val = 16777215
        vals = [val*args[0],val*args[1],val*args[2],val*args[3],val*args[4],val*args[5],]

        r=0


        for v in vals:
            val-=v
            if (block[n]>val):
                break
            r+=1
        
        if(first_rare==1 and r<2):
            first_rare=0
            r+=2

        calcs=get_rarity(r)

        c=0
        tr=calcs[1]

        random.seed(block[n])
        order=[0,1,2,3,4,5]
        stats=[0,1,2,3,4,5]
        order=random.sample(order,6)
        for i in range(6):
            if(i>0):
                if((c==calcs[3]) and (calcs[2]>0)):
                    calcs[2]-=1
                    if(calcs[2]==0):
                        calcs[3]-=1
                if((c>=calcs[5]) and (calcs[4]>0)):
                    calcs[4]-=1
                    if(calcs[4]==0):
                        calcs[5]=8

            mx=[calcs[2],calcs[3]]
            mn=[calcs[4],calcs[5]]

            if(flag): print(f'max({calcs[5]},{tr}-(({mx[0]}*{mx[1]})+((max(5-{i}-{mx[0]},0))*({mx[1]}-(min(1,{mx[0]})))))) = Max({calcs[5]},' + str(tr-((mx[0]*mx[1])+((max(5-i-mx[0],0))*(mx[1]-(min(1,mx[0])))))) + ')')

            mn[1]=max(calcs[5],tr-((min(mx[0],5-i)*mx[1])+((max(5-i-mx[0],0))*(mx[1]-(min(1,mx[0]))))))
            mx[1]=min(calcs[3],tr-((min(mn[0],5-i)*mn[1])+((max(5-i-mn[0],0))*8)))

            if(flag): print(f'i : {i}\nc : {c}\ntr: {tr}\nmx: {mx}\nmn: {mn}\n')

            ###print(calcs)
            if(i==5):
                c=tr
            else:
                if(mn[1]!=mx[1]+1):
                    c= random.randint(mn[1],mx[1])
                else:
                    c=mn[1]
            stats[order[i]] = c

            tr -= c

        ttl=0
        for i in stats:
            if(i>20 or i<8): 
                flag=1
                print(f'\n-----------------------------------\nWARNING - ERROR: STAT OUT OF BOUNDS: {i}\n-----------------------------------\n')
            ttl+=i
        if(ttl!=calcs[1]):
            flag=1
            print('\n----------------------------------------\nWARNING - ERROR: STAT TOTAL INCONSISTENT\n----------------------------------------\n')
            
        if(flag):
            print('stats: '+ str(stats))
            print('order: '+ str(order))
            print('calcs: ' + str(calcs))
            print('total | goal\n' + str(ttl) + '    | ' + str(calcs[1]))
        output[n]=(stats,r)
    output[5]=block[5]
    return output

def convert_block(blocks):
    response = ['','','','','']
    p=0 # Cycle variable - there must be a better way with for loop
    for block in blocks:
        rarity=get_rarity(block[1]) # get rarity[1] for stat total
        response[p] += str(rarity[1])
        for i in block[0]:
            response[p] += str(i)



test = generate_block()
test = generate_char(test)
print(convert_block())