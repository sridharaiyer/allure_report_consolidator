import winrm

# s = winrm.Session('172.20.0.29', auth=('pceqa', 'pceqa1'), transport='kerberos')
s = winrm.Session('172.20.0.29', auth=('pceqa', 'pceqa1'))
r = s.run_cmd('ipconfig', ['/all'])
print(r.status_code)
