#coding=utf-8
import sys
import threading
from time import ctime,sleep
from httplib import HTTPConnection



###########################################################################

def jia(a,b):
    c=a+b
    return c

#############################################################################

def automation():
    browser = Browser()
    browser.visit('http://www.baidu.com')
    all = browser.find_by_tag('a')
    print(all[0])
    print(all[1])

    for ttt in all:
        print(ttt)

    def jia(a,b):
        c=a+b
        return c


    bob=jia(1,2)
    print bob
    ttt.click()
    browser.goback()

    browser.fill('wd', 'test')
    button = browser.find_by_id('su')
    button.click()
    browser.find_by_name('su').click()
    if browser.is_text_present('splinter.readthedocs.org'):
        print "Yes, found it! :)"
    else:
        print "No, didn't find it :("
    all = browser.findElements(By.tagName("a"))
    browser.quit()

    for element in all:
        element.click()

#######################################################################################

def log():
    man = []
    other = []
    try:
        data = open('C:\\Python27\\test.txt')
        for each in data:
            try:
                (role,spake) = each.split(":")
                spake = spake.strip()
                if role == 'Man':
                    man.append(spake)
                elif role == 'Other Man':
                    other.append(spake)
            except ValueError:
                pass
        data.close()
    except IOError:
        print('The datafile is missging!')

    try:
        man_file = open('C:\\Python27\\man_data.txt','a')
        other_file = open('C:\\Python27\\other_data.txt','a')

        n =1
        while n<10:
            n=n+1
            man_file.writelines('\n\nxxxxxxxxxxx')
            other_file.writelines('\n\nxxxxxxxxxxxxx')
  
        print(man, man_file)
        print(other, other_file)
    except IOError as err:
        print('File error' + err ) 
    finally:
        man_file.close()
        other_file.close()

###############################################################################
"""
def print_qinghama(the_list,indent =False,level=0, fn=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fn)
        else:
            if indent:
                for tab_stop in range(level):
                    print( file = fn)
            print(each_item, file = fn )
"""  

#############################################################################      

def dump_load():
    with open('C:\\Python27\\test.txt','wb') as logfile:
        pickle.dump([1,2,'three'],logfile)


    with open('C:\\Python27\\test.txt','rb') as logrestorefile:
        a_list = pickle.load(logrestorefile)

    print(a_list) 
    
 #############################################################################   

def mystore():   
    data = [4,6,22,6,9,7,2,4]
    print data
    data.sort()
    print data

 #############################################################################


class Athlete:
    def _init_(self,a_name,a_dob=None,a_times=[1]):
        self.name = a_name
        self.dob = a_dob
        self.time = a_times

    def add(a,b):
        c = a + b
 
 
 ############################################################################
 
def suiji():
    n=0
    while n<10:
        print n
        n= n+1
        print random.randint(1,99) 
 ############################################################################  
 
def suijiupdate():
    print '子行不行啊'

    hehe = open('C:\\Python27\\logfile\\log.txt','w')
    #print hehe.readline()
    n=0
    while n<10:
        print n
        hehe.writelines('n的值：'+ str(n)+ '\n')
        n= n+1
        print random.randint(1,99) 
        hehe.writelines('随机数的值：'+ str(random.randint(1,99)) + '\n')

    hehe.close()

 ############################################################################ 
 
