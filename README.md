Tunnel_http
===========

TP ARX Tunnel HTTP


Installer proxypy (pour tester avec un proxy):
=========
1. Récupérer le code
svn checkout http://proxpy.googlecode.com/svn/trunk/
2. Corriger un peu de code
Dans la fonction getPath de http.py, il faut remplacer "return s" (ligne 251) par "return self.url"
3. Lancer le proxy
Dans le dossier lancer:
sudo python proxpy.py -p 3128
