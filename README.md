# Regression

## Data Collection Server
This repo contains a server that can be used to download cryptocurrency prices. Use the <code>make start_server</code> command to start a screen session and run the <b>cryptoServer.py</b> script located in <b>bin/</b> . To install screen on Ubuntu use <code>sudo apt install screen</code> . <code>screen -ls</code> can be used to interact with the screen session once it has be instatiated. All files are stored in the <b>raw_data/</b> directory.<br>

A dshboard has been made to view the data in <b>cryptoData.csv</b>. <br> https://datastudio.google.com/open/1ztty4l8Kx1YMtSQIZ4zgcwSlq4jJc3cP
<!--
https://datastudio.google.com/open/1ztty4l8Kx1YMtSQIZ4zgcwSlq4jJc3cP
-->

## Files
<b>bin/</b>: contains all the programs/scripts used in this repository <br>

<b>data/</b> and <b>raw_data/</b>: The web server stores all the information in <b>raw_data/</b> which gets trasffered into <b>data/</b> after being processed. <br>

<b>template/</b> A template is used to suppress code in the pdf report. <br>

<b>Main.ipynb</b> Most of the work for this project will be contained in this jupyter notebook. It is used to generate the html and pdf report through make. <br>

<b>makefile</b>: used to run the data server and generate the pdf report from Main.ipynb. Running <code>make pdf</code> can be used to create the pdf from <b>Main.ipynb</b> and <code>make clean</code> can be used to delete the reports. 
