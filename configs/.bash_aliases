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
