#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DARK NIGHT - RECONX V2.0
Gabungan: Subfinder + Httpx-toolkit
FIXED: Pake httpx-toolkit
HANYA UNTUK TESTING DENGAN IZIN!
"""

import subprocess
import sys
import os
import time
import argparse
import json
import re
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
{Fore.RED}║         {Fore.WHITE}DAFFAZXXS - SUBFINDER + HTTPX-TOOLKIT{Fore.RED}           ║
{Fore.RED}║              {Fore.WHITE}[SUBDOMAIN DISCOVERY + LIVE CHECK]{Fore.RED}              ║
{Fore.RED}╚══════════════════════════════════════════════════════════════╝{Fore.WHITE}
"""

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)
    print(f"{Fore.YELLOW}[!] HANYA UNTUK TESTING DENGAN IZIN!{Fore.WHITE}\n")

def check_tools():
    """Cek tools"""
    tools = ['subfinder', 'httpx-toolkit']
    missing = []
    
    for tool in tools:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode != 0:
            missing.append(tool)
    
    if missing:
        print(f"{Fore.RED}[!] Tools berikut tidak ditemukan: {', '.join(missing)}{Fore.WHITE}")
        print(f"{Fore.YELLOW}[*] Install dengan:{Fore.WHITE}")
        print("    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")
        print("    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest")
        print("    atau pake: apt install httpx-toolkit -y")
        sys.exit(1)
    
    print(f"{Fore.GREEN}[✓] Semua tools tersedia{Fore.WHITE}")

def get_version(tool):
    try:
        result = subprocess.run([tool, '-version'], capture_output=True, text=True)
        return result.stdout.strip().split('\n')[0]
    except:
        return "Unknown"

def run_subfinder(domain, output_file, passive=True, threads=50):
    print(f"{Fore.CYAN}[*] Menjalankan Subfinder untuk {domain}{Fore.WHITE}")
    
    cmd = ['subfinder', '-d', domain]
    if passive:
        cmd.append('-passive')
    if output_file:
        cmd.extend(['-o', output_file])
    cmd.extend(['-silent', '-t', str(threads)])
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start_time
        
        subdomains = []
        for line in result.stdout.split('\n'):
            if line.strip():
                subdomains.append(line.strip())
        
        print(f"{Fore.GREEN}[✓] Subfinder selesai: {len(subdomains)} subdomain ditemukan ({elapsed:.2f}s){Fore.WHITE}")
        return subdomains, elapsed
    
    except Exception as e:
        print(f"{Fore.RED}[✗] Error Subfinder: {e}{Fore.WHITE}")
        return [], 0

def run_httpx_toolkit(subdomains, output_file, threads=50, follow_redirects=False):
    """Jalankan httpx-toolkit"""
    if not subdomains:
        print(f"{Fore.YELLOW}[!] Tidak ada subdomain{Fore.WHITE}")
        return [], 0
    
    print(f"{Fore.CYAN}[*] Menjalankan Httpx-toolkit untuk {len(subdomains)} subdomain{Fore.WHITE}")
    
    temp_file = '/tmp/subdomains_temp.txt'
    with open(temp_file, 'w') as f:
        f.write('\n'.join(subdomains))
    
    cmd = ['httpx-toolkit', '-l', temp_file]
    cmd.append('-status-code')
    cmd.append('-title')
    cmd.append('-tech-detect')
    cmd.append('-follow-redirects')
    cmd.append('-response-time')
    cmd.append('-content-length')
    cmd.extend(['-threads', str(threads)])
    cmd.append('-silent')
    cmd.append('-no-color')
    
    if output_file:
        cmd.extend(['-o', output_file])
    
    cmd.append('-json')
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start_time
        
        live_hosts = []
        for line in result.stdout.split('\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    live_hosts.append(data)
                except:
                    pass
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        print(f"{Fore.GREEN}[✓] Httpx-toolkit selesai: {len(live_hosts)} host live ({elapsed:.2f}s){Fore.WHITE}")
        return live_hosts, elapsed
    
    except Exception as e:
        print(f"{Fore.RED}[✗] Error Httpx-toolkit: {e}{Fore.WHITE}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return [], 0

def print_summary(domain, subdomains, live_hosts, elapsed_subfinder, elapsed_httpx):
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║                         SUMMARY                               ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Fore.WHITE}")
    
    print(f"{Fore.YELLOW}[+] Domain: {domain}{Fore.WHITE}")
    print(f"{Fore.YELLOW}[+] Total Subdomain: {len(subdomains)}{Fore.WHITE}")
    print(f"{Fore.YELLOW}[+] Live Hosts: {len(live_hosts)}{Fore.WHITE}")
    print(f"{Fore.YELLOW}[+] Subfinder Time: {elapsed_subfinder:.2f}s{Fore.WHITE}")
    print(f"{Fore.YELLOW}[+] Httpx Time: {elapsed_httpx:.2f}s{Fore.WHITE}")
    print(f"{Fore.YELLOW}[+] Total Time: {elapsed_subfinder + elapsed_httpx:.2f}s{Fore.WHITE}")
    
    if live_hosts:
        print(f"\n{Fore.CYAN}[+] Live Hosts:{Fore.WHITE}")
        print(f"{'No':<4} {'URL':<50} {'Status':<8} {'Title':<30}")
        print("-" * 95)
        for i, host in enumerate(live_hosts[:20], 1):
            url = host.get('url', '')
            status = str(host.get('status_code', ''))
            title = host.get('title', '')[:30]
            print(f"{i:<4} {url:<50} {status:<8} {title:<30}")
        
        if len(live_hosts) > 20:
            print(f"{Fore.YELLOW}... dan {len(live_hosts) - 20} host lainnya{Fore.WHITE}")

def export_results(domain, subdomains, live_hosts, output_dir='results'):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    sub_file = f"{output_dir}/{domain}_subdomains_{timestamp}.txt"
    with open(sub_file, 'w') as f:
        f.write('\n'.join(subdomains))
    
    live_file = f"{output_dir}/{domain}_live_{timestamp}.txt"
    with open(live_file, 'w') as f:
        for host in live_hosts:
            f.write(host.get('url', '') + '\n')
    
    json_file = f"{output_dir}/{domain}_full_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump({
            'domain': domain,
            'timestamp': timestamp,
            'subdomains': subdomains,
            'live_hosts': live_hosts,
            'stats': {
                'total_subdomains': len(subdomains),
                'live_hosts': len(live_hosts)
            }
        }, f, indent=2)
    
    print(f"\n{Fore.GREEN}[✓] Hasil disimpan di:{Fore.WHITE}")
    print(f"    - {sub_file}")
    print(f"    - {live_file}")
    print(f"    - {json_file}")

def main():
    parser = argparse.ArgumentParser(description='ReconX - Subfinder + Httpx-toolkit')
    parser.add_argument('-d', '--domain', required=True, help='Domain target')
    parser.add_argument('-o', '--output', help='File output subdomain')
    parser.add_argument('-l', '--live', help='File output live host')
    parser.add_argument('--passive', action='store_true', help='Passive mode (no DNS)')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Threads (default: 50)')
    parser.add_argument('--follow', action='store_true', help='Follow redirects')
    parser.add_argument('--export', action='store_true', help='Export ke file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    
    args = parser.parse_args()
    
    print_banner()
    check_tools()
    
    print(f"{Fore.YELLOW}[*] Versi Tools:{Fore.WHITE}")
    print(f"    Subfinder: {get_version('subfinder')}")
    print(f"    Httpx-toolkit: {get_version('httpx-toolkit')}")
    print(f"{Fore.YELLOW}[*] Target Domain: {args.domain}{Fore.WHITE}")
    print(f"{Fore.YELLOW}[*] Threads: {args.threads}{Fore.WHITE}")
    print("-" * 50)
    
    subdomains, elapsed_subfinder = run_subfinder(
        domain=args.domain,
        output_file=args.output,
        passive=args.passive,
        threads=args.threads
    )
    
    if not subdomains:
        print(f"{Fore.YELLOW}[!] Tidak ada subdomain ditemukan.{Fore.WHITE}")
        sys.exit(1)
    
    live_hosts, elapsed_httpx = run_httpx_toolkit(
        subdomains=subdomains,
        output_file=args.live,
        threads=args.threads,
        follow_redirects=args.follow
    )
    
    print_summary(args.domain, subdomains, live_hosts, elapsed_subfinder, elapsed_httpx)
    
    if args.export:
        export_results(args.domain, subdomains, live_hosts)
    
    print(f"\n{Fore.GREEN}[✓] Selesai!{Fore.WHITE}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Dihentikan oleh user{Fore.WHITE}")
        sys.exit(0)
