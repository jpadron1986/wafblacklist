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
file = open("./app/file/fireholLevel1", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/fireholLevel1"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# torlist
url = "https://www.dan.me.uk/torlist/"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/torlist", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/torlist"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Honeypot
url = "https://www.projecthoneypot.org/list_of_ips.php?t=d&rss=1"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/honeypot", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/honeypot"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Danger rulez
url = "http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/blist", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/blist"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Spamhaus
url = "https://www.spamhaus.org/drop/drop.lasso"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/drop", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/drop"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Cinsscore
url = "https://cinsscore.com/list/ci-badguys.txt"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/ci-badguys", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/ci-badguys"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Blacklist.de
url = "https://lists.blocklist.de/lists/all.txt"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/all", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/all"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Greensnow
url = "https://blocklist.greensnow.co/greensnow.txt"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/greensnow", "w") 
file.write(str(contenido))
file.close()
filename = "./app/file/greensnow"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Talos
url = "https://www.talosintelligence.com/documents/ip-blacklist"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/talos", "w")
file.write(str(contenido))
file.close()
filename = "./app/file/talos"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Myip.ms
url = "https://myip.ms/files/blacklist/general/latest_blacklist.txt"
respuesta = urllib.request.urlopen(url)
contenido = respuesta.read()
file = open("./app/file/myip", "w")
file.write(str(contenido))
file.close()
filename = "./app/file/myip"
for line in (l.strip() for l in open(filename) if not l.startswith('#') and l.strip()):
     r.sadd('ips', line)

# Esportar lista de ips desde Redis al archivo de testo plano que se publicara en la web
ips = r.smembers('ips')
with open('./app/blacklist.html', 'w') as filehandle:
    filehandle.writelines("%s\n" % ip.decode() for ip in ips)