#!/usr/bin/python
IP_REGEX = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

import argparse
import re

_ip_re = re.compile(IP_REGEX)

def increase_ip(ip):
  blocks = [int(i) for i in ip.split('.')]
  for i in reversed(range(len(blocks))):
    if blocks[i] < 0xFF:
      blocks[i] += 1
      break
    else:
      blocks[i] = 0x0
  
  return '.'.join(map(str, blocks))
  

def generate_range(ip_start, ip_end):
  ip = ip_start
  while True:
    ip = increase_ip(ip)
    yield ip
    if ip == ip_end:
      break

def t_ip(s):
  if _ip_re.search(s):
    return s
  else:
    msg = '{} is not an IP'.format(s)
    raise argparse.ArgumentTypeError(msg)

def main():
  pars = argparse.ArgumentParser()
  pars.add_argument('ip_start', type=t_ip)
  pars.add_argument('ip_end', type=t_ip)

  args = pars.parse_args()

  for i in generate_range(args.ip_start, args.ip_end): print(i)

if __name__ == '__main__':
  main()

  
