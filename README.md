# Codebook

Codebook is a [new kind of blog][intro]. It contains *collections*, posts with a bunch of links
in them, that are organized topically. Our goal is to create one of the most comprehensive
and up-to-date organization of software development resources on the web.

It is run by [Tech Store Club][tsc] and a community of volunteers.

## Contact

- You can talk to us by [opening an issue on Github][github-issue],
- Or by hoping on to [freenode/#techstoreclub][freenode-chat].
  Note that we'll get your message but we're not always around, please wait up to a few hours for a response.

## Contribute Writing

- You can add to Codebook by using the "suggest link", "rate link", or "suggest topic" widgets around the site.
  Those go to our [wiki][wiki].
- If you are interested in writing for us, awesome! Here's [how to write a Codebook collection][write-collection],
  and here's where to [post a Codebook collection draft][draft-collection] 
- Want to write, but not sure what to write about? Contact us or take a look at [this suggestion page][sug-collection]. 

## License

Everything on this site is [(CC BY 4.0)][ccby4] which means you can use it for whatever you want as long as you
attribute us! Additionally, the software under the `builder/` directory is subject to the [MIT License][mit].

## Source Code

### Directories

- The `pages/` directory contains the collection pages for Codebook. These pages are encoded as markdown with link data indented.
- The `builder/` directory  contains the Python builder scripts for Codebook. These scripts take the pages in `pages/` and
   process them into `site/_post` pages (with nice looking links) as well as `site/_topics` pages which make up
   the category pages for the site.
- The `site/` contains the css/js/html assets for the site.
  [Jekyll][jekyll] runs over this and produces the html output for the site under `site/_site`.

### Installation

- You will need: Python3, Python-Slugify, Jekyll, fswatch, and possibly the unix utility `make`.
- First you can [clone the repository][repo] to get your own copy of the files or download a [snapshot][snapshot].
- Run `make` in the codebook directory to turn the collections into a static site located in `site/_site`.
- You can run `make watch` to serve the website and have the site regenerate whenever you makes changes under `pages/`.

### Contributing Source Code

Open a [pull request][codebook-pull] or [open an issue][codebook-issue] to help improve Codebook. 

[intro]: https://codebook.snc.io/collections/2015/06/17/introducing-codebook/
[tsc]: https://techstore.club
[github-issue]: https://github.com/techstoreclub/charter/issues
[freenode-chat]: https://webchat.freenode.net/?channels=techstoreclub&uio=d4
[write-collection]: https://wiki.snc.io/wiki/HowToWriteACollection
[draft-collection]: https://wiki.snc.io/wiki/DraftList
[wiki]: https://wiki.snc.io/
[sug-collection]: https://wiki.snc.io/wiki/CollectionSuggestion
[ccby4]: https://creativecommons.org/licenses/by/4.0/
[mit]: https://github.com/techstoreclub/codebook/tree/master/builder/LICENSE.md
[jekyll]: http://jekyllrb.com/
[repo]: https://github.com/techstoreclub/codebook
[snapshot]: https://github.com/techstoreclub/codebook/archive/master.zip
[codebook-pull]: https://github.com/techstoreclub/codebook/pulls
[codebook-issue]: https://github.com/techstoreclub/codebook/issues
