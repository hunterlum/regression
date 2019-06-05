# Regression

## Data Collection Server
This repo contains a server that can be used to download cryptocurrency prices. Use the <code>make start_server</code> command to start a screen session and run the <b>cryptoServer.py</b> script located in <b>bin/</b> . Use <code>sudo apt install screen</code> to install screen in Ubuntu. <code>screen -ls</code> can be used to interact with the screen session once it has be instatiated. All files are stored in the datapool/ directory.

## Files
bin: contains all the programs/scripts used here <br>
makefile: used to run the data server and generate the pdf report from Main.ipynb
