---
---

api_key = "+\\"
url = "https://wiki.snc.io/w/api.php"

setupFeedbackSubmitter = (tag, feedback_title, message_builder) ->
  $(tag).on "submit", (event) ->
    event.preventDefault()
    target = $(event.target)
    success_target = target.children(".link_feedback_success").first()
    submit_target = target.children(".link_feedback_link_button")
    text = message_builder(target)
    if (!text)
      return

    submit_target.hide()
    success_target.text("Sending...")
    req = $.post url, settings(feedback_title, text), () ->
      success_target.text("Thanks for submitting feedback!")
      target.parent().addClass("submit_success")

    req.fail () ->
      submit_target.show()
      success_target.text("Error")

# Feedback submitters

setupFeedbackSubmitter ".link_feedback_form", "Link Feedback - ", (target) ->
  like_target = target.children("[name*='like']").first()
  dislike_target = target.children("[name*='dislike']").first()
  if (like_target.val().trim() == "" && dislike_target.val().trim() == "")
    false
  else
    """Like: #{like_target.val()}\n\nDislike: #{dislike_target.val()}"""

# Submit feedback helpers

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

settings = (type, text) ->
  action: "edit"
  format: "json"
  pageid: 9
  section: "new"
  sectiontitle: type + ga_to_hash(getGoogleAnalyticsId())
  text: text
  summary: "Input from website"
  bot: ""
  token: api_key

# Human Hash Word List
# From https://github.com/zacharyvoase/humanhash/blob/master/humanhash.py

ga_to_hash = (ga_cookie) ->
  i = Number(ga_cookie.split(".")[2])
  w = DEFAULT_WORDLIST
  w[i % 256] +
  w[(i + (i // 256)) % 256] +
  w[(i + (i // 256 * 2)) % 256] +
  w[(i + (i // 256 * 3)) % 256]

DEFAULT_WORDLIST = [
  'Ack', 'Alabama', 'Alanine', 'Alaska', 'Alpha', 'Angel', 'Apart', 'April',
  'Arizona', 'Arkansas', 'Artist', 'Asparagus', 'Aspen', 'August', 'Autumn', 'Avocado',
  'Bacon', 'Bakerloo', 'Batman', 'Beer', 'Berlin', 'Beryllium', 'Black', 'Blossom',
  'Blue', 'Bluebird', 'Bravo', 'Bulldog', 'Burger', 'Butter', 'California', 'Carbon',
  'Cardinal', 'Carolina', 'Carpet', 'Cat', 'Ceiling', 'Charlie', 'Chicken', 'Coffee',
  'Cola', 'Cold', 'Colorado', 'Comet', 'Connecticut', 'Crazy', 'Cup', 'Dakota',
  'December', 'Delaware', 'Delta', 'Diet', 'Don', 'Double', 'Early', 'Earth',
  'East', 'Echo', 'Edward', 'Eight', 'Eighteen', 'Eleven', 'Emma', 'Enemy',
  'Equal', 'Failed', 'Fanta', 'Fifteen', 'Fillet', 'Finch', 'Fish', 'Five',
  'Fix', 'Floor', 'Florida', 'Football', 'Four', 'Fourteen', 'Foxtrot', 'Freddie',
  'Friend', 'Fruit', 'Gee', 'Georgia', 'Glucose', 'Golf', 'Green', 'Grey',
  'Hamper', 'Happy', 'Harry', 'Hawaii', 'Helium', 'High', 'Hot', 'Hotel',
  'Hydrogen', 'Idaho', 'Illinois', 'India', 'Indigo', 'Ink', 'Iowa', 'Island',
  'Item', 'Jersey', 'Jig', 'Johnny', 'Juliet', 'July', 'Jupiter', 'Kansas',
  'Kentucky', 'Kilo', 'King', 'Kitten', 'Lactose', 'Lake', 'Lamp', 'Lemon',
  'Leopard', 'Lima', 'Lion', 'Lithium', 'London', 'Louisiana', 'Low', 'Magazine',
  'Magnesium', 'Maine', 'Mango', 'March', 'Mars', 'Maryland', 'Massachusetts', 'May',
  'Mexico', 'Michigan', 'Mike', 'Minnesota', 'Mirror', 'Mississippi', 'Missouri', 'Mobile',
  'Mockingbird', 'Monkey', 'Montana', 'Moon', 'Mountain', 'Muppet', 'Music', 'Nebraska',
  'Neptune', 'Network', 'Nevada', 'Nine', 'Nineteen', 'Nitrogen', 'North', 'November',
  'Nuts', 'October', 'Ohio', 'Oklahoma', 'One', 'Orange', 'Oranges', 'Oregon',
  'Oscar', 'Oven', 'Oxygen', 'Papa', 'Paris', 'Pasta', 'Pennsylvania', 'Pip',
  'Pizza', 'Pluto', 'Potato', 'Princess', 'Purple', 'Quebec', 'Queen', 'Quiet',
  'Red', 'River', 'Robert', 'Robin', 'Romeo', 'Rugby', 'Sad', 'Salami',
  'Saturn', 'September', 'Seven', 'Seventeen', 'Shade', 'Sierra', 'Single', 'Sink',
  'Six', 'Sixteen', 'Skylark', 'Snake', 'Social', 'Sodium', 'Solar', 'South',
  'Spaghetti', 'Speaker', 'Spring', 'Stairway', 'Steak', 'Stream', 'Summer', 'Sweet',
  'Table', 'Tango', 'Ten', 'Tennessee', 'Tennis', 'Texas', 'Thirteen', 'Three',
  'Timing', 'Triple', 'Twelve', 'Twenty', 'Two', 'Uncle', 'Undress', 'Uniform',
  'Uranus', 'Utah', 'Vegan', 'Venus', 'Vermont', 'Victor', 'Video', 'Violet',
  'Virginia', 'Washington', 'West', 'Whiskey', 'White', 'William', 'Winner', 'Winter',
  'Wisconsin', 'Wolfram', 'Wyoming', 'Xray', 'Yankee', 'Yellow', 'Zebra', 'Zulu',
]