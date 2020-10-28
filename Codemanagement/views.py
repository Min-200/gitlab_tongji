#coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import Codemanagement,Codestatistical
import django.utils.timezone as timezone
import os
import re
import models
from .models import Codemanagement
import datetime
import gitlab

Gitdata_path = "/home/shiminde/Gitlab-data"

def index(request):
	return render(request,'index.html',{'hello':'nihao'})



def RefreshGitdata(request):
	Project_name = os.listdir(Gitdata_path)
        for Project in Project_name:
		f = open(Gitdata_path+"/"+Project+"/index.html")
		html = f.read()
		table = re.findall(r'<dt(.*?)</dd>', html, re.S)
		index={}
		for i in table:
        		a=i.split("</dt><dd>")
        		index[a[0].replace(">","")] = a[1]
			print index
		index['Total Commits'] = index['Total Commits'].split()[0]
		index['Total Lines of Code'] = index['Total Lines of Code'].split()[0]
		new = models.Codemanagement.objects.create()
		#new.created_time =  models.DateTimeField(auto_now_add=True)
		new.ProjectName = index["Project name"]
		new.Generated = index['Generated']
		new.ReportPeriod = index['Report Period']
		new.TotalCommits = index['Total Commits']
		new.TotalLinesofCode = index['Total Lines of Code']
		new.Age = index['Age']
		new.TotalFiles = index['Total Files']
		new.Authors = index['Authors']
        	new.save()
	return redirect('/admin')

def get_all_gitdata(request):
	#sql_list = Codemanagement.objects.all()
	allcommits = 0
	alllines = 0
	allfiles = 0

	commits_list = Codemanagement.objects.values('TotalCommits')
	for i in commits_list:
		print i["TotalCommits"]
		allcommits = allcommits + int(i["TotalCommits"])
	
	linescode_list = Codemanagement.objects.values('TotalLinesofCode')
	for i in linescode_list:
		print i["TotalLinesofCode"]
		alllines  = alllines + int(i["TotalLinesofCode"])

	files_list = Codemanagement.objects.values('TotalFiles')
	for i in files_list:
		print i["TotalFiles"]
		allfiles  = allfiles + int(i["TotalFiles"])
	new = models.Codestatistical.objects.create()
	new.Allcommits = allcommits
	new.Allcodelines = alllines
	new.Allfiles = allfiles
	new.save()
	return redirect('/admin')

def Search_week(request):   #查询本周的数据
	now_time = datetime.datetime.now() #当前时间   21 周三
	print now_time
	day_num = now_time.isoweekday() #本周第几天    第三天
	print day_num
	week_day = now_time - datetime.timedelta(days=day_num-1)  # 2020-10-21 - (3-1) = 2020-10-19 是周一 
	print week_day
	all_datas = Codemanagement.objects.filter(created_time__range=(week_day, now_time))
	print all_datas


def Search_month(request):
	now_time = datetime.datetime.now()
	print now_time.month
	#month_datas = Codemanagement.objects.filter(created_time__month=now_time.month)
	month_datas = Codemanagement.objects.filter(created_time__month=9)
	print month_datas

def Search_year(request):
	now_time = datetime.datetime.now()
	month_year = Codemanagement.objects.filter(created_time__year=now_time.year)
	print month_year

def Pre_Seven(request):
	now_time = datetime.datetime.now()
	Pre_data = {}
	list = []
	dict = {}
	Pre_data["one"] = now_time - datetime.timedelta(days=1)
	Pre_data["two"] = now_time - datetime.timedelta(days=2)
	Pre_data["three"] = now_time - datetime.timedelta(days=3)
	Pre_data["four"] = now_time - datetime.timedelta(days=4)
	Pre_data["five"] = now_time - datetime.timedelta(days=5)
	Pre_data["six"] = now_time - datetime.timedelta(days=6)
	
	print Pre_data["one"].year,"-",Pre_data["one"].month,"-",Pre_data["one"].day
	
	Numlist = ["one","two","three","four","five","six"]
	date_list = []
	Numdict = {}
	for i in Numlist:	
		Numdict["Pre_data_%s"%i] = '{}-{}-{}'.format(Pre_data["%s"%i].year,Pre_data["%s"%i].month,Pre_data["%s"%i].day)
		#date_list.append(Numdict["Pre_data_%s"%i])
	date_list = [Numdict["Pre_data_one"],Numdict["Pre_data_two"],Numdict["Pre_data_three"],Numdict["Pre_data_four"],Numdict["Pre_data_five"],Numdict["Pre_data_six"]]
	print Numdict
	print date_list

	cur_datas = Codestatistical.objects.filter(created_time__year=now_time.year,created_time__month=now_time.month,created_time__day=now_time.day)

	for i  in cur_datas.values('Allcommits'):
		global cur_Allcommits
		cur_Allcommits =  int(i["Allcommits"])
	for i  in cur_datas.values('Allcodelines'):
		global cur_Allcodelines
		cur_Allcodelines = int(i["Allcodelines"])
	for i  in cur_datas.values('Allfiles'):
		global cur_Allfiles
		cur_Allfiles = int(i["Allfiles"])
	
	print cur_Allcommits,cur_Allcodelines,cur_Allfiles

	pre_one_datas = Codestatistical.objects.filter(created_time__year=Pre_data["one"].year,created_time__month=Pre_data["one"].month,created_time__day=Pre_data["one"].day)
	for i  in pre_one_datas.values('Allcommits'):
		pre_one_Allcommits =  int(i["Allcommits"])
	for i  in pre_one_datas.values('Allcodelines'):
		pre_one_Allcodelines = int(i["Allcodelines"])
	for i  in pre_one_datas.values('Allfiles'):
		pre_one_Allfiles = int(i["Allfiles"])
	
	pre_two_datas = Codestatistical.objects.filter(created_time__year=Pre_data["two"].year,created_time__month=Pre_data["two"].month,created_time__day=Pre_data["two"].day)
	for i  in pre_two_datas.values('Allcommits'):
		pre_two_Allcommits =  int(i["Allcommits"])
	for i  in pre_two_datas.values('Allcodelines'):
		pre_two_Allcodelines = int(i["Allcodelines"])
	for i  in pre_two_datas.values('Allfiles'):
		pre_two_Allfiles = int(i["Allfiles"])
	pre_three_datas = Codestatistical.objects.filter(created_time__year=Pre_data["three"].year,created_time__month=Pre_data["three"].month,created_time__day=Pre_data["three"].day)
	for i  in pre_three_datas.values('Allcommits'):
		pre_three_Allcommits =  int(i["Allcommits"])
	for i  in pre_three_datas.values('Allcodelines'):
		pre_three_Allcodelines = int(i["Allcodelines"])
	for i  in pre_three_datas.values('Allfiles'):
		pre_three_Allfiles = int(i["Allfiles"])
	pre_four_datas = Codestatistical.objects.filter(created_time__year=Pre_data["four"].year,created_time__month=Pre_data["four"].month,created_time__day=Pre_data["four"].day)
	for i  in pre_four_datas.values('Allcommits'):
		pre_four_Allcommits =  int(i["Allcommits"])
	for i  in pre_four_datas.values('Allcodelines'):
		pre_four_Allcodelines = int(i["Allcodelines"])
	for i  in pre_four_datas.values('Allfiles'):
		pre_four_Allfiles = int(i["Allfiles"])
	pre_five_datas = Codestatistical.objects.filter(created_time__year=Pre_data["five"].year,created_time__month=Pre_data["five"].month,created_time__day=Pre_data["five"].day)
	for i  in pre_five_datas.values('Allcommits'):
		pre_five_Allcommits =  int(i["Allcommits"])
	for i  in pre_five_datas.values('Allcodelines'):
		pre_five_Allcodelines = int(i["Allcodelines"])
	for i  in pre_five_datas.values('Allfiles'):
		pre_five_Allfiles = int(i["Allfiles"])
	pre_six_datas = Codestatistical.objects.filter(created_time__year=Pre_data["six"].year,created_time__month=Pre_data["six"].month,created_time__day=Pre_data["six"].day)
	for i  in pre_six_datas.values('Allcommits'):
		pre_six_Allcommits =  int(i["Allcommits"])
	for i  in pre_six_datas.values('Allcodelines'):
		pre_six_Allcodelines = int(i["Allcodelines"])
	for i  in pre_six_datas.values('Allfiles'):
		pre_six_Allfiles = int(i["Allfiles"])
	print cur_datas,pre_one_datas,pre_two_datas,pre_three_datas,pre_four_datas,pre_five_datas,pre_six_datas
       

	commit_list = [pre_six_Allcommits,pre_five_Allcommits,pre_four_Allcommits,pre_three_Allcommits,pre_two_Allcommits,pre_one_Allcommits,cur_Allcommits]
	print commit_list
	print type(pre_six_Allcommits)

	return render(request, "index.html",{"commit_list": commit_list,"date_list": date_list})

def get(request):
        commit_list = [56, 40, 54, 23, 12, 31]
        return render(request, "index.html",{"commit_list":commit_list})

def get_gitlab(request):
	now_time = datetime.datetime.now()
	#下面为获取前30天的数据
	day_list = []
        Pre_data = {}
	dict = {}
	pre_data_dict = {}
	dict1 = {}
	Y_list = []
	X_list = []
	X_file_list = []
	X_line_list = []
	Y_file_list = []
	Y_line_list = []
	for i in range(30):
		i = i+1
		day_list.append(i)
	#print day_list
	
	for i in day_list:
        	 #dict["pre_%s_date" % i]= now_time - datetime.timedelta(days=i)
        	 date = now_time - datetime.timedelta(days=i)
	
		 pre_data_dict["%s"%i] = Codestatistical.objects.filter(created_time__year=date.year,created_time__month=date.month,created_time__day=date.day)

	#print pre_data_dict

	for x in pre_data_dict:
		for Y in pre_data_dict[x].values('Allcommits'):
			dict1["%s_commits"% x] = int(Y["Allcommits"])
		for Y in pre_data_dict[x].values('Allcodelines'):
			dict1["%s_codelines"% x] = int(Y["Allcodelines"])
		for Y in pre_data_dict[x].values('Allfiles'):
			dict1["%s_files"% x] = int(Y["Allfiles"])
	for i in range(30):
		i = i+1
		#print i
		code = dict1.get("%s_commits" %i,-1)
		code_file = dict1.get("%s_codelines" %i,-1)
		code_lines = dict1.get("%s_files" %i,-1)
		#print code
		date = now_time - datetime.timedelta(days=i)
		X_list.append("{}-{}".format(date.month,date.day))		
		if code != -1:
			Y_list.append(dict1["%s_commits" %i])
		else:
			Y_list.append(0)
		if code_file != -1:
			Y_file_list.append(dict1["%s_files" %i])
		else:
			Y_file_list.append(0)
		if code_lines != -1:
			Y_line_list.append(dict1["%s_codelines" %i])
		else:
			Y_line_list.append(0)
	print "list ++++++++++++++++"
	#print Y_list
	#print Y_file_list
	#print Y_line_list
	Y_list = list(reversed(Y_list))	#commit 30天数据
	X_list = list(reversed(X_list)) #30天日期
	

	Y_file_list = list(reversed(Y_file_list))
	Y_line_list = list(reversed(Y_line_list))

	print type(Y_file_list[0])

	Pre_Seven_data = Y_list[-7:]   #7天的提交数据
	Pre_Seven_day = X_list[-7:]    #7天的日期

	Pre_Seven_file_data = Y_file_list[-7:] #7天的文件数
	Pre_Seven_line_data = Y_line_list[-7:] #7天的代码行数
	
	return render(request, "index.html",{"commit_list":Y_list,"X_list":X_list,"Pre_Seven_data":Pre_Seven_data,"Pre_Seven_day":Pre_Seven_day,"Pre_Seven_file_data":Pre_Seven_file_data,"Pre_Seven_line_data":Pre_Seven_line_data,"Y_file_list":Y_file_list,"Y_line_list":Y_line_list})



def TotalProject(request):  #通过API,获取所有项目的提交数,文件数,每日修改代码行数.包含所有分支的统计
	gl = gitlab.Gitlab('http://192.1.1.1', private_token='ZPgSMCpwyp')
	gl.auth()
	groups = gl.groups.list(all=True,include_subgroups=True) 
	dic = dict()
	now_time = datetime.datetime.now()
	pre_one_time = now_time - datetime.timedelta(1)

	print "开始时间:",pre_one_time
	print "结束时间",now_time

	pre_one_time_day = str(pre_one_time.month)+"-"+str(pre_one_time.day)

	start_time = pre_one_time  #01:00:00
	end_time = now_time

	projects = gl.projects.list(all=True,order_by="last_activity_at")
            #print project


	for project in projects:            #单个项目
                   #单个项目的提交列表
    		project_commits_line = 0
    		commit_list = []
		file_num = 0
    		branches = project.branches.list()#把每个项目下面的所有分支查出来
    		for branch in branches:#然后再遍历每一个分支
        		commits = project.commits.list(all=True,query_parameters={'since': start_time, 'until': end_time, 'ref_name': branch.name})  #分支下所有提交
        		if len(commits) != 0:  #如果过滤到每个提交在规定的时间里面
            			for i in commits:
                			print i.id
                			com = project.commits.get(i.id)
                			branch_commit_line = com.stats["total"]
                			if branch_commit_line >= 1:
                    				project_commits_line = project_commits_line + branch_commit_line
				
                			commit_list.append(i.id)  #将每个提交的ID添加到这个列表,最后统计当天的提交次数


			fileList = project.repository_tree(all=True,recursive=True,ref=branch.name)
    			file_num = file_num + len(fileList)
    		project_name = str(project.name)
    		project_commits_num = len(list(set(commit_list)))
		new = models.Codestatistical.objects.create()
                #new.created_time =  models.DateTimeField(auto_now_add=True)

                new.Projectname = project_name
                new.Allfiles = file_num
                new.Allcommits = project_commits_num
                new.Allcodelines = project_commits_line
    		print "项目名称:%s,文件数:%s,当天修改的行数:%s,当天提交次数:%s,提交时间:%s:" % (project_name,file_num,project_commits_line,project_commits_num,pre_one_time_day)
			 
			
		new.save()
	print "done"

def SearchProject(request,pk):
	new = Codestatistical.objects.get(pk=pk)
	#print new.Projectname,new.Allfiles,new.Allcommits,new.Allcodelines
	now_time = datetime.datetime.now()
	project = Codestatistical.objects.filter(Projectname=new.Projectname).order_by("-id")[:7]
	print project
	day_list = []
	project_files = []
	project_commits = []
	project_lines = []
	pre_seven_day_list = []
	for X in project:
		project_files.append(int(X.Allfiles))
		project_commits.append(int(X.Allcommits))
		project_lines.append(int(X.Allcodelines))
	for i in range(7):
                i = i+1
                #day_list.append(i)
		date = now_time - datetime.timedelta(days=i)
                pre_seven_day_list.append("{}-{}".format(date.month,date.day))

	while len(project_files) < 7:
		print "No"
		project_files.append(0)
	while len(project_commits) < 7:
		project_commits.append(0)
	while len(project_lines) < 7:
		project_lines.append(0)
	print pre_seven_day_list	
	project_files = list(reversed(project_files))
	project_commits = list(reversed(project_commits))
	project_lines = list(reversed(project_lines))
	pre_seven_day_list = list(reversed(pre_seven_day_list))
	print project_files  #7天的文件数据
	print project_commits
	print project_lines
	#return HttpResponse(new.Projectname)
	return render(request, "project.html",{"pre_seven_day_list":pre_seven_day_list,"project_files":project_files,"project_commits":project_commits,"project_lines":project_lines})
