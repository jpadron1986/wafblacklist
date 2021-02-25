from urllib.request import urlopen
import redis
import urllib.request
# apertura de redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
#
## Conexion y descarga en variable de listas ip + copia en BD de Redis.
#
# Firehol
url = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("fireholLevel1", "w") 
file.write(str(contenido))
file.close()
filename = "fireholLevel1"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Honeypot
url0 = "https://www.projecthoneypot.org/list_of_ips.php?t=d&rss=1"
respuesta0 = urllib.request.urlopen(url0)
contenido0 = respuesta0.read()
file0 = open("honeypot", "w") 
file0.write(str(contenido0))
file0.close()
filename0 = "honeypot"
for line0 in (l.strip() for l in open(filename0) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line0)

# Danger rulez
url1 = "http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
respuesta1 = urllib.request.urlopen(url1)
contenido1 = respuesta1.read()
file1 = open("blist", "w") 
file1.write(str(contenido1))
file1.close()
filename1 = "blist"
for line1 in (l.strip() for l in open(filename1) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line1)

# Spamhaus
url2 = "https://www.spamhaus.org/drop/drop.lasso"
respuesta2 = urllib.request.urlopen(url2)
contenido2 = respuesta2.read()
file2 = open("drop", "w") 
file2.write(str(contenido1))
file2.close()
filename2 = "drop"
for line2 in (l.strip() for l in open(filename2) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line2)

# Cinsscore
url3 = "https://cinsscore.com/list/ci-badguys.txt"
respuesta3 = urllib.request.urlopen(url3)
contenido3 = respuesta3.read()
file3 = open("ci-badguys", "w") 
file3.write(str(contenido3))
file3.close()
filename3 = "ci-badguys"
for line3 in (l.strip() for l in open(filename3) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line3)

# Blacklist.de
url4 = "https://lists.blocklist.de/lists/all.txt"
respuesta4 = urllib.request.urlopen(url4)
contenido4 = respuesta4.read()
file4 = open("all", "w") 
file4.write(str(contenido4))
file4.close()
filename4 = "all"
for line4 in (l.strip() for l in open(filename4) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line4)

# Greensnow
url5 = "https://blocklist.greensnow.co/greensnow.txt"
respuesta5 = urllib.request.urlopen(url5)
contenido5 = respuesta5.read()
file5 = open("greensnow", "w") 
file5.write(str(contenido5))
file5.close()
filename5 = "greensnow"
for line5 in (l.strip() for l in open(filename5) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line5)

# Talos
url6 = "https://www.talosintelligence.com/documents/ip-blacklist"
respuesta6 = urllib.request.urlopen(url6)
contenido6 = respuesta6.read()
file6 = open("talos", "w")
file6.write(str(contenido5))
file6.close()
filename6 = "talos"
for line6 in (l.strip() for l in open(filename6) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line6)

# Myip.ms
url7 = "https://myip.ms/files/blacklist/general/latest_blacklist.txt"
respuesta7 = urllib.request.urlopen(url7)
contenido7 = respuesta7.read()
file7 = open("myip", "w")
file7.write(str(contenido7))
file7.close()
filename7 = "myip"
for line7 in (l.strip() for l in open(filename7) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line7)

# Esportar lista de ips desde Redis al archivo de testo plano que se publicara en la web
ips = r.smembers('ips')
with open('blacklist.html', 'w') as filehandle:
    filehandle.writelines("%s\n" % ip.decode() for ip in ips)