#!/bin/bash
gitstatus="/home/gitstats/gitstats" #gitstats二进制文件
git_repo_dir="/var/opt/gitlab/git-data/repositories" #gitlab的git仓库存储位置
resultdir="/home/scm"   #结果存放的目录

#先找到目录下的所有Git库
cd $git_repo_dir 
giturl=`find . -name "*.git" | grep -v "wiki"`
for i in  $giturl
do
	git_repo=${i#*/}
	echo $git_repo
	echo "文件名字"
	echo `basename $git_repo`
	echo "目录名字"
	gitdir=`dirname $git_repo`
	echo "GitRepo路径为"
	full_git_url="$git_repo_dir/$git_repo"

	echo $full_git_url

	target_dir="$resultdir/$gitdir"
	mkdir -p $resultdir/$gitdir
	$gitstatus $full_git_url $target_dir
	
done
#根据目录的路径来截取目录层级，之后放到对应的目录中,然后创建对应的层级目录
