(function() {
  var DEFAULT_WORDLIST, api_key, ct_input_name, ga_to_hash, getGoogleAnalyticsId, rand, settings, setupFeedbackSubmitter, url;

  api_key = "+\\";

  url = "https://wiki.snc.io/w/api.php";

  setupFeedbackSubmitter = function(tag, feedback_title, message_builder) {
    return $(tag).on("submit", function(event) {
      var req, submit_target, success_target, target, text;
      event.preventDefault();
      target = $(event.target);
      success_target = target.children(".link_feedback_success").first();
      submit_target = target.children(".link_feedback_link_button");
      text = message_builder(target);
      if (!text) {
        return;
      }
      submit_target.hide();
      success_target.text("Sending...");
      req = $.post(url, settings(feedback_title, text), function() {
        success_target.text("Thanks for submitting feedback!");
        return target.addClass("submit_success");
      });
      return req.fail(function() {
        submit_target.show();
        return success_target.text("Error");
      });
    });
  };

  setupFeedbackSubmitter(".link_feedback_form", "Link Feedback - ", function(target) {
    var dislike_target, like_target;
    like_target = target.children("[name*='like']").first();
    dislike_target = target.children("[name*='dislike']").first();
    if (like_target.val().trim() === "" && dislike_target.val().trim() === "") {
      return false;
    } else {
      return "Like: " + (like_target.val()) + "\n\nDislike: " + (dislike_target.val());
    }
  });

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

  settings = function(type, text) {
    return {
      action: "edit",
      format: "json",
      pageid: 9,
      section: "new",
      sectiontitle: type + ga_to_hash(getGoogleAnalyticsId()),
      text: text,
      summary: "Input from website",
      bot: "",
      token: api_key
    };
  };

  ga_to_hash = function(ga_cookie) {
    var i, w;
    i = Number(ga_cookie.split(".")[2]);
    w = DEFAULT_WORDLIST;
    return w[i % 256] + w[(i + (Math.floor(i / 256))) % 256] + w[(i + (Math.floor(i / 256) * 2)) % 256] + w[(i + (Math.floor(i / 256) * 3)) % 256];
  };

  DEFAULT_WORDLIST = ['Ack', 'Alabama', 'Alanine', 'Alaska', 'Alpha', 'Angel', 'Apart', 'April', 'Arizona', 'Arkansas', 'Artist', 'Asparagus', 'Aspen', 'August', 'Autumn', 'Avocado', 'Bacon', 'Bakerloo', 'Batman', 'Beer', 'Berlin', 'Beryllium', 'Black', 'Blossom', 'Blue', 'Bluebird', 'Bravo', 'Bulldog', 'Burger', 'Butter', 'California', 'Carbon', 'Cardinal', 'Carolina', 'Carpet', 'Cat', 'Ceiling', 'Charlie', 'Chicken', 'Coffee', 'Cola', 'Cold', 'Colorado', 'Comet', 'Connecticut', 'Crazy', 'Cup', 'Dakota', 'December', 'Delaware', 'Delta', 'Diet', 'Don', 'Double', 'Early', 'Earth', 'East', 'Echo', 'Edward', 'Eight', 'Eighteen', 'Eleven', 'Emma', 'Enemy', 'Equal', 'Failed', 'Fanta', 'Fifteen', 'Fillet', 'Finch', 'Fish', 'Five', 'Fix', 'Floor', 'Florida', 'Football', 'Four', 'Fourteen', 'Foxtrot', 'Freddie', 'Friend', 'Fruit', 'Gee', 'Georgia', 'Glucose', 'Golf', 'Green', 'Grey', 'Hamper', 'Happy', 'Harry', 'Hawaii', 'Helium', 'High', 'Hot', 'Hotel', 'Hydrogen', 'Idaho', 'Illinois', 'India', 'Indigo', 'Ink', 'Iowa', 'Island', 'Item', 'Jersey', 'Jig', 'Johnny', 'Juliet', 'July', 'Jupiter', 'Kansas', 'Kentucky', 'Kilo', 'King', 'Kitten', 'Lactose', 'Lake', 'Lamp', 'Lemon', 'Leopard', 'Lima', 'Lion', 'Lithium', 'London', 'Louisiana', 'Low', 'Magazine', 'Magnesium', 'Maine', 'Mango', 'March', 'Mars', 'Maryland', 'Massachusetts', 'May', 'Mexico', 'Michigan', 'Mike', 'Minnesota', 'Mirror', 'Mississippi', 'Missouri', 'Mobile', 'Mockingbird', 'Monkey', 'Montana', 'Moon', 'Mountain', 'Muppet', 'Music', 'Nebraska', 'Neptune', 'Network', 'Nevada', 'Nine', 'Nineteen', 'Nitrogen', 'North', 'November', 'Nuts', 'October', 'Ohio', 'Oklahoma', 'One', 'Orange', 'Oranges', 'Oregon', 'Oscar', 'Oven', 'Oxygen', 'Papa', 'Paris', 'Pasta', 'Pennsylvania', 'Pip', 'Pizza', 'Pluto', 'Potato', 'Princess', 'Purple', 'Quebec', 'Queen', 'Quiet', 'Red', 'River', 'Robert', 'Robin', 'Romeo', 'Rugby', 'Sad', 'Salami', 'Saturn', 'September', 'Seven', 'Seventeen', 'Shade', 'Sierra', 'Single', 'Sink', 'Six', 'Sixteen', 'Skylark', 'Snake', 'Social', 'Sodium', 'Solar', 'South', 'Spaghetti', 'Speaker', 'Spring', 'Stairway', 'Steak', 'Stream', 'Summer', 'Sweet', 'Table', 'Tango', 'Ten', 'Tennessee', 'Tennis', 'Texas', 'Thirteen', 'Three', 'Timing', 'Triple', 'Twelve', 'Twenty', 'Two', 'Uncle', 'Undress', 'Uniform', 'Uranus', 'Utah', 'Vegan', 'Venus', 'Vermont', 'Victor', 'Video', 'Violet', 'Virginia', 'Washington', 'West', 'Whiskey', 'White', 'William', 'Winner', 'Winter', 'Wisconsin', 'Wolfram', 'Wyoming', 'Xray', 'Yankee', 'Yellow', 'Zebra', 'Zulu'];

  !function(a){"use strict";function b(a,b){var c=(65535&a)+(65535&b),d=(a>>16)+(b>>16)+(c>>16);return d<<16|65535&c}function c(a,b){return a<<b|a>>>32-b}function d(a,d,e,f,g,h){return b(c(b(b(d,a),b(f,h)),g),e)}function e(a,b,c,e,f,g,h){return d(b&c|~b&e,a,b,f,g,h)}function f(a,b,c,e,f,g,h){return d(b&e|c&~e,a,b,f,g,h)}function g(a,b,c,e,f,g,h){return d(b^c^e,a,b,f,g,h)}function h(a,b,c,e,f,g,h){return d(c^(b|~e),a,b,f,g,h)}function i(a,c){a[c>>5]|=128<<c%32,a[(c+64>>>9<<4)+14]=c;var d,i,j,k,l,m=1732584193,n=-271733879,o=-1732584194,p=271733878;for(d=0;d<a.length;d+=16)i=m,j=n,k=o,l=p,m=e(m,n,o,p,a[d],7,-680876936),p=e(p,m,n,o,a[d+1],12,-389564586),o=e(o,p,m,n,a[d+2],17,606105819),n=e(n,o,p,m,a[d+3],22,-1044525330),m=e(m,n,o,p,a[d+4],7,-176418897),p=e(p,m,n,o,a[d+5],12,1200080426),o=e(o,p,m,n,a[d+6],17,-1473231341),n=e(n,o,p,m,a[d+7],22,-45705983),m=e(m,n,o,p,a[d+8],7,1770035416),p=e(p,m,n,o,a[d+9],12,-1958414417),o=e(o,p,m,n,a[d+10],17,-42063),n=e(n,o,p,m,a[d+11],22,-1990404162),m=e(m,n,o,p,a[d+12],7,1804603682),p=e(p,m,n,o,a[d+13],12,-40341101),o=e(o,p,m,n,a[d+14],17,-1502002290),n=e(n,o,p,m,a[d+15],22,1236535329),m=f(m,n,o,p,a[d+1],5,-165796510),p=f(p,m,n,o,a[d+6],9,-1069501632),o=f(o,p,m,n,a[d+11],14,643717713),n=f(n,o,p,m,a[d],20,-373897302),m=f(m,n,o,p,a[d+5],5,-701558691),p=f(p,m,n,o,a[d+10],9,38016083),o=f(o,p,m,n,a[d+15],14,-660478335),n=f(n,o,p,m,a[d+4],20,-405537848),m=f(m,n,o,p,a[d+9],5,568446438),p=f(p,m,n,o,a[d+14],9,-1019803690),o=f(o,p,m,n,a[d+3],14,-187363961),n=f(n,o,p,m,a[d+8],20,1163531501),m=f(m,n,o,p,a[d+13],5,-1444681467),p=f(p,m,n,o,a[d+2],9,-51403784),o=f(o,p,m,n,a[d+7],14,1735328473),n=f(n,o,p,m,a[d+12],20,-1926607734),m=g(m,n,o,p,a[d+5],4,-378558),p=g(p,m,n,o,a[d+8],11,-2022574463),o=g(o,p,m,n,a[d+11],16,1839030562),n=g(n,o,p,m,a[d+14],23,-35309556),m=g(m,n,o,p,a[d+1],4,-1530992060),p=g(p,m,n,o,a[d+4],11,1272893353),o=g(o,p,m,n,a[d+7],16,-155497632),n=g(n,o,p,m,a[d+10],23,-1094730640),m=g(m,n,o,p,a[d+13],4,681279174),p=g(p,m,n,o,a[d],11,-358537222),o=g(o,p,m,n,a[d+3],16,-722521979),n=g(n,o,p,m,a[d+6],23,76029189),m=g(m,n,o,p,a[d+9],4,-640364487),p=g(p,m,n,o,a[d+12],11,-421815835),o=g(o,p,m,n,a[d+15],16,530742520),n=g(n,o,p,m,a[d+2],23,-995338651),m=h(m,n,o,p,a[d],6,-198630844),p=h(p,m,n,o,a[d+7],10,1126891415),o=h(o,p,m,n,a[d+14],15,-1416354905),n=h(n,o,p,m,a[d+5],21,-57434055),m=h(m,n,o,p,a[d+12],6,1700485571),p=h(p,m,n,o,a[d+3],10,-1894986606),o=h(o,p,m,n,a[d+10],15,-1051523),n=h(n,o,p,m,a[d+1],21,-2054922799),m=h(m,n,o,p,a[d+8],6,1873313359),p=h(p,m,n,o,a[d+15],10,-30611744),o=h(o,p,m,n,a[d+6],15,-1560198380),n=h(n,o,p,m,a[d+13],21,1309151649),m=h(m,n,o,p,a[d+4],6,-145523070),p=h(p,m,n,o,a[d+11],10,-1120210379),o=h(o,p,m,n,a[d+2],15,718787259),n=h(n,o,p,m,a[d+9],21,-343485551),m=b(m,i),n=b(n,j),o=b(o,k),p=b(p,l);return[m,n,o,p]}function j(a){var b,c="";for(b=0;b<32*a.length;b+=8)c+=String.fromCharCode(a[b>>5]>>>b%32&255);return c}function k(a){var b,c=[];for(c[(a.length>>2)-1]=void 0,b=0;b<c.length;b+=1)c[b]=0;for(b=0;b<8*a.length;b+=8)c[b>>5]|=(255&a.charCodeAt(b/8))<<b%32;return c}function l(a){return j(i(k(a),8*a.length))}function m(a,b){var c,d,e=k(a),f=[],g=[];for(f[15]=g[15]=void 0,e.length>16&&(e=i(e,8*a.length)),c=0;16>c;c+=1)f[c]=909522486^e[c],g[c]=1549556828^e[c];return d=i(f.concat(k(b)),512+8*b.length),j(i(g.concat(d),640))}function n(a){var b,c,d="0123456789abcdef",e="";for(c=0;c<a.length;c+=1)b=a.charCodeAt(c),e+=d.charAt(b>>>4&15)+d.charAt(15&b);return e}function o(a){return unescape(encodeURIComponent(a))}function p(a){return l(o(a))}function q(a){return n(p(a))}function r(a,b){return m(o(a),o(b))}function s(a,b){return n(r(a,b))}function t(a,b,c){return b?c?r(b,a):s(b,a):c?p(a):q(a)}"function"==typeof define&&define.amd?define(function(){return t}):a.md5=t}(this);;

  rand = function(min, max) {
    return Math.random() * (max - min) + min;
  };

  ct_input_name = "ct_checkjs_" + (md5(rand(0, 1000)));

  $(document).ready(function() {
    return $("[name*='ct_checkjs']").each(function(i, val) {
      val.id = ct_input_name;
      return val.value = "cb2b2fb6bee3251f032a965d4a36e99b";
    });
  });

}).call(this);
