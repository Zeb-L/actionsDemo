import urllib.request
import urllib.error
import urllib.parse
import datetime
import re

ys_str = ["cctv"]
ws_str = ["卫视"]
ty_str = ["体育","cctv5","cctv-5"]
dy_str = ["影视","影院","电影","cctv6","cctv-6"]
yy_str = ["音乐","cctv15","cctv-15"]
xw_str = ["新闻","cctv13","cctv-13"]
se_str = ["少儿","卡通","动画","cctv14","cctv-14"]
gd_str = ["翡翠台","明珠","凤凰","汕尾"]

alldata_lists=[]
keep_lists=[]


def get_ua():
    import random
    user_agents = [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
		"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
		"Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
		"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"
    ]
    user_agent = random.choice(user_agents)
    return user_agent

def printlog(logstr):
	with open("log.txt","a") as file:
		timeNow = datetime.datetime.now()
		timeN= timeNow.strftime('%Y/%m/%d %H:%M:%S')
		file.write(" "+timeN+": ")
		file.write(logstr+"\n")
		file.close()

def downloadfile(dlurl,i,utype):
	global alldata_lists
	global keep_lists
	reconnect = 3
	for rc in range(reconnect):
		if rc < reconnect:
			ua = get_ua()
			headers = {'User-Agent': ua}
			try:
				_url = urllib.request.Request(dlurl,headers=headers)
				response = urllib.request.urlopen(_url, None, 10)
				data=response.read().decode('utf-8')
				if utype == "m":
					datalists=data.split("\n")
					mdata=[]
					for i in range(len(datalists)):
						if datalists[i].startswith('#EXTINF'):
							if datalists[i+1] == "\n" or datalists[i+1] == "" or datalists[i+1] == "\r":
								name = datalists[i+2]
							else:
								name = datalists[i+1]
							renameurl = str(datalists[i].split(",")[1].replace("\n","").replace("\r",""))+","+str(name.replace("\n","").replace("\r",""))
							mdata.append(renameurl)
					# # f.write(mdata)
					# print(mdata)
					alldata_lists=mdata
					printlog("\n【Success】: "+dlurl)
				elif utype == "t":
					# f.write(data)
					tdata = data.split("\n")
					for item in range(len(tdata)):
						t = tdata[item].replace("\uFEFF", "").replace("\r", "")
						t_temp = t.find(",")
						if t_temp != -1:
							alldata_lists.append(t)
					printlog("\n【Success】: "+dlurl)
				elif utype == "k":
					# f.write(data)
					kdata = data.split("\n")
					for item in range(len(kdata)):
						k = kdata[item].replace("\uFEFF", "").replace("\r", "")
						k_temp = k.find(",")
						if k_temp != -1:
							keep_lists.append(k)
					printlog("\n【Success】: "+dlurl)
				break
			except:
				printlog("\nError:【连接超时】 "+dlurl)
				printlog("重试第",str(rc+1),"次")
				if str(rc+1) == "3":
					printlog("Error:【链接失效】 "+dlurl)
				continue

def dl_file():
	with open("./data.txt",'r',encoding='UTF-8') as filecont:    
		datalists = filecont.readlines()
		filecont.close()
	for i in range(len(datalists)):
		urldata=datalists[i].split("@=")
		if urldata[0] == "m3u":
			downloadfile(urldata[1],i,"m")
		elif urldata[0] == "txt":
			downloadfile(urldata[1],i,"t")
		elif urldata[0] == "keep":
			downloadfile(urldata[1],i,"k")




def checkM3U8(m_url):
	try:
		ua = get_ua()
		headers = {'User-Agent': ua}
		r=urllib.request.Request(url=m_url,headers=headers)
		response=urllib.request.urlopen(r,timeout=2)
		if str(response.status) == '200':
			return "ok"
	except:
		return "no"
	response.close()

def jdt(start,end):
    one = end / 20
    bfb = round(start/end * 100, 2)
    if start < one:
        pt=" 进度条"+" [--------------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*2:
        pt=" 进度条"+" [#-------------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*3:
        pt=" 进度条"+" [##------------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*4:
        pt=" 进度条"+" [###-----------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*5:
        pt=" 进度条"+" [####----------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*6:
        pt=" 进度条"+" [#####---------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*7:
        pt=" 进度条"+" [######--------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*8:
        pt=" 进度条"+" [#######-------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*9:
        pt=" 进度条"+" [########------------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*10:
        pt=" 进度条"+" [#########-----------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*11:
        pt=" 进度条"+" [##########----------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*12:
        pt=" 进度条"+" [###########---------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*13:
        pt=" 进度条"+" [############--------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*14:
        pt=" 进度条"+" [#############-------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*15:
        pt=" 进度条"+" [##############------] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*16:
        pt=" 进度条"+" [###############-----] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*17:
        pt=" 进度条"+" [################----] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*18:
        pt=" 进度条"+" [#################---] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*19:
        pt=" 进度条"+" [##################--] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif one < start < one*20:
        pt=" 进度条"+" [###################-] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt
    elif start >= one*20:
        pt=" 进度条"+" [####################] "+str(bfb)+"%"+"  |  "+str(start)+"/"+str(end)
        return pt

def checkLists(lists):
    onlineList=[]
    for i in range(len(lists)):
        jdt2 = jdt(i+1,len(lists))
        print('\r',"【直播源检查】 "+str(jdt2),end=' ')
        # print("【直播源检查】 "+str(i)+" / "+str(len(lists)),end='\r')
        url=lists[i].split(",")[1]
        check_url = checkM3U8(url)
        if check_url == "ok":
            onlineList.append(lists[i])
    return onlineList

def reset_url_lists(allLists,string):
    data_lists=[]
    for i in range(len(string)):
        for j in range(len(allLists)):
            cont = allLists[j].split(",")
            searchitem = re.compile(string[i],re.IGNORECASE)
            item = searchitem.search(cont[0])
            if str(item) != "None":
                # print(cont[0].replace(" ","").replace('\uFEFF', '')+","+cont[1])
                searchttp = re.compile(r"#http",re.IGNORECASE)
                searchttp2 = searchttp.search(cont[1])
                m3u8url=[]
                if str(searchttp2) == "None":
                    m3u8url.append(cont[1])
                else:
                    m3u8urllist = cont[1].replace("#http","http").split("http")
                    for li in range(len(m3u8urllist)):
                        if m3u8urllist[li] != "":
                            m3u8url.append("http"+m3u8urllist[li])
                # print(m3u8url)
                if len(m3u8url) == 1:
                    data_lists.append(cont[0].replace(" ","").replace("\n","").replace("\t","").replace("\uFEFF", "")+","+m3u8url[0].replace("\n","").replace("\t","").replace(" ",""))
                else:
                    for y in range(len(m3u8url)):
                        data_lists.append(cont[0].replace(" ","").replace("\n","").replace("\t","").replace("\uFEFF", "")+","+m3u8url[y].replace("\n","").replace("\t","").replace(" ",""))
    return data_lists

def rd(lists):
    tem=[]
    relists=[]
    for item in range(len(lists)):
        reitem = lists[item].split(",")
        if reitem[1] != "#genre#":
            if reitem[1] not in tem:
                tem.append(reitem[1])
                relists.append(lists[item])
    tem=[]
    print("原数据:"+str(len(lists))+"  去重后: "+str(len(relists))+"\n")
    return relists


def start(lists,str_list,title):
	data_lists = reset_url_lists(lists,str_list)
	rd_data_list = rd(data_lists)
	print("开始检查\n")
	ol_d_l = checkLists(rd_data_list)
	print("\n"+title+"  【全部源数量:  "+str(len(data_lists))+"  |  去重后源数量:  "+str(len(rd_data_list))+"  |  在线源数量:  "+str(len(ol_d_l))+" 】")
	printlog("\n"+title+"  【全部源数量:  "+str(len(data_lists))+"  |  去重后源数量:  "+str(len(rd_data_list))+"  |  在线源数量:  "+str(len(ol_d_l))+" 】")
	with open("tvbox_live.txt","a", encoding='utf-8') as file:
		file.write("\n")
		file.write(title+",#genre#\n")
		for line in range(len(ol_d_l)):
			file.write(ol_d_l[line]+"\n")
		file.close()	



# 根据数据源获取到所有txt格式数据（alldata_lists）
dl_file()
start(alldata_lists,ys_str,"央视频道")
