"""
Quick hack to turn the image dump (exported to JSON from MariaDB) into
individual Jekyll posts.
"""
import json
import base64
from datetime import datetime
from pathlib import Path

POST_ROOT = Path('_posts')


with open('skins.json') as src:
    skins = json.load(src)

    for skin in skins:
        added = datetime.strptime(skin['added'], '%Y-%m-%d %H:%M:%S')
        added = added.strftime('%Y-%m-%d')

        preview = base64.b64encode(bytes.fromhex(skin['image_combined'][2:]))
        preview = preview.decode('utf-8')

        raw = base64.b64encode(bytes.fromhex(skin['image'][2:]))
        raw = raw.decode('utf-8')

        with open(POST_ROOT / f'{added}-{skin["id"]}.md', 'wb') as out:
            out.write(f'''---
title: >
    {skin["name"]}

layout: post
permalink: /view/{skin["id"]}
votes: {skin["vote_count"]}
preview: "data:image/png;base64,{preview}"
---
<dl class="side-by-side">
<dt>Preview</dt>
<dd>
    <img class="preview" src="data:image/png;base64,{preview}">
</dd>
<dt>Original</dt>
<dd>
    <img class="preview" src="data:image/png;base64,{raw}">
</dd>
<dt>Title</dt>
<dd>{skin["name"]}</dd>
<dt>Description</dt>
<dd>{skin["description"]}</dd>
<dt>Added By</dt>
<dd>{skin["author"]}</dd>
<dt>Added On</dt>
<dd>{added}</dd>
<dt>Votes</dt>
<dd>{skin["vote_count"]}</dd>
</dl>
'''.encode('utf-8'))
