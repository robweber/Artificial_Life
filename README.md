## Artificial Life

This is a modification to the Artificial Life project as described on the [314reactor.com](https://314reactor.com/2017/10/16/artificial-life-project/) blog. The goal of the project is to use a Raspberry Pi and a [Unicorn Pi Hat](https://shop.pimoroni.com/products/unicorn-hat) to simulate a set of artificial lifeforms. The main difference from this branch and the main branch is that this project will run the code via the [WebIOPi](http://webiopi.trouch.com/) framework. This gives a web interface to the program and allows running and changing the parameters in a more user friendly nature. Plus the entire device can be accessed via a browser so direct console access to the Pi is not necessary. Other programming changes are listed below. 


### Installation

These instructions assume you have a Raspberry Pi with Raspbian installed all ready to go. 

1. Install WebIOPi

```

#clone webiopi - this version supports 1,2,3 and Zero
git clone https://github.com/thortex/rpi3-webiopi.git
cd rpi3-webiopi

#install deps
cd dev
./01_setup-required-packages.sh

./03_install_python_dev.sh

./10_make_deb.sh

#install the dpkg files
sudo dpkg -i ~/build.webiopi/python2-webiopi*.deb
sudo dpkg -i ~/build.webiopi/python3-webiopi*.deb

#use python 2
sudo webiopi-select-python 2

#restart the services
sudo systemctl daemon-reload
sudo systemctl restart webiopi

```

2. Install Artificial Life 

```

#clone repo
https://github.com/robweber/Artificial_Life.git
cd Artificial_Life
git checkout webiopi

#install dependencies
sudo pip install -r requirements.txt

#copy config file
sudo cp webiopi.config /etc/webiopi/config

#generate a new password for web interface
sudo webiopi-passwd

#restart the services
sudo systemctl restart webiopi

```

3. WebIOPi should now be running on http://IP:8000


### Running the Program

Log in to the web interface on port 8000 using the username and password created in the installation step. 

The main page allows you to start the program and run Artificial Life. The running status will query every so often and change if the program finishes. 

The settings page allows you to tweak the run time settings. These are saved in a file and will persist between reboots. 

### Changes From Original

I made some tweaks to the original version of the program to suit myself. They are listed below: 

__Red/Blue Colors Tied to Aggression/Lifespan__

In the original program the colors were not any specific indicator of the traits of the life form. While this may be true in life (ie, eye color not an indicator of lifespan) I wanted more of a visual indicator of what was happening on the board. To this end I tied the red color to the aggression of a life form and the blue color to the life span. 

To calculate these values the actual aggression and life span values are created as normal. It's important to note that these values are either inherited from the parents or are random when being created. This keeps things interesting in terms of offspring. Once the values are known the lifeform's value is calculated as a percentage of the global values. This percentage is used to calculate how red or blue a life form is. In general terms, more aggressive life forms are redder and long living life forms are bluer.  
