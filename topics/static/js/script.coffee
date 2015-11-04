#################
## Saving Page ##
#################

link_block = """<div class="link_block" id="">
    <div class="commentary" contenteditable="true">
        <span>
        </span>
    </div>
    <div class="icon mirror">
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

add_new_button_to = (target) ->
  new_button = $('<a>').attr({
    class: 'ss-plus add-link-button'
  })
  new_button.insertAfter(target)
  new_button.click ->
    $(link_block).insertAfter(target)

add_new_link_buttons = (topic_page) ->
  add_new_button_to($(topic_page).children().last())
  $(topic_page).children('h1').each ->
    add_new_button_to(this)

$(document).ready ->
  topic_page = $('#topic-edit-form')
  add_new_link_buttons(topic_page)
  if topic_page.length
    topic_page.submit (e) ->
      $('<input>').attr({
        type: 'hidden'
        name: 'text'
        value: JSON.stringify(topic_form_to_output_array(topic_page))
      }).appendTo(topic_page)

