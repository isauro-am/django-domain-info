from xml import dom
from django.shortcuts import render, redirect
import socket
import requests

from django.views import View

import subprocess

# Create your views here.


def bash_command(bashCommand: str):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    output = output.decode("utf-8")

    return output


def get_txt_records(domain: str, key: str):
    txt_records = []
    bashCommand = "dig " + key + " " + domain

    output = bash_command(bashCommand)
    output = str(output)
    output = output.replace('\t', '')
    output = output.split('\n')

    for line in output:
        if "IN"+key in line:
            txt = line.split("IN"+key)
            if len(txt[1]) > 0:
                txt_records.append(txt[1])
    return txt_records


def get_ip_info(ip: str):
    # https://ipwho.is/
    r = requests.get('https://ipwho.is/'+ip)

    return r.json()


class DomainView(View):
    def post(self, request):
        domain = request.POST['domain']

        txt_records = get_txt_records(domain, 'TXT')
        dmarc_records = get_txt_records('_dmarc.' + domain, 'TXT')

        mx_records = get_txt_records(domain, 'MX')
        ns_records = get_txt_records(domain, 'NS')

        a_records = get_txt_records(domain, 'A')

        hostnames = []

        for a in a_records:
            try:
                hostnames.append(socket.gethostbyaddr(str(a))[0])
            except:
                hostnames = hostnames

        ip_list = []

        for ip in a_records:
            ip_list.append(get_ip_info(ip))

        context = {
            "data": True,
            "domain": domain,
            "txt": txt_records,
            "dmarc": dmarc_records,
            "mx": mx_records,
            "ns": ns_records,
            "a": a_records,
            "hostnames": hostnames,
            "ips": ip_list
        }
        return render(request, 'domain/domain.html', context=context)

    def get(self, request):
        context = {
            'data': False
        }

        return render(request, 'domain/domain.html', context=context)
