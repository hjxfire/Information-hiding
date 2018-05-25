#!/usr/bin/env python3

from PIL import Image
import numpy

class LSB:
    #隐藏
    @staticmethod
    def hide(img,imgHide):
        #图片转数组
        imgArr=numpy.array(img)
        imgHideArr=numpy.array(imgHide)
        print('载体图片大小:'+str(imgArr.shape))
        print('隐藏图片大小:'+str(imgHideArr.shape))

        #将imgHide嵌入img
        j=0
        for i in range(imgHideArr.shape[0]*imgHideArr.shape[1]*imgHideArr.shape[2]): #imgHideArr中元素总个数
            tmp=bin(imgHideArr[int(i/3/imgHideArr.shape[1])][int(i/3)%imgHideArr.shape[1]][i%3])[2:].zfill(8)

            #imgHide前4位
            imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3]=int(bin(imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3])[2:].zfill(8)[:4]+tmp[:4],2)
            j+=1
            #imgHide后4位
            imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3]=int(bin(imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3])[2:].zfill(8)[:4]+tmp[4:],2)

            # #两位嵌入
            # for k in range(4):
            #     imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3]=int(bin(imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3])[:6].zfill(8)[:]+tmp[k*2:(k+1)*2],2)
            #     j+=1

        #在img末尾藏入imgHide的大小信息
        tmp=bin(imgHideArr.shape[0])[2:].zfill(16)  #宽
        i=9
        for j in range(4):
            imgArr[imgArr.shape[0]-1][imgArr.shape[1]-i][j%3]=int(bin(imgArr[imgArr.shape[0]-1][imgArr.shape[1]-i][j%3])[2:].zfill(8)[4:]+tmp[j*4:(j+1)*4],2)
            i-=1
        tmp=bin(imgHideArr.shape[1])[2:].zfill(16)  #长
        for j in range(4):
            imgArr[imgArr.shape[0]-1][imgArr.shape[1]-i][j%3]=int(bin(imgArr[imgArr.shape[0]-1][imgArr.shape[1]-i][j%3])[2:].zfill(8)[4:]+tmp[j*4:(j+1)*4],2)
            i-=1

        return Image.fromarray(imgArr)

    #提取
    @staticmethod
    def extract(img):
        imgArr=numpy.array(img)

        #提取长宽
        #宽
        i=9
        tmp=''
        for j in range(4):
            tmp=tmp+bin(imgArr[imgArr.shape[0]-1][imgArr.shape[1]-i][j%3])[2:].zfill(8)[4:]
            i-=1
        a=int(tmp,2)
        #长
        tmp=''
        for j in range(4):
            tmp=tmp+bin(imgArr[imgArr.shape[0]-1][imgArr.shape[1]-i][j%3])[2:].zfill(8)[4:]
            i-=1
        b=int(tmp,2)

        print('载体图片大小:'+str(imgArr.shape))
        print('隐藏图片大小:['+str(a)+','+str(b)+',3]')

        #提取图片
        imgHideArr=numpy.empty(shape=(a,b,3),dtype=numpy.uint8)
        j=0
        for i in range(a*b*3):
            tmp=bin(imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3])[2:].zfill(8)[4:]
            j+=1
            tmp=tmp+bin(imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3])[2:].zfill(8)[4:]
            imgHideArr[int(i/3/imgHideArr.shape[1])][int(i/3)%imgHideArr.shape[1]][i%3]=int(tmp,2)

            # #两位提取(未完)
            # tmp=bin(imgArr[int(j/3/imgArr.shape[1])][int(j/3)%imgArr.shape[1]][j%3])[2:].zfill(8)[6:]
            # imgHideArr[int(i/3/imgHideArr.shape[1])][int(i/3)%imgHideArr.shape[1]][i%3]=int(tmp,2)

        return Image.fromarray(imgHideArr)
