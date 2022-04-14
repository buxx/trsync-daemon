[server]
trsync_bin_path = "/usr/local/bin/trsync"
listen_timeout = 60
instances = algoo,bux
local_folder = ~/Tracim

[instance.algoo]
address = algoo.tracim.fr
username = bux
unsecure = false
workspaces_ids = 42,43

[instance.bux]
address = tracim.bux.fr
username = bux
unsecure = false
workspaces_ids = 24,23