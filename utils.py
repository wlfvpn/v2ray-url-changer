import yaml


def load_config(path='config.yaml'):
    with open(path, 'r') as stream:
        config = yaml.safe_load(stream)
    return config
    
def get_cf_ip():
    from collections import defaultdict
    import requests

    url = "http://bot.sudoer.net/best.cf.iran"
    response = requests.get(url)
    data = response.text.strip().split('\n')
    net = defaultdict(str, {"MCI":"HamrahAval", "RTL":"Rightel", "AST":"Asiatek", "IRC":"Irancel", "SHT":"Shatel", "MKB":"Mokhaberat", "MBT":"Mobinnet", "ZTL":"Zitel", "PRS":"ParsOnline"})
    data_list = []
    for i in data:
        parts = i.split()
        if parts[0] not in net.keys():
                continue
        if len(parts)>=3:
            data_dict = {'Name': parts[0], 'IP': parts[1], 'Time': parts[2],"DESC":net[parts[0]]}
        else:
            data_dict = {'Name': parts[0], 'IP': None, 'Time': None, "DESC":None}
        data_list.append(data_dict)
    return data_list

def alternate(url):
    import re

    ### get address
    addr_match = re.search(r'@([^:]+):', url)
    if addr_match:
        address = addr_match.group(1)
    else:
        return
    ### get host and add it
    host = None
    match_host = re.search(r'host=([^&#]+)', url)
    if match_host:
        host = match_host.group(1)
    else:
        host = address
        url_parts = url.split("#")
        url = url_parts[0] + f"&host={host}#" + url_parts[1]

    ### get sni and add it
    match_sni = re.search(r'sni=([^&#]+)', url)
    if not match_sni:
        url_parts = url.split("#")
        url = url_parts[0] + f"&sni={host}#" + url_parts[1] 

    cf_good_ips = get_cf_ip()
    urls = []
    for cf_ip in cf_good_ips:
        if cf_ip["IP"]:
            new_url = url.replace(address, cf_ip["IP"],1)
            url_parts = new_url.split("#")
            new_url +=  f'-{cf_ip["DESC"]}'
            urls.append(new_url)
    return urls


def check_vless_trojan_format(string):
    import re
    pattern = re.compile(r'(vless|trojan)://([^@]+?)@([^:]+?):(\d+)\?([^#]+?)#(.+?)')
    match = pattern.match(string)
    if match:
        return True
    else:
        return False