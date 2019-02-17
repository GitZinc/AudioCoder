# author by LYS 2017/5/24
# for Deep Learning course
'''
1. read the whole files under a certain folder
2. chose 10000 files randomly
3. copy them to another folder and save
'''
import os, random, shutil

def getfile(fileDir):
    # 1
    pathDir = os.listdir(fileDir)
    # 2
    sample = random.sample(pathDir, 1)
    name = fileDir + sample[0]
    return name
    # print(self.name)
    # 3
    # for name in sample:
    #     shutil.copyfile(fileDir+name, tarDir+name)
# if __name__ == '__main__':
#     fileDir = "/home/phantom/Nutstore/Project/TTL_wave_ver_2.0/images/librosa_test/频域分析/cqt/"
#     tarDir = '/home/phantom/Nutstore/Project/TTL_wave_ver_2.0/images/librosa_test/频域分析/tardir/'
#     copyFile(fileDir)
