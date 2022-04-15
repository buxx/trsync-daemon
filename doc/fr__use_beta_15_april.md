## Linux

1. Télécharger trsync : https://tracim.bux.fr/ui/guest-download/235932d2-6e9f-4786-b736-c09fdb8ffdf1
2. Télécharger trsync-manager : https://tracim.bux.fr/ui/guest-download/26aa1eec-6077-424a-9e8f-2ddc827a8268
3. Décompresser les deux binaires à un emplacement, par exemple `/home/votre_nom_dutilisateur/.bin/`
4. Créer un fichier à l'emplacement `/home/votre_nom_dutilisateur/.trsync.conf` contenant par exemple :
```
[server]
trsync_bin_path = "/home/votre_nom_dutilisateur/.bin/trsync"
listen_timeout = 60
instances = algoo
local_folder = /home/votre_nom_dutilisateur/Tracim

[instance.algoo]
address = algoo.tracim.fr
username = votre_nom_dutilisateur_tracim
password = LeMotDePAsse
unsecure = false
workspaces_ids = 29,3
```
5. Remplacer les valeurs par les vôtres
6. Pour démarrer la synchronisation, dans un terminal, éxécuter `~/.bin/trsync-manager`
