all:
	test -d output || mkdir output
	rst2html index.rst > output/index.html

clean:
	rm -rf output

publish:
	rsync -aP --delete output/ people.mozilla.org:public_html/relengdocs/
