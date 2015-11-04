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

link_block = """<div class="link_block" id="">
    <div class="commentary" contenteditable="true">
        <span>
        </span>
    </div>
    <div class="icon">
        <span class="opinion/yes"></span>
        <span class="ss-chat"></span>
        <span class="opinion ss-check"></span>
    </div>
    <h3 class="link_url" contenteditable="true"></h3>
    <label>
        <input class="editing-link-url" name="url" value="http://">
    </label>
    <div class="more_link_data" contenteditable="true">
    </div>
    <div class="description" contenteditable="true">
    </div>
    <div class="control-bar">
      <a class="ss-plus add-link-button"></a>
      <a class="ss-delete remove-link-button"></a>
      <a class="ss-navigateup move-link-up-button"></a>
      <a class="ss-navigatedown move-link-down-button"></a>
    </div>
</div>
"""

get_link = (link_block) ->
  link_block.children('label').children('input').first().val()

get_title = (link_block) ->
  link_block.children('.link_url').first()[0].innerText.trim()

get_type = (link_block) ->
  link_block.children('.icon').children().first().attr('class')

get_metadata = (link_block) ->
  link_block.children('.more_link_data').first()[0].innerText.trim()

get_description = (link_block) ->
  link_block.children('.description').first()[0].innerText.trim()

get_commentary = (link_block) ->
  link_block.children('.commentary').first()[0].innerText.trim()

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
    if child.tagName == "H1" and child.innerText.trim()
      output.push({section: child.innerText.trim().replace('\n', '')})
    else if child.tagName == "H2" and child.innerText.trim()
      output.push({subsection: child.innerText.trim().replace('\n', '')})
    else if child.tagName == "DIV" and child.className == "link_block"
      output.push({link: link_block_to_text($(child))})
  output

setupButtons = (element) ->
  controlBar = $(element).children('.control-bar')
  controlBar.children('.add-link-button').click ->
    new_link_block = $(link_block)
    new_link_block.hide()
    new_link_block.insertAfter($(this).parent().parent())
    new_link_block.slideDown(150)
    setupButtons(new_link_block)
  controlBar.children('.remove-link-button').click ->
    parent = $(this).parent().parent()
    parent.slideUp 150, ->
      parent.remove()
  controlBar.children('.move-link-up-button').click ->
      $(this).parent().parent().moveUp()
  controlBar.children('.move-link-down-button').click ->
      $(this).parent().parent().moveDown()

add_new_link_buttons = (topic_page) ->
  add_new_button_to($(topic_page).children().last())
  $(topic_page).children('h1').each ->
    add_new_button_to(this)



$ ->
  topic_page_form = $('#topic-edit-form')
  topic_page = topic_page_form.children('div').first()
  if topic_page.length
    if not topic_page.children().length
      $(link_block).appendTo(topic_page)
    topic_page.children('.link_block').each (index, element) ->
      setupButtons(element)
    topic_page_form.submit (e) ->
      $('<input>').attr({
        type: 'hidden'
        name: 'text'
        value: JSON.stringify(topic_form_to_output_array(topic_page))
      }).appendTo(topic_page)
