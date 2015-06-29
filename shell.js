var KeyFromEvent = function(e) {
  var ch = String.fromCharCode(e.keyCode)
  // if is between 'a' and 'z'
  if (ch >= 'A' && ch <= 'Z') {
    if (e.shiftKey)
      return ch
    else
      return String.fromCharCode(e.keyCode + 32)
  }
  // if is between '0' and '9'
  if (ch >= '0' && ch <= '9') {
    if (!e.shiftKey)
      return ch
    // deal with shift key
  }
  // return / backspace / tab / space
  if ('\r\n\t\b '.indexOf(ch) >= 0)
    return ch

  // hash
  // see https://css-tricks.com/snippets/javascript/javascript-keycodes/
  // to complement this
  ch = {
    189: '-',
    190: '.',
  }[e.keyCode]
  if (ch)
    return ch;
  // debug for others
  console.log({
    keyCode: e.keyCode,
    shiftKey: e.shiftKey,
    metaKey: e.metaKey,
    ctrlKey: e.ctrlKey,
  })
}

var ws = new WebSocket("ws://" + location.host + "/shell")
var shell = $("#shell")[0]
ws.onopen = function() {
  $(document).on("keydown", function(e){
    var ch = KeyFromEvent(e)
    if (ch)
      ws.send(ch)
    // e.preventDefault()
  })
}
var process_output = function(data) {
  // see http://www.asciitable.com
  var i
  for (i = 0; i < data.length; i++) {
    var ch = data[i]
    if (ch >= ' ' || '\r\n\t\b'.indexOf(ch) >= 0) {
      shell.innerText += ch
    } else if (ch == '\007') { // bell
      // TODO: screen should blink here
    } else if (ch == '\033') { // escape
      // data[i+1] should be '['
      if (data[i+2] == 'K') {
        i += 2
        shell.innerText = shell.innerText.slice(0, -2)
      } else { // could be ASCII color control etc.
        shell.innerText += "\\033"
      }
    } else {
      shell.innerText += "\\0" + ch.charCodeAt(0).toString(8)
    }
  }
}
ws.onmessage = function(evt) {
  process_output(evt.data)
}
ws.onclose = function() {
  process_output("\n[Connection closed by remote host]\n")
}

