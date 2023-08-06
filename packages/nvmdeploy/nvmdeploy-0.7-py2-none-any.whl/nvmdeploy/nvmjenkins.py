# coding=utf-8
import jenkins

server_url = 'http://mobile.test.elenet.me/jenkins'

def serverWithAuth(name, pwd):
    return jenkins.Jenkins(server_url, username=name, password=pwd)

def verifyUser(name, pwd):
    server = serverWithAuth(name, pwd)
    try:
        user = server.get_whoami()
    except:
        return None
    else:
        return user

def submitTask(name, pwd, task):
    server = serverWithAuth(name, pwd)
    bump = ''
    version = ''
    if task['task_use_bump'] == True:
        bumps = ['patch', 'minor', 'major']
        selections = ['1', '2', '3']
        select = raw_input('select (1)patch (2)minor (3)major (default 1):')
        if select in selections:
            bump = bumps[selections.index(select)]
        else:
            bump = 'patch'
        print 'bump is ' + bump
    else:
        version = raw_input('input target release version:')
        if version == None or len(version) == 0:
            print('请输入正确的版本号')
            raise Exception
    params = {
        'GIT_URI': task['task_git_uri'],
        'BUMP': bump,
        'VERSION': version,
        'REMOTE_BRANCH': task['task_branch'],
        'SLACK_NAME': task['task_slack']
    }
    # print server.get_job_info('Eleme_iOS_pod_release')['lastBuild']
    try:
        print 'task 提交中 。。。'
        server.build_job('Eleme_iOS_pod_release', params)
    except BaseException:
        print BaseException
    else:
        print '\033[1;32;40m task 提交成功'

def getBuildInfo(server):
    try:
        info = server.get_job_info('Eleme_iOS_pod_release')['lastBuild']
    except BaseException:
        print BaseException
    else:
        print 'Build Number: ' + info['number']
        print 'See Build At: ' + info['url']