$ ->
  currently_opening = false
  site_navs = $('.site-nav ul li a')
  if site_navs.length
    site_navs.each (tab_index, tab) ->
      tab = $(tab)
      tab.click (e) ->
        if (!currently_opening && e.which == 1 && !e.metaKey && !e.shiftKey)
          currently_opening = true
          $('.site-nav ul li a').addClass "opening"
          tab.parent().siblings().removeClass "active"
          tab.parent().addClass "active"
          opening_timer = window.setTimeout ->
            window.location = tab.attr('href')
          , 1000
          $.get tab.attr('href'), {html_body_only: 'true'}, (data) ->
            window.clearTimeout(opening_timer)
            history.replaceState({}, "", tab.attr('href'))
            $("body").html(data)
          return false
