##################
## Ajaxify site ##
##################
$ ->
  site_navs = $('.site-nav ul li a')
  if site_navs.length
    currently_opening = false
    site_navs.each (tab_index, tab) ->
      tab = $(tab)
      tab.click (e) ->
        if not currently_opening and e.which == 1 and not e.metaKey and not e.shiftKey
          currently_opening = true
          $('.site-nav ul li a').addClass "opening"
          tab.parent().siblings().removeClass "active"
          tab.parent().addClass "active"
          opening_timer = window.setTimeout( ->
            window.location = tab.attr('href')
          , 1000)
          $.get tab.attr('href'), {html_body_only: 'true'}, (data) ->
            window.clearTimeout(opening_timer)
            history.replaceState({}, "", tab.attr('href'))
            $("body").html(data)
          return false
