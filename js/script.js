(function() {
  var api_key, getDateString, getGoogleAnalyticsId, getSectionTitle, settings, url;

  api_key = "+\\";

  url = "https://wiki.snc.io/w/api.php";

  getGoogleAnalyticsId = function() {
    var c, ca, i, name;
    name = '_ga=';
    ca = document.cookie.split(';');
    i = 0;
    while (i < ca.length) {
      c = ca[i];
      while (c.charAt(0) === ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) === 0) {
        return c.substring(name.length, c.length);
      }
      i++;
    }
    return '';
  };

  getDateString = function() {
    return new Date().toUTCString();
  };

  getSectionTitle = function() {
    return getDateString() + "-" + getGoogleAnalyticsId();
  };

  settings = function(type, text) {
    return {
      action: "edit",
      format: "json",
      pageid: 9,
      section: "new",
      sectiontitle: type + "-" + getSectionTitle(),
      text: text,
      summary: "Input from website",
      bot: "",
      token: api_key
    };
  };

  window.post_suggestion = function(type, text) {
    return $.post(url, settings(type, text));
  };

}).call(this);
