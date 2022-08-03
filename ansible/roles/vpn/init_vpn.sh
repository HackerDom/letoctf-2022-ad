#!/bin/bash -e

cd "$(dirname "$0")"

if [[ $# != 3 ]]; then
    echo "Usage: init.sh <vpn_ip> <domain> <number_of_teams>"
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

if [[ ! $NUMBER_OF_TEAMS =~ ^[0-9]+$ ]]; then
  echo "Bad number_of_teams"
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

echo "Patching inventory.cfg"
sed -E -i "s/vpn\.a ansible_host=\S+/vpn.a ansible_host=$IP/" ../../inventory.cfg

echo "Patching gen/gen_conf_client_prod.py"
sed -E -i "s/SERVER = \"[0-9a-z.-]+\"/SERVER = \"game.${DOMAIN}\"/" gen/gen_conf_client_prod.py

echo "Patching number of teams"
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/gen_conf_server_prod.py
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/gen_conf_client_prod.py
sed -E -i "s/N = [0-9]+/N = ${NUMBER_OF_TEAMS}/" gen/gen_keys_prod.py
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/networkclosed/open_network.sh
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/networkclosed/check_network.sh
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/networkclosed/check_network.sh
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/networkclosed/close_network.sh
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/snat/check_snat_rules.sh 
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/snat/del_snat_rules.sh 
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/snat/add_snat_rules.sh
sed -E -i "s/for num in \{0\.\.[0-9]+\}/for num in \{0\.\.${NUMBER_OF_TEAMS}\}/" files/snat/add_snat_rules.sh

echo "Generating VPN configs"
gen/gen_all_keys.sh

echo "Copying server VPN configs from gen/server_prod/ to vpn/files/openvpn_prod"
rsync -a gen/server_prod/ vpn/files/openvpn_prod/

echo "Done"