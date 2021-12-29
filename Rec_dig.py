#!/usr/bin/env python3

import subprocess
import shlex
import datetime
import re #how to filter multiple resolutions from dig

#default values
dnsintsrv = "10.30.23.5"
dnsextsrv = "8.8.8.8"
dnserv= str(dnsintsrv)
internal = 1
menu = 1
printfile = "N"

print("Program created by AC for bulk resolution")
print("files needed: list_of_dns.txt ; list_of_ip.txt ; list_of_srv.txt inside default file location: c:/Tmp/")

#program start
while menu != 8:
    __image__ = ''' \033[80m

            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            +                        o o                                            +
            +                     \_`-)|_                                           +
            +                  ,""       \            Recursive dig                 +
            +                ,"  ## |  o\ /o.                                       +
            +              ," ##   ,-\__    `.         By AC  v2.1                  +
            +            ,"       /     `--._;)                                     +
            +          ,"     ## /                                                  +
            +        ,"   ##    /                                                   +
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    \033[80m
    '''
    print(__image__)
    print("1) DNS query (list_of_dns->IP)")
    print("   10) DNS query COMPLETE trace(list_of_dns->IP)")
    print("   11) DNS query internal + external (list_of_dns->IP)")
    print("2) Reverse DNS Resolution (list_of_ip->Host)")
    print("3) Check DNS resolution on multiple Servers (list_of_srv)")
    print("   30) Anycast DNS resolution on multiple Servers (list_of_srv)")
    print("4) Change to internal DNS server (actual (AMR Users Anycast): " + str(dnsintsrv) +" )")
    print("5) Change to external DNS server (actual (google public DNS): " + str(dnsextsrv) + " )")
    print("6) Change DNS server (actual: " + str(dnserv) +" )")
    print("7) Output to file (actual: " + str(printfile) + " )")
    print("8) Close program")
    print(" ")
    menu = input("Enter an option: \n")

    if menu == '1' or '10' or '11' or '2' or '3':
        if printfile == "Y":
            a = str(datetime.datetime.now()).split(".")[0]
            b = a.replace(":", "_").replace(" ", "_")
            #fout = open("C:\\tmp\\rec_dig_output_" + b + ".csv", "at")
            fo = open("C:\\tmp\\rec_dig_output_" + b + ".csv", 'w')

    if menu == '1':
        print("Recursive dig (list_of_dns->IP)")
        filepath = 'c:/tmp/list_of_dns.txt'
        with open(filepath) as fp:
           line = fp.readline()
           cnt = 1
           while line:
               cmd = 'dig @' + str(dnserv) +' ' + str(line) + ' +short'
               proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
               out, err = proc.communicate()
               #print(out)
               output = str(out).split("\n")
               #print(output)
               reply=str(output).lstrip("['").rstrip("']").replace("b'","").replace('\\r','').replace('\\n','').replace('\\','').replace('"','').replace("'","").replace('.com.','.com -> ')
               #test=reply.split("connection timed out")[1]
               if (reply=="" or reply.split("connection timed out")[1]==True):
                   print(str(line).split("\n")[0].lstrip("'").rstrip("'") + " -> No DNS Record")
               else:
                   print(str(line).split("\n")[0].lstrip("'").rstrip("'") + " -> " + reply )
               line = fp.readline()
               cnt += 1

    if menu == '10':
        print("Recursive dig COMPLETE(list_of_dns->IP)")
        filepath = 'c:/tmp/list_of_dns.txt'
        with open(filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                cmd = 'dig @' + str(dnserv) +' ' + str(line).strip()
                proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
                out, err = proc.communicate()
                #print(out)
                #output = str(out).split("\n")
                try:
                    output=str(out).split("ANSWER SECTION:")[1].split("Query")[0].replace("\\r","").split("\\t")
                except:
                    print(line.strip() + " -> No Record" )
                else:
                    tmp=len(output)
                    #print(tmp)
                    #print(output)
                    if (tmp==5):
                        print((output[0].replace("\\n","") + " -> (" + output[3] + ") -> " + output[4].replace("\\n","").replace(";","")))
                    if (tmp==6):
                        print(output[0].replace("\\n","") + " -> (" + output[4] + ") -> " + output[5].replace("\\n","").replace(";",""))
                    if (tmp==10):
                        #print(output)
                        tmp2=int(tmp/5)
                        #print(tmp2)
                        #toprint=toprint+output[i*0].split("\\n")[1] + " -> (" + output[i*3] + ") -> " + output[i*4].split("\\n")[0]
                        print(output[0].split("\\n")[1] + " -> (" + output[3] + ") -> " + output[4].split("\\n")[0] + " -> (" + output[8] + ") -> " +  output[9].replace("\\n","").replace(";",""))
                    if (tmp!=5 and tmp!=6 and tmp!=10):
                        print(output)
                line = fp.readline()
                cnt += 1

    if menu == '11':
        print("11) DNS query internal + external (list_of_dns->IP)")
        filepath = 'c:/tmp/list_of_dns.txt'
        with open(filepath) as fp:
           line = fp.readline()
           cnt = 1
           while line:
               cmd1 = 'dig @' + str(dnsintsrv) +' ' + str(line) + ' +short'
               cmd2 = 'dig @' + str(dnsextsrv) + ' ' + str(line) + ' +short'
               proc1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
               proc2 = subprocess.Popen(shlex.split(cmd2), stdout=subprocess.PIPE)
               out1, err = proc1.communicate()
               out2, err = proc2.communicate()
               output1 = str(out1).split("\n")
               output2 = str(out2).split("\n")
               print("Internal) " + str(line).split("\n")[0].lstrip("'").rstrip("'") + " -> " + str(output1).lstrip("['").rstrip("']").replace("b'","").replace('\\r','').replace('\\n','').replace('\\','').replace('"','').replace("'","").replace('.com.','.com -> '))
               print("External) " + str(line).split("\n")[0].lstrip("'").rstrip("'") + " -> " + str(output2).lstrip("['").rstrip("']").replace("b'","").replace('\\r','').replace('\\n','').replace('\\','').replace('"','').replace("'","").replace('.com.','.com -> '))
               line = fp.readline()
               cnt += 1

    if menu == '2':
        print("2) Reverse DNS Resolution (list_of_ip->Host)")
        filepath = 'c:/tmp/list_of_ip.txt'
        with open(filepath) as fp:
           line = fp.readline()
           cnt = 1
           while line:
               #cmd = 'dig -x @' + str(dnserv) + ' ' + str(line) + ' +short'
               cmd = 'dig -x ' + str(line) + ' +short'
               proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
               out, err = proc.communicate()
               output = str(out).split("\n")
               if ("b''" in str(output).lstrip("['").rstrip("']")):
                    output="none"
               else:
                   output=str(output).lstrip("['").rstrip("']").replace("b'","").replace("\\\\r\\\\n'","").replace('"','')
               print(str(line).split("\n")[0].lstrip("'").rstrip("'") + " -> " + output)
               with open("C:\\tmp\\output2.txt","a") as f:  # using "a" instead of a for adding lines and not replacing each export
                   f.writelines(str(line).split("\n")[0].lstrip("'").rstrip("'") + " -> " + str(output).lstrip("['").rstrip("']"))
               line = fp.readline()
               cnt += 1

    if menu == '3':
        print("3) Check DNS resolution on multiple Servers (list_of_srv)") #if want to test with Entire Grid use list_of_ipam
        filepath = 'c:/tmp/list_of_srv.txt'
        with open(filepath) as fp:
           line = fp.readline()
           cnt = 1
           while line:
               test = 'accenture.com'
               cmd = 'dig @' + str(line) + ' ' + test + ' +short'
               proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
               out, err = proc.communicate()
               output = str(out).split("\n")
               string = str(output).lstrip("['").rstrip("']")[3:-8]
               try:
                   string2 = string.split("<<>>")[1]
               except:
                   print(str(line).split("\n")[0] + " : " + test + " -> " + string)

               else:
                    print(str(line).split("\n")[0] + " : Server not responding DNS queries")

               #print(err)
               #fo.write(str(line).split("\n")[0] + " : " + test + " -> " + str(output).lstrip("['").rstrip("']")[3:-8] + "\n")
               line = fp.readline()
               cnt += 1
        fp.close()
        if printfile == "Y":
            fo.close()
        input("Press Enter to continue...")

    if menu == '30':
        print("30) Anycast DNS resolution on multiple Servers (list_of_srv)") #if want to test with Entire Grid use list_of_ipam
        filepath = 'c:/tmp/list_of_srv.txt'
        with open(filepath,'r') as fp:
            #line = fp.readline()
            cnt = 1
            #while line:
            for line in fp:
                line=line.strip()
                test = '.accenture.com'
                #cmd = 'dig @' + str(line) + test + ' hostname.bind txt chaos +short'
                cmd = 'dig @' + str(line) + ' hostname.bind txt chaos +short'
                proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
                out, err = proc.communicate()
                #print(out)
                output = str(out).split("\n")
                string = str(output).split('"')[1]
                try:
                    string2 = string.split("<<>>")[1]
                except:
                    print(str(line) + " : " + "Anycast resolving to -> " + string)

                else:
                    print(str(line) + " : Server not responding Anycast DNS queries")

                #print(err)
                #fo.write(str(line).split("\n")[0] + " : " + test + " -> " + str(output).lstrip("['").rstrip("']")[3:-8] + "\n")
                #line = fp.readline()
                #cnt += 1
        fp.close()
        if printfile == "Y":
            fo.close()
        input("Press Enter to continue...")

    if menu == '4':
        print("4) Change to internal DNS server (actual (AMR Users Anycast): " + str(dnsintsrv) + " )")

        dnserv = dnsintsrv

    if menu== '5':
        print("5) Change to external DNS server (actual (google public DNS): " + str(dnsextsrv) + " )")
        dnserv = dnsextsrv

    if menu== '6':
        print("6) Change DNS server (actual: " + str(dnserv) + " )")
        dnserv = str(input("Enter a different DNS Server: \n"))

    if menu== '7':
        print("6) Output mode has changed")
        if printfile == "N":
            printfile = "Y"
        else: printfile = "N"


#for i in `cat c:/tmp/list_of_dns` #TO TEST DNS SERVERS


# rac-secure.gslb.norwichunion.com.



#return (0)