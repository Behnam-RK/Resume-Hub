function isUnicode(str) {
  var letters = [];
  for (var i = 0; i <= str.length; i++) {
    letters[i] = str.substring((i - 1), i);
    if (letters[i].charCodeAt() > 255) { return true; }
  }
  return false;
}

$(document).ready(function(){
  $(".autobidi").each(function(){
    if (isUnicode( $(this).text() )) {
      $(this).css('direction', 'rtl');
    }
    else {
      $(this).css('direction', 'ltr');
    }
  });
});
