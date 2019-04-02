import git
import os

class githot():

    #: git信息初始化
    def __init__(self, url, user, password, localPath):
        if url is None or localPath is None or user is None:
            raise Exception('gitApi报错: git地址,项目名,项目路径,都不能为空！')
        elif password:
            self.__gitUrl = url.replace('://', ('://%s:%s@'%(user, password)), 1)
        else:
            self.__gitUrl = url
        self.__localPath = localPath


    #: 项目克隆,以及项目与初始化
    def gitClone(self):
        try:
            repo = None
            if os.listdir(self.__localPath):
                repo = git.Repo(self.__localPath)
            else:
                repo = git.Repo.clone_from(url=self.__gitUrl, to_path=self.__localPath)
            return repo
        except Exception as e:
            raise Exception('gitApi报错: git账号密码错误！.{}'.format(e))


    #: 项目分支获取 === 需要点时间，因为先clone代码，在获取分支的
    def getBranchsFromGit(self):
        repo = self.gitClone()
        #：获取分支
        repo.git.fetch()
        branchs = repo.git.branch('-r').split('\n')
        for i in range(len(branchs)):
            branchs[i] = branchs[i].strip()
            if branchs[i].find('->') > 0:
                branchs[i] = branchs[i][15:]
        return branchs


    #: 指定项目分支,下载源代码
    def getPullFromGitByBranch(self, branch):
        if branch is None:
            raise Exception('gitApi报错: branch不能为空！')
        repo = self.gitClone()
        repo.git.checkout(branch)
        branch = branch.split('/')
        if len(branch) != 2 or branch[0] != 'origin':
            raise Exception("gitApi报错: branch参数报错, branch参数例子：origin/xxxx")
        repo.git.pull(branch[0], branch[1])
        print(branch)