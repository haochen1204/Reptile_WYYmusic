import os
import requests
from bs4 import BeautifulSoup
import re
import sys
import getopt

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
            print('[*] '+ x['name'] + '.mp3 Downloading...')
            url = 'http://music.163.com/song/media/outer/url?id=' + x['id'] + '.mp3'
            try: 
                save_file(url , output_path + os.sep  + x['name'] + '.mp3')
                downNum = downNum + 1
                print('[+] '+ x['name'] + '.mp3 Download complete !')
            except:
                print('[+] '+ x['name'] + '.mp3 Download error !')
                f = open('log_error.txt','a')
                f.write(x['name']+'\n')
                f.close()
    print('[+] Download complete ' + str(downNum) + ' files !')

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
            """)

def my_help():
    print("""
        -h --help       查看帮助文档
        -u --url        歌单列表的网址
        -o --output     歌曲文件的存储路径(可使用绝对路径或相对路径)
                        默认为当前路径下的./music文件

        eg(网易云热歌榜):
        python3 pachong.py -u https://music.163.com/#/discover/toplist?id=3778678
        python3 pachong.py -u https://music.163.com/#/discover/toplist?id=3778678 -o ./music
    """)

def main():
    url = ''
    output_path = './music'

    poc_head()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 
        "hu:o:",
        ["help","url=","output="])
    except getopt.GetoptError as err:
        print(str(err))
        my_help()

    # 从opts中读取数据，o为参数,a为参数后带的值
    for o,a in opts:
        if o in ['-h','--help']:            
            my_help()
            return
        elif o in ['-u','--url']:
            url = a.replace("#/","")
        elif o in ['-o','--output']:
            output_path = a
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    music_list = get_music_data(url)
    print('[+] 歌单获取成功！ 共计',len(music_list),'首歌曲！')
    get(music_list,output_path)

main()
