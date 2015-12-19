##################
## Ajaxify site ##
##################
$ ->
    currently_opening = false
    last_page_loaded = false
    new_page_considered_at = 5 * 1000 # 5 seconds in Milliseconds
    new_page_view_timer = false

    consider_request_new_page = ->
        if not last_page_loaded?
            true
        else
            right_now = new Date()
            result = right_now - last_page_loaded > new_page_considered_at
            last_page_loaded = right_now
            result

    update_page_click = (tab, new_page) ->
        $('.quick-link').addClass "opening"
        tab.parent().siblings().removeClass "active"
        tab.parent().addClass "active"
        update_page_ajax(tab.attr('href'), new_page)

    update_page_ajax = (tab_url, new_page) ->
        # Fall back to non-ajax page load if request longer then 1 second
        opening_timer = window.setTimeout(->
            window.location = tab_url
        , 1000)
        $.get tab_url, {html_body_only: 'true'}, (data) ->
            # Update page data
            data = data.split("~~~")
            title = data[0]
            page_data = data[1]
            window.clearTimeout(opening_timer)
            # Manipulate history/location
            if not history.state? or history.state.tab_url != tab_url
                if new_page
                    history.pushState({tab_url: tab_url}, "", tab_url)
                else
                    history.replaceState({tab_url: tab_url}, "", tab_url)
            # Set page title, update page data
            document.title = title
            $(".ajax-content").html(page_data)
            window.scrollTo(0, 0)
            # Release updating lock and re-set up page for ajax
            currently_opening = false
            ajaxify()
            # Send ga collection if on page longer then new_page_considered_at
            if new_page_view_timer?
                window.clearTimeout(new_page_view_timer)
            new_page_view_timer = window.setTimeout(->
                ga('send', 'pageview');
                new_page_view_timer = false
            , new_page_considered_at)

    ajaxify = ->
        site_navs = $('.quick-link')
        if site_navs.length
            site_navs.each (tab_index, tab) ->
                tab = $(tab)
                tab.click (e) ->
                    if not currently_opening and e.which == 1 and not e.metaKey and not e.shiftKey
                        currently_opening = true
                        update_page_click(tab, consider_request_new_page())
                        return false

    # Handle browser back/forward. Delay to ignore first page load.
    window.setTimeout(->
        window.onpopstate = ->
            update_page_ajax(window.location.pathname, consider_request_new_page())
    , 50)

    ajaxify()
