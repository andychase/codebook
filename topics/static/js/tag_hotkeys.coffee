$ ->
    tagLink = $('.tag-link')
    if tagLink.length
        $('body').keypress (e) ->
            tag = e.target.tagName.toLowerCase()
            if e.which == 100 && tag != 'input' && tag != 'textarea'
                deleteInput = $('input[name=link_delete]')
                if deleteInput.prop('checked')
                    $('.link-tag').submit()
                else
                    deleteInput.prop('checked', true)
