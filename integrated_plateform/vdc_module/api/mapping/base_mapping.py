# coding=utf-8
import json
import ConfigParser
# 读取配置文件
import nova_mapping
import keystone_mapping

def findKey(mydisc, get_value):
    key_list = []
    value_list = []
    for key, value in mydisc.items():
        key_list.append(key)
        value_list.append(value.rstrip('*'))
    if get_value in value_list:
        get_value_index = value_list.index(get_value)
        return key_list[get_value_index]
    else:
        return None


# 生成局部字典
def partialDict(partialMapping, value):
    """
    :param partialMapping: 映射对象的局部值(最后结果的键) 'server/name' or '[networks[/uuid'
    :param value: 最后结果对应键的值 'test1233' or 'cae2d610-924d-4964-aaa8-7f49abd475e8'
    :return: 局部dict {'server': {'name': 'test1233'}} or {'networks':['uuid': 'cae2d610-924d-4964-aaa8-7f49abd475e8']}
    """
    global partialResult
    partialMapping.reverse()
    v = value
    for i in partialMapping:
        if i.find("[") >= 0:  # 带[]的局部字典
            sp = i.strip().strip("[").strip("*")
            partialResult = dict()
            partialResult[sp] = [v]
            v = partialResult
        else:
            sp = i.strip().strip("[").strip("*")
            partialResult = dict()
            partialResult[sp] = v
            v = partialResult
    # print(partialResult)
    return partialResult


def handle_dict(origin, addition, keyword):
    # type: (object, object) -> object
    layer_key = origin.keys()
    if addition.keys()[0] in layer_key:
        layer_origin = origin[addition.keys()[0]]
        layer_addition = addition[addition.keys()[0]]
        if isinstance(layer_origin, dict):
            handle_dict(layer_origin, layer_addition, keyword)
        else:
            handle_list(layer_origin, layer_addition, keyword)
    else:
        origin[addition.keys()[0]] = addition[addition.keys()[0]]


def handle_list(origin, addition, keyword):
    if addition[0].keys()[0] == keyword:
        if keyword in origin[len(origin) - 1].keys():
            origin.append({})
        origin[len(origin) - 1][addition[0].keys()[0]] = addition[0][addition[0].keys()[0]]
    else:
        handle_dict(origin[len(origin) - 1], addition[0], keyword)


# 生成全局字典并转换成json输出
def create_dict(partialMapping, value):
    """
    :param result: 递归的全局字典
    :param partialMapping: 映射对象的局部值(最后结果的键) 'server/name' or '[networks[/uuid'
    :param value: 最后结果对应键的值 'test1233' or 'cae2d610-924d-4964-aaa8-7f49abd475e8'
    :return:
    """
    result = {}
    partialResult = partialDict(partialMapping, value)
    result[partialResult.keys()[0]] = partialResult[partialResult.keys()[0]]
    return result


def create_mapping(result, params, prior):
    if isinstance(params, dict):
        if len(params) == 0:
            this_value = result.values()
            for x in range(len(this_value)):
                this_value[x] = this_value[x].rstrip('*')
            if prior.lstrip('/') in this_value:
                result[str(len(result))] = prior.lstrip('/') + '*'
            else:
                result[str(len(result))] = prior.lstrip('/')
        else:
            for x in range(len(params)):
                temp_key = params.keys()[x]
                temp_value = params[temp_key]
                next_one = prior + '/' + temp_key
                create_mapping(result, temp_value, next_one)
    elif isinstance(params, list):
        if len(params) == 0:
            this_value = result.values()
            for x in range(len(this_value)):
                this_value[x] = this_value[x].rstrip('*')
            if prior.lstrip('/').rstrip('*') in this_value:
                result[str(len(result))] = prior.lstrip('/') + '*'
            else:
                result[str(len(result))] = prior.lstrip('/') + '['
        else:
            if isinstance(params[len(params)-1], dict) is False:
                print('error! missing a list!')
            for y in range(len(params)):
                for x in range(len(params[y])):
                    temp_key = params[y].keys()[x]
                    temp_value = params[y][temp_key]
                    next_one = prior + '[/' + temp_key
                    create_mapping(result, temp_value, next_one)
    else:
        this_value = result.values()
        for x in range(len(this_value)):
            this_value[x] = this_value[x].rstrip('*')
        if prior.lstrip('/') in this_value:
            result[findKey(result, prior.lstrip('/'))] = prior.lstrip('/') + '*'
        else:
            result[str(len(result))] = prior.lstrip('/')


def js2info(info, key2keymapping):
    result = {}
    for x in range(len(info)):
        infovalue = info[info.keys()[x]]
        if isinstance(infovalue, list):
            newname = ''
            templ = []
            for y in range(len(infovalue)):
                tempd = {}
                for z in range(len(infovalue[y])):
                    newname = info.keys()[x] + '/' + infovalue[y].keys()[z]
                    newkey = findKey(key2keymapping, newname)
                    tempd[newkey] = infovalue[y][infovalue[y].keys()[z]]
                templ.append(tempd)
            result[newname] = templ
        else:
            newkey = findKey(key2keymapping, info.keys()[x])
            result[newkey] = infovalue
    return result


class Mapping(object):
    def __init__(self):
        # nova
        self.nova_create_server_key2key = nova_mapping.create_server_key2key
        self.nova_create_server_key2path = nova_mapping.create_server_key2path

        self.nova_snapshot_key2key = nova_mapping.snapshot_key2key
        self.nova_snapshot_key2path = nova_mapping.snapshot_key2path

        self.nova_create_flavors_key2key = nova_mapping.create_flavors_key2key
        self.nova_create_flavors_key2path = nova_mapping.create_flavors_key2path

        self.nova_rebuild_server_key2key = nova_mapping.rebuild_server_key2key
        self.nova_rebuild_server_key2path = nova_mapping.rebuild_server_key2path

        self.nova_rescue_server_key2key = nova_mapping.rescue_server_key2key
        self.nova_rescue_server_key2path = nova_mapping.rescue_server_key2path

        self.nova_resize_server_key2key = nova_mapping.resize_server_key2key
        self.nova_resize_server_key2path = nova_mapping.resize_server_key2path

        self.nova_create_servermeta_key2key = nova_mapping.create_servermeta_key2key
        self.nova_create_servermeta_key2path = nova_mapping.create_servermeta_key2path

        self.nova_create_keypairs_key2key = nova_mapping.create_keypairs_key2key
        self.nova_create_keypairs_key2path = nova_mapping.create_keypairs_key2path

        self.nova_update_server_key2key = nova_mapping.update_key2key
        self.nova_update_server_key2path = nova_mapping.update_key2path

        #keystone
        self.keystone_unscoped_key2key = keystone_mapping.unscoped_key2key
        self.keystone_unscoped_key2path = keystone_mapping.unscoped_key2path

        self.keystone_scoped_key2key = keystone_mapping.scoped_key2key
        self.keystone_scoped_key2path = keystone_mapping.scoped_key2path

    def info2params(self, info, key2keymapping, mapping):
        """
        :param info: json_param
        :param mapping: mapping table
        :return: restful api params in json format
        """
        try:
            rawinfodict = json.loads(info)
        # except ValueError, e:
        except:
            #print(ValueError)
            rawinfodict = info
        for e in rawinfodict.keys():
            if rawinfodict[e] == '':
                del rawinfodict[e]
                continue
            if isinstance(rawinfodict[e], dict):
                if rawinfodict[e].keys()[0] == '':
                    del rawinfodict[e]
        infodict = js2info(rawinfodict, key2keymapping)
        # print(infodict)
        result = {}
        num = 0
        for key, value in infodict.items():

            # print(key)
            # print(value)
            if isinstance(value, list):
                # print(range(len(value)))
                for x in range(len(value)):
                    for innerkey, innervalue in value[x].items():
                        # num = num + 1
                        partialMapping = mapping[innerkey].split("/")
                        patialResult = create_dict(partialMapping, innervalue)
                        handle_dict(result, patialResult, partialMapping[0].rstrip("*"))
                        # print(partialMapping)
                        # print(num)
                        # print(patialResult)
            else:
                partialMapping = mapping[key].split("/")
                patialResult = create_dict(partialMapping, value)
                handle_dict(result, patialResult, '-1')
        result = json.dumps(result)
        return result

    def params2mapping(self, params):
        """
        :param params: restful api params in json format
        :return: mapping
        """
        try:
            params = json.loads(params)
        # except ValueError, e:
        except:
            #print(ValueError)
            params = params
        result = {}
        prior = ''
        flag = create_mapping(result, params, prior)
        if flag is False:
            result = {}
        print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
        return result
