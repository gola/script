#!/usr/bin/python
'''
macOS free command
Created on Nov 12, 2018
@author: Ethan Gola
'''

import subprocess
import re
import sys

def macos_free():
    # Get process info
    ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0]
    vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0]

    # Iterate processes
    processLines = ps.split('\n')
    sep = re.compile('[\s]+')
    rssTotal = 0 # kB
    for row in range(1,len(processLines)):
        rowText = processLines[row].strip()
        rowElements = sep.split(rowText)
        try:
            rss = float(rowElements[0]) * 1024
        except:
            rss = 0 # ignore...
        rssTotal += rss

    # Process vm_stat
    vmLines = vm.split('\n')
    sep = re.compile(':[\s]+')
    vmStats = {}
    for row in range(1,len(vmLines)-2):
        rowText = vmLines[row].strip()
        rowElements = sep.split(rowText)
        vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

    # Get physical memory info
    # $ top -l 1 -s 0 | grep PhysMem
    physmem = subprocess.Popen("top -l 1 -s 0 | grep PhysMem", shell=True, stdout=subprocess.PIPE).communicate()[0]

    result = ""
    result = result + physmem + "\n"
    result = result + 'Wired Memory:\t\t%d MB' % ( vmStats["Pages wired down"]/1024/1024 ) + "\n"
    result = result + 'Active Memory:\t\t%d MB' % ( vmStats["Pages active"]/1024/1024 ) + "\n"
    result = result + 'Inactive Memory:\t%d MB' % ( vmStats["Pages inactive"]/1024/1024 ) + "\n"
    result = result + 'Free Memory:\t\t%d MB' % ( vmStats["Pages free"]/1024/1024 ) + "\n"
    result = result + 'Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 )

    return result

def main():
    rs = macos_free()
    print rs

if __name__=="__main__":
    main()
    sys.exit()
