import random
import matplotlib.pyplot as plt
from tkinter import *


class attribute(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def show(self):
        print('x = ',self.x, ', y = ',self.y)

'''从一个二维列表中获得skyline points'''
def skyline(list_attr):
    try:
        list_attr = sorted(list_attr, key=lambda x: x[0], reverse=False)
        i = 0
        for item in list_attr[1:]:
            temp = list_attr[i]
            if temp[1] <= item[1]:
                list_attr.remove(item)
                i -= 1
            i += 1
        return list_attr
    except:
        pass
    



def sub_sort(array, low, high):
    key = array[low]
    while low < high:
        while low < high and array[high] >= key:
            high -= 1
        while low < high and array[high] < key:
            array[low] = array[high]
            low += 1
            array[high] = array[low]
    array[low] = key
    return low


def quick_sort(array, low, high):
     if low < high:
        key_index = sub_sort(array,low,high)
        quick_sort(array,low,key_index)
        quick_sort(array,key_index+1,high)


def circle(canvas, x, y, r):
    id = canvas.create_oval((x - r, y - r, x + r, y + r),fill = 'black')



def main():
    
    root = Tk()
    c = Canvas(root, bg = 'white')
    c.pack()
    list_of_attr = []
    for i in range(100):
        list_of_attr.append([random.randint(1, 100), random.randint(1, 100)])
    for suoyou in list_of_attr:
        circle(c, 2*suoyou[0]+100,-2*suoyou[1]+220,1)
    result = skyline(list_of_attr)
    for suoyou in result:
        circle(c, 2*suoyou[0] + 100,220 -2*suoyou[1] , 3)
    x = []
    y = []

    for item in result:
        x.append(item[0])
        y.append(item[1])


    root.mainloop()
    '''
    #plt.plot(xx,yy)
    plt.plot(x, y)
    #plt.subplot(1,2,1)
    plt.show()'''
    


if __name__ == '__main__':
    array = [8, 10,9,6,4,16,5,13,26,18,2,45,34,23,1,7,3]
    quick_sort(array, 0, len(array) - 1)
    main()
