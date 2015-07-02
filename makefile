all:
	python3 builder/ pages/
	cd site/ && jekyll b

watch:
	bash -c "fswatch pages/ | xargs -t -n1 python3 builder/ pages/ & PIDPY=$$! ; cd site/ && jekyll s & PIDJEK=$$! ; wait $$PIDPY ; wait $$PIDJEK " 

clean:
	rm -fr builder/__pycache__ site/_site site/_topics site/_posts
