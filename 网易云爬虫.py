import os
import requests
from bs4 import BeautifulSoup
import re
import time
import sys

user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

def get_music_data(url):
    """
        用于获取歌曲列表中的歌曲信息
    """
    headers = {'User-Agent':user_agent}
    webData = requests.get(url,headers=headers).text

    soup = BeautifulSoup(webData,'lxml')
    find_list = soup.find('ul',class_="f-hide").find_all('a')

    tempArr = []
    for a in find_list:
        music_id  = a['href'].replace('/song?id=','')
        music_name = a.text
        tempArr.append({'id':music_id,'name':music_name})
    return tempArr

def get(values,output_path):
    """
        用于下载歌曲
    """
    downNum    = 0
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    for x in values:
        x['name'] = re.sub(rstr, "_", x['name'])# 替换字符串中的匹配项
        if not os.path.exists(output_path + os.sep + x['name'] + '.mp3'):
            print('[*] '+ x['name'] + '.mp3 下载中...')
            url = 'http://music.163.com/song/media/outer/url?id=' + x['id'] + '.mp3'
            try: 
                save_file(url , output_path + os.sep  + x['name'] + '.mp3')
                downNum = downNum + 1
                print('[+] '+ x['name'] + '.mp3 下载完成 !')
            except:
                print('[+] '+ x['name'] + '.mp3 下载失败 !')
    print('[+] 共计下载完成歌曲 ' + str(downNum) + ' 首 !')

def save_file(url,path):
    """
        用于保存歌曲文件
    """
    headers = {'User-Agent':user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Upgrade-Insecure-Requests':'1'}
    response = requests.get(url,headers=headers)
    f = open(path, 'wb')
    f.write(response.content)
    f.flush()

def poc_head():
    print("""
     __      _______.___._____.___.   __________               __  .__.__          
    /  \    /  \__  |   |\__  |   |   \______   \ ____ _______/  |_|__|  |   ____  
    \   \/\/   //   |   | /   |   |    |       _// __ \\____ \   __\  |  | _/ __ \ 
     \        / \____   | \____   |    |    |   \  ___/|  |_> >  | |  |  |_\  ___/ 
      \__/\  /  / ______| / ______|____|____|_  /\___  >   __/|__| |__|____/\___  >
           \/   \/        \/     /_____/      \/     \/|__|                     \/
                                            
                                                    author      昊辰
                                                    博客：      www.haochen1204.com
                                                    公众号：    霜刃信安
            """)

def main():
    url = ''
    output_path = sys.argv[0][0:len(sys.argv[0])-len(os.path.basename(sys.argv[0]))]+'music_'+time.strftime('%Y%m%d%H%M', time.localtime())
    poc_head()

    url = input('请输入歌单的网址:').replace("#/","")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    music_list = get_music_data(url)
    print('[+] 歌单获取成功！ 共计',len(music_list),'首歌曲！')
    get(music_list,output_path)
    print('[+] 歌曲存放目录为 '+output_path+' 文件')
    print('[+] 程序运行结束 10秒后自动退出')
    time.sleep(10)
main()
