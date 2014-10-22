#!/bin/bash
# Amon Agent install script.
set -e
logfile="amonagent-install.log"

# Set up a named pipe for logging
npipe=/tmp/$$.tmp
mknod $npipe p

# Log all output to a log for error checking
tee <$npipe $logfile &
exec 1>&-
exec 1>$npipe 2>&1
trap "rm -f $npipe" EXIT

function file_exists() {
    [ -f "$1" ]
}

# Basic distro detection
DISTRO=
if file_exists /etc/debian_version ; then
    DISTRO='debian'
elif file_exists /etc/system-release; then
    DISTRO='rpm'
fi

# Proper distro detection - for Ansible
DISTRO_ID=$(
python - <<EOF
import platform ; print platform.dist()[0].lower()
EOF
)

DISTRO_VERSION=$(
python - <<EOF
import platform ; print int(float(platform.dist()[1]))
EOF
)

function on_error() {
    printf "\033[31m
It looks like you hit an issue when trying to install the Agent.

Troubleshooting and basic usage information for the Agent are available at:

   https://amon.cx/docs#monitoring

If you're still having problems, please send an email to martin@amon.cx
with the contents of amonagent-install.log and we'll do our very best to help you
solve your problem.\n\033[0m\n"
}
trap on_error ERR

if [ -n "$SERVER_KEY" ]; then
    serverkey=$SERVER_KEY
fi

if [ ! $serverkey ]; then
    printf "\033[31mServer key not available in SERVER_KEY environment variable.\033[0m\n"
    exit 1;
fi


# Root user detection
if [ $(echo "$UID") = "0" ]; then
    sudo_cmd=''
else
    sudo_cmd='sudo'
fi



function install_amon() {
   
    # Install the necessary package sources
    if [ $DISTRO == 'rpm' ]; then
        echo -e "\033[34m\n* Installing YUM sources for Amon\n\033[0m"
        $sudo_cmd sh -c "echo -e '[amon]\nname = Amon.\nbaseurl = http://packages.amon.cx/rpm/\nenabled=1\ngpgcheck=0\npriority=1' > /etc/yum.repos.d/amon.repo"

        printf "\033[34m* Installing the Amon Agent package\n\033[0m\n"

        $sudo_cmd yum -y install amon-agent
      
    elif [ $DISTRO == 'debian' ]; then
        printf "\033[34m\n* Installing APT package sources for Amon\n\033[0m\n"
        $sudo_cmd sh -c "echo 'deb http://packages.amon.cx/repo amon contrib' > /etc/apt/sources.list.d/amonagent.list"
        $sudo_cmd apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv AD53961F

        printf "\033[34m\n* Installing the Amon Agent package\n\033[0m\n"
       
        $sudo_cmd apt-get update
        $sudo_cmd apt-get install -y --force-yes amon-agent

    else
        printf "\033[31mYour OS or distribution are not supported by this install script.
            Please follow the instructions on the Agent setup page:

        https://amon.cx/docs#monitoring\033[0m\n"
        exit;
    fi

    printf "\033[34m\n* Adding your API key to the Agent configuration: /etc/amon-agent.conf\n\033[0m\n"


    $sudo_cmd sh -c "echo  '{\"server_key\": \"$serverkey\"}' > /etc/amon-agent.conf"


    printf "\033[34m* Starting the Agent...\n\033[0m\n"
    $sudo_cmd /etc/init.d/amon-agent restart


}

function install_ansible(){
    
    printf "\033[34m\n* Installing Ansible ...\n\033[0m\n"
    # Ansible is separated in several repositories, detect the Distro

    if [ $DISTRO == 'debian' ]; then

        if [ $DISTRO_ID == 'ubuntu' ]; then
            $sudo_cmd apt-get install -y --force-yes python-software-properties software-properties-common
            $sudo_cmd apt-add-repository -y ppa:ansible/ansible
            $sudo_cmd apt-get update
            $sudo_cmd apt-get install ansible
        elif [ $DISTRO_ID == 'debian' ]; then

            if [ $DISTRO_VERSION == 7 ]; then
                $sudo_cmd sh -c "echo 'deb http://http.debian.net/debian wheezy-backports main' > /etc/apt/sources.list.d/backports.list"
                $sudo_cmd apt-get update
                $sudo_cmd apt-get -t wheezy-backports install "ansible"
            else
                $sudo_cmd sh -c "echo 'deb http://http.debian.net/debian-backports squeeze-backports(-sloppy) main' > /etc/apt/sources.list.d/backports.list"
                $sudo_cmd apt-get update
                $sudo_cmd apt-get -t squeeze-backports install "ansible"
            fi 
        fi

    elif [ $DISTRO == 'rpm' ]; then
        $sudo_cmd yum install epel-release
        $sudo_cmd yum -y install ansible
    fi
}

# Show a message about where to go for help.
function print_troubleshooting_instructions() {


printf "\033[32m All done. You can see your data at https://amon.cx/servers
   ----------------------------------
    
    For troubleshooting instructions, please see the Documentation:

        https://amon.cx/docs#monitoring

    If you ever want to stop the Agent, run:
        
        sudo /etc/init.d/amon-agent stop

    And to run it again run:

        sudo /etc/init.d/amon-agent start

\033[0m"


}


install_amon
install_ansible
print_troubleshooting_instructions
