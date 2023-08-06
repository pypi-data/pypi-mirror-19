from flask import render_template, request

from .. import assets, preprocessors
from ...util import wikimedia
from ..util import app_path, build_script_tags, build_style_tags


def configure(bp, config, db):

    @bp.route("/ui/")
    def ui():
        wikis = db.campaigns.wikis()
        return render_template("ui.html",
                               wikis=sorted(list(wikis)))

    @bp.route("/ui/<wiki>/")
    @preprocessors.debuggable
    def ui_wiki(wiki):
        script_tags = build_script_tags(assets.LIB_JS, config)
        style_tags = build_style_tags(assets.LIB_CSS, config)

        return render_template("ui_wiki.html",
                               script_tags=script_tags,
                               style_tags=style_tags,
                               url_root=request.url_root,
                               mw_host=wikimedia.host_from_dbname(wiki))

    return bp
