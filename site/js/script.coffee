---
---
api_key = "891c04bb5d3fea14d398fa7d4abd7ae55594f9b8+\\"

url = "https://wiki.snc.io/w/api.php"

getGoogleAnalyticsId = () ->
  name = '_ga='
  ca = document.cookie.split(';')
  i = 0
  while i < ca.length
    c = ca[i]
    while c.charAt(0) == ' '
      c = c.substring(1)
    if c.indexOf(name) == 0
      return c.substring(name.length, c.length)
    i++
  ''

getDateString = () -> new Date().toUTCString()

getSectionTitle = () -> getDateString() + "-" + getGoogleAnalyticsId()

settings = (text) ->
  action: "edit"
  format: "json"
  pageid: 9
  section: "new"
  sectiontitle: getSectionTitle()
  text: text
  summary: "Input from website"
  bot: ""
  token: api_key

window.post_suggestion = (suggestion_text) ->
  $.post(url, settings(suggestion_text))
