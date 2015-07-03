all:
	python3 builder/ pages/
	cd site/ && jekyll b

watch:
	bash -c "fswatch pages/ | xargs -t -n1 python3 builder/ pages/ & PIDPY=$$! ; cd site/ && jekyll s & PIDJEK=$$! ; wait $$PIDPY ; wait $$PIDJEK " 

clean:
	rm -fr builder/__pycache__ site/_site site/_topics site/_posts

pub: clean all
	git clone --no-checkout --branch gh-pages . pub
	cp -r site/_site/* pub/
	cd pub && git add . && git commit -m "`date +"pub %B%d_%y"`"
	git fetch pub gh-pages:gh-pages
	rm -fr pub
