$ ->
  site_navs = $('.site-nav ul li a')
  if site_navs.length
    site_navs.each (tab_index, tab) ->
      tab = $(tab)
      tab.click (e) ->
        if (e.which == 1 && !e.metaKey && !e.shiftKey)
          $.get tab.attr('href'), {html_body_only: 'true'}, (data) ->
            history.replaceState({}, "", tab.attr('href'))
            $("body").html(data)
          return false
