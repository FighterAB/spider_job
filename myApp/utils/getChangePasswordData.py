from myApp.models import User
import hashlib


def changePassword(userInfo, passwordInfo):
    oldPwd = passwordInfo['oldpassword']
    newpassword = passwordInfo['newpassword']
    checknewpassword = passwordInfo['checknewpassword']
    md5 = hashlib.md5()
    md5.update(oldPwd.encode())
    oldPwd = md5.hexdigest()
    if oldPwd=='' or newpassword=='' or checknewpassword=='' : return '不允许为空'
    if oldPwd != userInfo.password: return "原始密码不正确"
    if newpassword != checknewpassword:return "新密码两次输入不一致"
    md5 = hashlib.md5()
    md5.update(newpassword.encode())
    newpassword = md5.hexdigest()

    userInfo.password = newpassword
    userInfo.save()
