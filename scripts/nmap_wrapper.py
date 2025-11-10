#!/usr/bin/env python3
"""Wrapper for nmap scans exporting filtered JSON.

Requirements:
  pip install python-nmap
  nmap must be installed on the host.

Usage:
  python scripts/nmap_wrapper.py --targets 10.0.0.0/24 --ports 22,80,443 --output out.json
"""
import argparse
import json
import nmap


def scan(targets, ports):
    nm = nmap.PortScanner()
    nm.scan(hosts=targets, ports=ports, arguments='-sS -T4')
    results = []
    for host in nm.all_hosts():
        host_info = {'ip': host, 'state': nm[host].state(), 'protocols': []}
        for proto in nm[host].all_protocols():
            lports = []
            for port in nm[host][proto].keys():
                pinfo = nm[host][proto][port]
                lports.append({'port': port, 'state': pinfo.get('state'), 'name': pinfo.get('name'), 'product': pinfo.get('product')})
            host_info['protocols'].append({'protocol': proto, 'ports': lports})
        results.append(host_info)
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--targets', required=True)
    p.add_argument('--ports', default='22,80,443')
    p.add_argument('--output', default='nmap_results.json')
    args = p.parse_args()
    out = scan(args.targets, args.ports)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print('Wrote', args.output)


if __name__ == '__main__':
    main()
