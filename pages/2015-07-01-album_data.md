	Exploring SQL: How many title tracks are placed third?
	Andy Chase
	July 01 2015

I was listening to [Florance + The Machine](http://pitchfork.com/reviews/albums/20605-how-big-how-blue-how-beautiful/)'s newest album when I noticed that a lot of music albums place their title track third on the album. Is this really the case I wonder? Well, having some abilities in Data Science I decided to see if I could get a chart out how many albums have title tracks and where they land.

# 1. Getting the data

First in order to answer this question I'm going to need some data to work with.

Music Brainz is a "MusicBrainz is a community-maintained open source encyclopedia of music information" ([About](https://musicbrainz.org/doc/About)). Since their data is open and freely avaliable it seems like a good source.

    [data]
    title: MusicBrainz Database / Download
    url: https://musicbrainz.org/doc/MusicBrainz_Database/Download
    date: 23 May 2015
    authors:
        - Stefan Kestenholz (https://about.me/stefankestenholz) (https://wiki.musicbrainz.org/User:Keschte/OfficialBio)
        - Pavan Chander (https://wiki.musicbrainz.org/About/Team)
        - Other MusicBrainz Contributors
    topic: music/metadata
    commentary: >
        Has all the music metadata you need
    description: >
        MusicBrainz started in 2000 by [Robert Kaye](http://mayhem-chaos.net/) who needed a place to store metadata files for the an unix cd player called Workman. Today MusicBrainz has metadata for 15 million records by almost a million artists worldwide ([Wikipedia Contributors, 2015](https://en.wikipedia.org/wiki/MusicBrainz)) ([MusicBrains: About](https://musicbrainz.org/doc/About/History)).
        <br><br>
        MusicBrains has expanded their open data effors into [MetaBrains](https://metabrainz.org/) which also wearhouses data for Music Cover Art, Music Critisim, and Books as well. 

# 2. Setting up an environment

1. Set up a virtual server on [Digital Ocean](//digitalocean.com/?refcode=d91055f0c205) ([non-ref](//digitalocean.com)) to work on. *Optional:* I like working on another server because a remote server has a lot of bandwidth so I can get the data quickly, and I can feel good about downloading a lot of remote scripts and dependancies without harming my local environment.
2. Followed the MusicBrainz instructions on setting up the database: [MusicBrainz Database Setup](https://bitbucket.org/lalinsky/mbslave).

# 3. Ask my question

So the goal here is now to ask the questions I have about title tracks to the database. I'm going to be querying SQL here to do this.


    [guide]
    title: SQL Tutorial
    url: http://www.w3schools.com/sql/
    date: June 15 2000
    authors:
        - W3Schools/Refsnes Data
    topic: databases/sql
    section: Sql
    subsection: What is SQL and what are the basic commands to know?
    commentary: >
        Has good introductionary information, but [w3fools](//w3fools.com) recommends that you don't stop at introduction tutorials.
    description: >
        W3Schools is a website aimed at educating people of the very basics of web technlogy.

First I have to study the [MusicBrainz Schema Diagram](https://musicbrainz.org/doc/MusicBrainz_Database/Schema) to figure out what kind of queries I have to write in order to figure out how to answer my question.

# How many albums have title tracks?

In the schema above, I found that the `musicbrainz.medium` table contains the relationship between "releases" (albums releases essentially), and tracks. I need to see how many mediums have associated tracks with the same as that medium.

{% highlight sql %}
SELECT COUNT(DISTINCT(medium.name)) -- Select names that are different
FROM musicbrainz.medium;

 count  -- <- Results
-------
 45,374
{% endhighlight %}

This is not what I expected, there should be at least a million albums out there. It turns out medium names are often blank for some reason, so I need to get the name from the release table instead. I'm going to also add in the `musicbrainz.release_group` table which will account for when there are multiple releases of one album.

{% highlight sql %}
SELECT COUNT(DISTINCT(release_group.name)) 
FROM musicbrainz.medium 
LEFT JOIN musicbrainz.release 
     ON medium.release = release.id
LEFT JOIN musicbrainz.release_group
     ON release_group.id = release.release_group;

  count  
---------
 970,467
 {% endhighlight %}

That's better.

Now I just need to find out how many albums have title tracks;

{% highlight sql %}
SELECT COUNT(DISTINCT(release_group.name)) 
FROM musicbrainz.medium
LEFT JOIN musicbrainz.release 
    ON medium.release = release.id 
LEFT JOIN musicbrainz.track 
    ON track.medium = medium.id 
LEFT JOIN musicbrainz.release_group 
    ON release_group.id = release.release_group 
WHERE lower(track.name) = lower(release_group.name);
-- ^ This is what finds the title track
-- ^ lower(track.name) so its case insensitive

 count  
--------
 250,241
{% endhighlight %}

Now for some quick calculations...

{% highlight python %}
In [1]: releases = 970467
In [2]: title_releases = 250241
In [3]: title_releases / releases
Out[3]: 0.25785626919823135
{% endhighlight %}

`26%`! That's a massive number of albums from lazy artists who can't be bothered to name all their songs without re-using the album name.

# Where are the title tracks placed (are they usually third)?

To answer this question we need to take the results from above (finding tracks that are title tracks) and query over that data, grouping up the most common positions for those tracks and counting them.

{% highlight sql %}
SELECT sub.position, count(sub.position) 
FROM (
    SELECT distinct release_group.name, track.position 
    FROM musicbrainz.medium
    LEFT JOIN musicbrainz.release 
        ON medium.release = release.id 
    LEFT JOIN musicbrainz.track 
        ON track.medium = medium.id 
    LEFT JOIN musicbrainz.release_group 
        ON release_group.id = release.release_group 
    WHERE track.name = release_group.name
    AND track.position < 10 -- Only care about the first few
    AND medium.track_count > 3 -- Skip title-track only albums
) sub 
GROUP BY sub.position
ORDER BY sub.pos;

 position | count 
----------+-------
        0 |     4
        1 | 73038
        2 | 25044
        3 | 18565
        4 | 15792
        5 | 13404
        6 | 12464
        7 | 10363
        8 |  8664
        9 |  7418
{% endhighlight %}

As a nice chart:

![chart.png](/images/2015-07-01-album_data.svg){:.fill}

As you can see my hypothesis was incorrect, it seems that artists like put the title track first. Oh well, that seems to make sense, if you were to include a title track it would make sense to put it first.

Well I hope you were able to see how you one might answer questions you might have about data using open data and data analysis tools.