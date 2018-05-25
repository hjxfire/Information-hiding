#!/usr/bin/env python3
#图像的LSB隐藏算法,使用载体的低4位,隐藏信息后的载体使用无损格式保存(bmp,png等)

from PIL import Image
import sys,argparse
import LSB

#隐藏
def hide(file,fileHide,outFile):
    # 打开图片文件
    img=Image.open(file)
    imgHide=Image.open(fileHide)
    img.show()
    imgHide.show()
    #处理
    img=LSB.LSB.hide(img,imgHide)
    img.show()
    img.save(outFile,quality=100)

#提取
def extract(file,outFile):
    # 打开图片文件
    img=Image.open(file)
    img.show()
    #处理
    imgHide=LSB.LSB.extract(img)
    imgHide.show()
    imgHide.save(outFile,quality=100)

#解析命令行
parser=argparse.ArgumentParser(usage='\n ./%(prog)s -h file fileHide -o outFile\n ./%(prog)s -e file -o outFile',conflict_handler='resolve',add_help=False)
parser.add_argument('-h','--hide',type=str,nargs=2,help='载体图片文件和隐藏信息图片文件')
parser.add_argument('-e','--extract',type=str,help='带有隐藏信息的图片文件')
parser.add_argument('-o','--outfile',type=str,help='输出的图片文件')
parser.add_argument('--help',action='store_true',help='显示帮助信息')
args=parser.parse_args(sys.argv[1:])

if args.help:
    print(parser.print_help())
    sys.exit()
elif args.outfile!=None:
    if args.hide!=None and args.extract==None:
        hide(args.hide[0],args.hide[1],args.outfile)
    elif args.hide==None and args.extract!=None:
        extract(args.extract,args.outfile)
else:
    print('输入不正确!')
    sys.exit()

# try:
#     opts,args=getopt.getopt(sys.argv[1:],"h:e:o:",["hide=","extract=","output=","help"])
#     print(opts)
#     print(args)
# except getopt.GetoptError:
#     print("./ImgHideLSB -h file fileHide -o outFile")
#     print("./ImgHideLSB -e file -o outFile")
#     print("./ImgHideLSB --help")
#     sys.exit()
#
# for opt,arg in opts:
#     if opt=="--help":
#         print("./ImgHideLSB -h file fileHide -o outFile")
#         print("./ImgHideLSB -e file -o outFile")
#         print("./ImgHideLSB --help")
#         sys.exit()
#     elif opt in ("-h","--hide"):
#         file=arg
#         fileHide=args[0]
#         flag=True
#     elif opt in ("-e","--extract"):
#         file=arg
#         flag=False
#     elif opt in ("-o","--output"):
#         outFile=arg
#
# if(flag):
#     hide(file,fileHide,outFile)
# else:
#     extract(file,outFile)