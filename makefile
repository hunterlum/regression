start_server:
	screen -d -m ./bin/cryptoServer.py

reports: pdf html

#https://stackoverflow.com/questions/34818723/export-notebook-to-pdf-without-code
pdf:
	 jupyter nbconvert --to pdf --template template/hidecode Main.ipynb --output Report.pdf

html:
	 jupyter nbconvert --to html Main.ipynb --output Report.html

clean:
	rm Report.*
