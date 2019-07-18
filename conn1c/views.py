from django.shortcuts import render
import requests

user1c = 'web'
pass1c = 'web'

class conn1c:
    base_url = 'http://46.174.89.208:6060/zup_Inwike/hs/Inwike/ID/'

    def load_dict(self, params, data):
        result = {}
        for key in params:
            result[key]=data[key]
        return result

    def load_list(self, prefix, start, data):
        result = []
        cnt = start
        key = '{}_{}'.format(prefix,cnt)
        while key in data:
            result.append(data.get(key,0))
            cnt += 1
            key = '{}_{}'.format(prefix, cnt)
        return result

    def emp_rating(self, emp_UID):
        payload = {'emp_UID': emp_UID}
        r = requests.get(self.base_url+'emp_rating', params=payload, auth=(user1c, pass1c))
        try:
            data = r.json()[0]
        except:
            data = {}

        print(data)
        result={}
        result['params'] = self.load_dict(['exp_emp','lvl_emp', 'raiting_emp', 'avr_knld', 'avr_soc', 'avr_resp', 'avr_activ', 'avr_innov', 'avr_ent', 'knld_12', 'soc_12', 'resp_12', 'activ_12', 'innov_12', 'ent_12'], data)
        result['months'] = self.load_list('month', 1, data)
        result['knlds'] = self.load_list('knld', 1, data)
        result['socs'] = self.load_list('soc', 1, data)
        result['resps'] = self.load_list('resp', 1, data)
        result['activs'] = self.load_list('activ', 1, data)
        result['innovs'] = self.load_list('innov', 1, data)
        result['ents'] = self.load_list('ent', 1, data)

        return result

    def emp_data(self, emp_UID):
        payload = {'emp_UID': emp_UID}
        r = requests.get(self.base_url+'emp_data', params=payload, auth=(user1c, pass1c))
        try:
            data = r.json()[0]
        except:
            data = {}

        result={}
        result['params'] = self.load_dict(['emp','Dep','org', 'position'], data)

        print(result)

        return result


