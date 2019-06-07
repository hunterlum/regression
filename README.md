# Regression

## Data Collection Server
This repo contains a server that can be used to download cryptocurrency prices. Use the <code>make start_server</code> command to start a screen session and run the <b>cryptoServer.py</b> script located in <b>bin/</b> . To install screen on Ubuntu use <code>sudo apt install screen</code> . <code>screen -ls</code> can be used to interact with the screen session once it has be instatiated. All files are stored in the <b>raw_data/</b> directory.<br>

A dshboard has been made to view the data in <b>cryptoData.csv</b>. <br> https://datastudio.google.com/open/1ztty4l8Kx1YMtSQIZ4zgcwSlq4jJc3cP
<!--
https://datastudio.google.com/open/1ztty4l8Kx1YMtSQIZ4zgcwSlq4jJc3cP
-->

## Files
bin: contains all the programs/scripts used here <br>
makefile: used to run the data server and generate the pdf report from Main.ipynb
