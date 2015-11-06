## External Functions and Helpers
##

$.fn.moveUp = ->
  $.each this, ->
    $(this).after $(this).prev()

$.fn.moveDown = ->
  $.each this, ->
    $(this).before $(this).next()


#################
## Saving Page ##
#################

link_block = """
<div class="link_block portlet">
    <div class="portlet-header ui-widget-header ui-corner-all ui-sortable-handle">
        <span class="ui-icon ui-icon-minusthick portlet-toggle"></span>
    </div>

    <textarea class="commentary" placeholder="Commentary"></textarea>
    <div class="icon mirror">
        <span class="opinion/yes"></span>
        <span class="ss-chat"></span>
        <span class="opinion ss-check"></span>
    </div>
    <input class="link_url" placeholder="Link title" value="">
    <label>
        <input class="editing-link-url" name="url" placeholder="https://example.org" value="">
    </label>
    <input class="more_link_data" placeholder="Metadata" value="">
    <textarea class="description" placeholder="Description"></textarea>
</div>
"""

bigger_header_block = """
<h1 class="portlet">
    <div class="portlet-header ui-widget-header ui-corner-all" contenteditable="false">
      <span class='ui-icon ui-icon-minusthick portlet-toggle'></span>
  </div>
  <input placeholder="Heading" />
</h1>
"""

smaller_header_block = """
<h2 class="portlet">
    <div class="portlet-header ui-widget-header ui-corner-all" contenteditable="false">
        <span class='ui-icon ui-icon-minusthick portlet-toggle'></span>
    </div>
    <input placeholder="Subheading" />
</h2>
"""

get_link = (link_block) ->
  link_block.children('label').children('input').first().val()

get_title = (link_block) ->
  link_block.children('.link_url').val().trim()

get_type = (link_block) ->
  link_block.children('.icon').children().first().attr('class')

get_metadata = (link_block) ->
  link_block.children('.more_link_data').val().trim()

get_description = (link_block) ->
  link_block.children('.description').val().trim()

get_commentary = (link_block) ->
  link_block.children('.commentary').val().trim()

link_block_to_text = (link_block) ->
  type: get_type(link_block)
  title: get_title(link_block)
  url: get_link(link_block)
  metadata: get_metadata(link_block)
  desc: get_description(link_block)
  commentary: get_commentary(link_block)


topic_form_to_output_array = (topic_page) ->
  output = []
  for child in topic_page.children()
    if child.tagName == "H1" and $(child).children('input').val().trim()
      output.push({section: $(child).children('input').val()})
    else if child.tagName == "H2" and $(child).children('input').val().trim()
      output.push({subsection: $(child).children('input').val()})
    else if child.tagName == "DIV" and $(child).hasClass("link_block")
      output.push({link: link_block_to_text($(child))})
  output

setupButtons = (topic_page_form) ->
  controlBar = $(topic_page_form).children('.edit-topic-add-element')
  elementBuilder = (block) ->
    ->
      new_link_block = $(block)
      new_link_block.hide()
      new_link_block.appendTo(topic_page_form.children('.column').first())
      new_link_block.slideDown(150)
      new_link_block.find(".portlet-toggle").click ->
        icon = $(this);
        icon.toggleClass("ui-icon-minusthick ui-icon-plusthick");
        icon.closest(".portlet").slideUp 150, ->
          $(this).remove();
      new_link_block.find("textarea").on('keyup', sizeTextArea)

  controlBar.find('.link').click(elementBuilder(link_block))
  controlBar.find('.bigger-header').click(elementBuilder(bigger_header_block))
  controlBar.find('.smaller-header').click(elementBuilder(smaller_header_block))

add_new_link_buttons = (topic_page) ->
  add_new_button_to($(topic_page).children().last())
  $(topic_page).children('h1').each ->
    add_new_button_to(this)

sizeTextArea = ->
  this.style.height = 0;
  this.style.height = (this.scrollHeight + 10) + 'px'

$ ->
  topic_page_form = $('#topic-edit-form')
  topic_page = topic_page_form.children('div').first()
  if topic_page.length
    setupButtons(topic_page_form)
    topic_page_form.submit (e) ->
      $('<input>').attr({
        type: 'hidden'
        name: 'text'
        value: JSON.stringify(topic_form_to_output_array(topic_page))
      }).appendTo(topic_page)

    # Prevent Enter Submit
    topic_page_form.find('input').on 'keyup keypress', (e) ->
      code = e.keyCode or e.which
      if code == 13
        e.preventDefault()
        false

    # Size textareas automatically
    $('textarea').each(sizeTextArea)
    $('textarea').on('keyup', sizeTextArea)

