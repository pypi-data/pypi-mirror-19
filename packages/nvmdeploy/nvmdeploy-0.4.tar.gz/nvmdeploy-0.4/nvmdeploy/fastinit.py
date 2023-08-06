# coding=utf-8
import os
import getpass
import yaml
from nvmjenkins import verifyUser, submitTask

config_dir = os.path.expanduser('~') + '/.nvm_deploy/'
config_file = config_dir + 'nvm_deploy_config.yaml'
AGREE_SELECTIONS = ['Y', 'y']
DISAGREE_SELECTIONS = ['N', 'n']

def need_init():
    return not configFileExists()

def configFolderExists():
    return os.path.isdir(config_dir)

def configFileExists():
    return configFolderExists() and os.path.isfile(config_file)

def createConfigFolderIfNeeded():
    if not configFolderExists():
        print('创建配置文件夹中...\n')
        os.mkdir(config_dir)

def startInit():
    print('====== 需要初始化 ======\n')
    jenkins_name = raw_input("jenkins id: ")
    jenkins_pwd = getpass.getpass("jenkins password: ")
    print('====== 验证中。。 ======\n')
    user = verifyUser(jenkins_name, jenkins_pwd)
    if user == None:
        print('====== 验证失败 ======\n')
        return
    print('====== 验证通过 ======\n')
    task = createTask()

    createConfigFolderIfNeeded()
    saveConfigFile(jenkins_name, jenkins_pwd, task['task_name'],
                   task['task_git_uri'], task['task_use_bump'],
                   task['task_branch'], task['task_slack'])
    print('初始化成功')

def saveConfigFile(uname, upwd, tname, turi, tbump, tbranch, tslack):
    task = {
        'task_name': tname,
        'task_use_bump': tbump,
        'task_git_uri': turi,
        'task_branch': tbranch,
        'task_slack': tslack
    }
    config = {
        'username': uname,
        'password': upwd,
        'tasks': [ task ]
    }
    f = open(config_file, 'w')
    yaml.dump(config, f)
    f.close()

def readConfigFile():
    s = yaml.load(file(config_file))
    return s

def createTask():
    print('====== 从 Eleme_iOS_pod_release 模板新建任务 ======\n')
    task_name = raw_input("任务名称: ")
    task_git_uri = raw_input("GIT_URI: ")
    task_use_bump = raw_input("使用 BUMP? (Y/n): ")
    if len(task_use_bump) == 0:
        task_use_version = False
    else:
        task_use_version = not task_use_bump in AGREE_SELECTIONS
    if task_use_version:
        print('将使用指定 Version发版')
    remote_branch = raw_input("指定分支(master): ")
    if len(remote_branch) == 0:
        remote_branch = 'master'
    slack_name = raw_input("Slack提醒(@somebody): ")
    return {
        'task_name': task_name,
        'task_git_uri': task_git_uri,
        'task_use_bump': not task_use_version,
        'task_branch': remote_branch,
        'task_slack': slack_name
    }

def addTask():
    task = createTask()
    config = readConfigFile()
    tasks = config['tasks']
    tasks.append(task)
    config['tasks'] = tasks
    f = open(config_file, 'w')
    yaml.dump(config, f)
    f.close()
    print("======= 添加成功 ======")

def reInit():
    del_confirm = raw_input("\033[1;31;40m 将要删除所有配置并重新初始化 (N/y): \033[0m")
    if del_confirm in AGREE_SELECTIONS:
        if configFileExists():
            os.remove(config_file)
            print("\n删除成功\n")
        startInit()

def deleteTask(name):
    config = readConfigFile()
    tasks = config['tasks']
    task = None
    for s in tasks:
        if s['task_name'] == name:
            task = s
    try:
        index = tasks.index(task)
        del tasks[index]
    except:
        print("未找到这个名字的 task")
    else:
        config['tasks'] = tasks
        f = open(config_file, 'w')
        yaml.dump(config, f)
        f.close()
        print '删除成功\n'

def listTask():
    config = readConfigFile()
    tasks = config['tasks']
    if len(tasks) == 0:
        print('    没有 Task\n')
        return
    for task in tasks:
        print '=============================\n'
        print("任务名: " + task['task_name'])
        print("Git URI: " + task['task_git_uri'])
        dieDai = "bump" if task['task_use_bump'] == True else "version"
        print("迭代方式: " + dieDai)
        print("目标分支: " + task['task_branch'])
        print("Slack通知: " + task['task_slack'])
        print '\n'

def doTask(name):
    config = readConfigFile()
    tasks = config['tasks']
    task = None
    for s in tasks:
        if s['task_name'] == name:
            task = s
    if task == None:
        print '未找到指定名称的 Task'
        return
    submitTask(config['username'], config['password'], task)