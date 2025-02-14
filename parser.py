import os, re
import getpass  # obtain the user name
import yaml
import multiprocessing, time
import subprocess
import platform


def dns_test(dns: dict):
    """
    run dns test using shell script
    """
    # ref: https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    dns_sh = os.path.join(os.getcwd(), 'dns_helper.sh')
    result = subprocess.run(dns_sh, stdout=subprocess.PIPE)  # run shell script
    # ref: https://stackoverflow.com/questions/2592764/what-does-a-b-prefix-before-a-python-string-mean
    result = result.stdout.decode(
        'utf-8')  # get the output of shell script and convert it to utf-8
    result = result.split()
    for i in range(len(result)):
        if result[i] in dns.keys():
            dns[result[i]] += float(result[i + 1])
    # print(dns)
    return

if __name__ == "__main__":
    # provider_url = input('plz paste ur proxy provider url.\n')
    provider_url = 'https://airtcplink.top/link/wUPE4AK4xzjuFkzT?clash=1'

    # use manger to keep the modified dict values
    manager = multiprocessing.Manager()
    # dns list
    dns = manager.dict({
        '223.5.5.5': 0,
        '223.6.6.6': 0,
        '119.29.29.29': 0,
        '119.28.28.28': 0,
        '114.114.114.114': 0,
        '114.114.115.115': 0,
    })

    start = time.time()
    n = 5  # how many times

    # ref: https://www.adamsmith.haus/python/examples/3205/multiprocessing-share-a-list-between-processes-using-a-%60manager%60
    for _ in range(n):
        locals()['p' + str(_)] = multiprocessing.Process(target=dns_test,
                                                        args=[dns])

    for _ in range(n):
        locals()['p' + str(_)].start()

    for _ in range(n):
        locals()['p' + str(_)].join()

    print(f'The accumulated results of {n}-time DNS test is \n {dns}')
    end = time.time()
    print(str(round(end - start, 3)) + 's')

    dns = dict(sorted(dns.items(), key=lambda item: item[1]))
    dns = list(dns.keys())
    name_serve, fallback = dns[:3], dns[3:]

    # get the clash config folder location
    clash_path = os.path.join(os.path.expanduser('~'), '.config' + os.sep + 'clash')
    config_path = os.path.join(clash_path, 'config.yaml')

    if platform.system() == 'Darwin':
        # get the path of config and provider
        for i in os.listdir(clash_path):
            if i != 'config.yaml' and i.endswith('.yaml'):
                provider = i.split('.yaml')[0]
                provider_path = os.path.join(clash_path, i)
    else:
        profile_path = os.path.join(clash_path, 'profiles')
        for i in os.listdir(profile_path):
            if i != 'list.yml':
                provider = i.split('.yml')[0]
                provider_path = os.path.join(clash_path, i)




    print(
        f'config yaml path is {config_path}; proxy provider yaml path is {provider_path}.'
    )

    config = dict()

    # config['port'] = 7890  # HTTP Proxy Port

    # config['socks-port'] = 7891  # socks5 port

    # # REF: https://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
    # if platform.system() == 'Darwin':
    #     config['redir-port'] = 7892  # redir proxy port for Linux and macOS
    # else:
    #     pass

    config[
        'allow-lan'] = False  # fobidden local area internet to elude the ssh connection error

    config['mode'] = 'Rule'  # Rule/Global/Direct

    # set the level of output log, silent is the default setting to avoid large memory cost
    # silent/info/warning/error/debug, the latter level u choose, the more detail log it outputs
    config['log-level'] = 'silent'

    config['external-controller'] = '0.0.0.0:9090'  # RESTful API

    config['secret'] = ''  # password of RESTful API

    # config['external-ui'] = 'folder'  # static web resources

    config['dns'] = {  # dns setting
        'enable': True,
        'enhanced-mode': 'fake-ip',
        'fallback': fallback,
        'listen': '0.0.0.0:1053',
        'nameserver': name_serve
    }

    config['tun'] = {  # tun mode
        'enable': True,
        'macOS-auto-detect-interface': True,
        'macOS-auto-route': True,
        'stack': 'system'
        'dns-hijack': ['tcp://8.8.8.8:53', '8.8.8.8:1053'] # fake-ip setting
    }


    config['experimental'] = {'interface-name': 'en0'}

    config['rule-providers'] = {  # https://github.com/Loyalsoldier/clash-rules
        'apple': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/apple.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/apple.txt'
        },
        'applications': {
            'behavior':
            'classical',
            'interval':
            86400,
            'path':
            './ruleset/applications.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/applications.txt'
        },
        'cncidr': {
            'behavior':
            'ipcidr',
            'interval':
            86400,
            'path':
            './ruleset/cncidr.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt'
        },
        'direct': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/direct.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt'
        },
        'gfw': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/gfw.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/gfw.txt'
        },
        'google': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/google.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/google.txt'
        },
        'greatfire': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/greatfire.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/greatfire.txt'
        },
        'icloud': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/icloud.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/icloud.txt'
        },
        'lancidr': {
            'behavior':
            'ipcidr',
            'interval':
            86400,
            'path':
            './ruleset/lancidr.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt'
        },
        'private': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/private.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt'
        },
        'proxy': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/proxy.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt'
        },
        'reject': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/reject.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt'
        },
        'telegramcidr': {
            'behavior':
            'ipcidr',
            'interval':
            86400,
            'path':
            './ruleset/telegramcidr.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/telegramcidr.txt'
        },
        'tld-not-cn': {
            'behavior':
            'domain',
            'interval':
            86400,
            'path':
            './ruleset/tld-not-cn.yaml',
            'type':
            'http',
            'url':
            'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/tld-not-cn.txt'
        }
    }

    config['proxy-groups'] = [
        {
            'name': 'Mode',
            'proxies': ['WhiteList', 'BlackList'],
            'type': 'select'
        },
        {
            'name': 'WhiteList',  # run proxy on rules and unknown situations
            'type':
            'fallback',  # REF: https://github.com/Dreamacro/clash/wiki/configuration#proxy-groups
            'url': 'http://www.google.com.hk/',
            'interval': 3600,  #s
            'tolerance': 50,  # ms
            'proxies': ['Proxy'],
        },
        {
            'name': 'BlackList',  # run proxy only on rules
            'type': 'fallback',
            'url': 'http://www.google.com.hk/',
            'interval': 3600,  #s
            'tolerance': 50,  # ms
            'proxies': ['DIRECT'],
        },
        {
            'name': 'Proxy',
            'type': 'select',
            # 'proxies': proxy_list
            'use': [
                provider,
            ]
        },
    ]

    config['proxy-providers'] = {
        provider: {
            'type': 'http',
            'path': provider_path,
            'url': provider_url,
            'interval': 3600,
            'health-check': {
                'enable': True,
                'url': 'http://www.google.com.hk/',
                'interval': 300
            }
        }
    }

    config['rules'] = [  #https://github.com/Loyalsoldier/clash-rules
        'RULE-SET,applications,DIRECT', 'DOMAIN,clash.razord.top,DIRECT',
        'DOMAIN,yacd.haishan.me,DIRECT', 'RULE-SET,private,DIRECT',
        'RULE-SET,reject,REJECT', 'RULE-SET,icloud,Proxy', 'RULE-SET,apple,Proxy',
        'RULE-SET,google,Proxy', 'RULE-SET,proxy,Proxy', 'RULE-SET,direct,DIRECT',
        'RULE-SET,lancidr,DIRECT', 'RULE-SET,cncidr,DIRECT',
        'RULE-SET,tld-not-cn,Proxy', 'RULE-SET,gfw,Proxy',
        'RULE-SET,greatfire,Proxy', 'RULE-SET,telegramcidr,Proxy',
        'GEOIP,LAN,DIRECT', 'GEOIP,CN,DIRECT', 'MATCH,Mode'
    ]

    with open(config_path, "w", encoding='utf-8') as stream:
        yaml.dump(config,
                stream,
                default_flow_style=False,
                allow_unicode=True,
                line_break='\n\n')