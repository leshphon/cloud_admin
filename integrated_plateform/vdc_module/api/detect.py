import json


def ansDetection(result):
    send = {}
    status = {
        202: "Normal",
        200: "Normal",
        204: "Normal",
        400: "ErrorBadRequest",
        401: "ErrorUnauthorized",
        403: "ErrorForbidden",
        404: "ErrorItemNotFound",
        409: "ErrorConflict"
    }
    send['msg'] = status.get(result.status_code, "OtherError")
    if send['msg'] == "Normal":
        send['code'] = 1
    else:
        send['code'] = 0
    try:
        temp = json.loads(result.content)
    except:
        temp = {}
    temp['detect'] = send
    return json.dumps(temp)
