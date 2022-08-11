#!/bin/bash -e

cd "$(dirname "$0")"

if [[ $# != 3 ]]; then
    echo "Usage: init.sh <cloud_ip> <domain> <number_of_teams>"
    exit 1
fi

IP="$1"
DOMAIN="$2"
NUMBER_OF_TEAMS="$3"

if [[ ! $IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Bad vpn_ip"
  exit 1
fi

if [[ ! $DOMAIN =~ ^[0-9a-z.-]+$ ]]; then
  echo "Bad domain"
  exit 1
fi

if ! which openvpn > /dev/null; then
  echo "It seems you don't have OpenVPN installed, please install it, it is needed for config generation"
  echo "Try 'apt install openvpn' or similar command"
  exit 1
fi

if ! which rsync > /dev/null; then
  echo "It seems you don't have rsync installed, please install it, it is needed for copying files"
  echo "Try 'apt install rsync' or similar command"
  exit 1
fi

if ! which ansible-playbook > /dev/null; then
  echo "It seems you don't have ansible installed, please install it, it is needed for deploying"
  echo "Try 'apt install ansible' or similar command"
  exit 1
fi

if [ ! -d ../vpn/gen/client_prod ]; then
  echo "It seems you don't generated ../vpn/gen/client_prod yet, please, generate it with ../vpn/init_vpn.sh script"
  exit 1
fi

echo "Patching inventory.cfg"
sed -E -i "s/cld-master\.a ansible_host=\S+/vpn.a ansible_host=$IP/" ../../inventory.cfg

echo "Patching files/api_srv/cloud_common.py"
sed -E -i "s/DOMAIN = \"[0-9a-z.-]+\"/DOMAIN = \"${DOMAIN}\"/" files/api_srv/cloud_common.py

echo "Patching gen/gen_conf_client_entergame_prod.py"
sed -E -i "s/SERVER = \"team%d.[0-9a-z.-]+\"/SERVER = \"team%d.${DOMAIN}\"/" gen/gen_conf_client_entergame_prod.py

echo "Patching files/nginx/cloud"
sed -E -i "s/server_name [0-9a-z.-]+;/server_name ${DOMAIN};/" files/nginx/cloud
sed -E -i "s/https:\/\/[0-9a-z.-]+\\\$request_uri/https:\/\/${DOMAIN}\$request_uri/" files/nginx/cloud

echo "Patching files/wsgi/cloudapi.wsgi"
sed -E -i "s/DOMAIN = \"[0-9a-z.-]+\"/DOMAIN = \"${DOMAIN}\"/" files/wsgi/cloudapi.wsgi

echo "Patching files/apache/000-default.conf"
sed -E -i "s/ServerName\s+[0-9a-z.-]+/ServerName ${DOMAIN}/" files/apache2/000-default.conf

echo "Patching number of teams"
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/gen_conf_client_entergame_prod.py
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/gen_conf_server_outside_prod.py
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/gen_rootpasswds_prod.py
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/gen_team_tokens_prod.py
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/init_teams_prod.py
sed -E -i "s/for i in \{1\.\.[0-9]+\}/for i in \{1\.\.${NUMBER_OF_TEAMS}\}/" gen/create_team_net_certs_prod.sh

echo "Copying ../vpn/gen/client_prod to gen/openvpn_team_main_net_client_prod"
rsync -a ../vpn/gen/client_prod/ gen/openvpn_team_main_net_client_prod


echo "Generating Cloud configs"
gen/gen_all_configs.sh

echo "Copying init state from gen/db_prod/ to files/api_srv/db_init_state_prod"
rsync -a gen/db_prod/ files/api_srv/db_init_state_prod

#echo "Everyting is ready for 'ansible-playbook vpn.yaml'"