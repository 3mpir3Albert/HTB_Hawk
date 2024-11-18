#!/bin/bash

function ctrl_c()
{
  echo -e "\n[!] Saliendo..."
  tput cnorm
  exit 1
}

trap ctrl_c SIGINT

function decrypt()
{

  $(openssl enc $1 -d -in drupal.enc -out mensaje.txt -k $2 2>/dev/null)
  if [[ $(file mensaje.txt | grep "ASCII") ]]; 
  then
    echo "[+] Descifrado exitoso con el algoritmo $1 y contraseña $2"
    tput cnorm
    exit 0
  fi

}

tput civis

#algorithm_cyphers=("-aes-128-cbc" "-aes-128-cfb" "-aes-128-cfb1" "-aes-128-cfb8" "-aes-128-ctr" "-aes-128-ecb" "-aes-128-ofb" "-aes-192-cbc" "-aes-192-cfb" "-aes-192-cfb1" "-aes-192-cfb8" "-aes-192-ctr" "-aes-192-ecb" "-aes-192-ofb" "-aes-256-cbc" "-aes-256-cfb" "-aes-256-cfb1" "-aes-256-cfb8" "-aes-256-ctr" "-aes-256-ecb" "-aes-256-ofb" "-aes128" "-aes128-wrap" "-aes128-wrap-pad" "-aes192" "-aes192-wrap" "-aes192-wrap-pad" "-aes256" "-aes256-wrap" "-aes256-wrap-pad" "-aria-128-cbc" "-aria-128-cfb" "-aria-128-cfb1" "-aria-128-cfb8" "-aria-128-ctr" "-aria-128-ecb" "-aria-128-ofb" "-aria-192-cbc" "-aria-192-cfb" "-aria-192-cfb1" "-aria-192-cfb8" "-aria-192-ctr" "-aria-192-ecb" "-aria-192-ofb" "-aria-256-cbc" "-aria-256-cfb" "-aria-256-cfb1" "-aria-256-cfb8" "-aria-256-ctr" "-aria-256-ecb" "-aria-256-ofb" "-aria128" "-aria192" "-aria256" "-bf" "-bf-cbc" "-bf-cfb" "-bf-ecb" "-bf-ofb" "-blowfish" "-camellia-128-cbc" "-camellia-128-cfb" "-camellia-128-cfb1" "-camellia-128-cfb8" "-camellia-128-ctr" "-camellia-128-ecb" "-camellia-128-ofb" "-camellia-192-cbc" "-camellia-192-cfb" "-camellia-192-cfb1" "-camellia-192-cfb8" "-camellia-192-ctr" "-camellia-192-ecb" "-camellia-192-ofb" "-camellia-256-cbc" "-camellia-256-cfb" "-camellia-256-cfb1" "-camellia-256-cfb8" "-camellia-256-ctr" "-camellia-256-ecb" "-camellia-256-ofb" "-camellia128" "-camellia192" "-camellia256" "-cast" "-cast-cbc" "-cast5-cbc" "-cast5-cfb" "-cast5-ecb" "-cast5-ofb" "-chacha20" "-des" "-des-cbc" "-des-cfb" "-des-cfb1" "-des-cfb8" "-des-ecb" "-des-ede" "-des-ede-cbc" "-des-ede-cfb" "-des-ede-ecb" "-des-ede-ofb" "-des-ede3" "-des-ede3-cbc" "-des-ede3-cfb" "-des-ede3-cfb1" "-des-ede3-cfb8" "-des-ede3-ecb" "-des-ede3-ofb" "-des-ofb" "-des3" "-des3-wrap" "-desx" "-desx-cbc" "-id-aes128-wrap" "-id-aes128-wrap-pad" "-id-aes192-wrap" "-id-aes192-wrap-pad" "-id-aes256-wrap" "-id-aes256-wrap-pad" "-id-smime-alg-CMS3DESwrap" "-rc2" "-rc2-128" "-rc2-40" "-rc2-40-cbc" "-rc2-64" "-rc2-64-cbc" "-rc2-cbc" "-rc2-cfb" "-rc2-ecb" "-rc2-ofb" "-rc4" "-rc4-40" "-seed" "-seed-cbc" "-seed-cfb" "-seed-ecb" "-seed-ofb" "-sm4" "-sm4-cbc" "-sm4-cfb" "-sm4-ctr" "-sm4-ecb" "-sm4-ofb")

algorithm_cyphers=("-aes-256-cbc" "-aes-256-ofb")

for algorithm in ${algorithm_cyphers[@]};
do
  echo -e "\n [i] Probando con el algoritmo $algorithm"

  for pass in $(cat /usr/share/wordlists/rockyou.txt);
  do

    decrypt "$algorithm" "$pass"
  
  done
done

tput cnorm
