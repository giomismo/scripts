#Shortcuts
alias exportea='echo export PATH=\$PATH:$(pwd) >> ~/.bashrc'
alias ll='ls -lah'
alias cd..='cd ../../'
alias cd...='cd ../../../'
alias cd....='cd ../../../../'
alias cd.....='cd ../../../../../'

#Android analisis
apk() {
    java -jar /Users/giomismo/Security/android/tools/apktool1.5.2/apktool.jar d $(pwd)/$1 $(pwd)/unapk
}
alias azip='unzip -d zip'

#Beautify json and store file if a "1" is passed as second arg
beautifier () {
    python -c "import json; fd = file('"$1"','r'); fc = fd.read(); fd.close(); fw = open('"${1}.beautified"', 'w'); fw.write(json.dumps(json.loads(fc), sort_keys=True, indent=4)); fw.close()"
    less ${1}.beautified
    if [ $# -eq 2 ]
    then
        if [ ! ${2} -eq 1 ]
        then
            rm ${1}.beautified
        fi
    else
        rm ${1}.beautified
    fi
}

