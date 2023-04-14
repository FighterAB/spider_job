from django.shortcuts import  render


def errorResponse(requset,errMsg):
    return render(requset,'error.html',{
        'errMsg':errMsg
    })