from flask import render_template, session, redirect, url_for
from flask.views import MethodView
from torcms.model.post_model import MPost
from . import main

uu = MPost()


@main.route('/post/add_document', methods=['GET'])
def user():
    return render_template('doc/post/post_add.html', )


#####################################################################################################
class UserView(MethodView):
    def get(self, url_str):
        return render_template('doc/post/post_add.html', )

    def post(self, url_str):
        return render_template('doc/post/post_add.html', )
        pass


main.add_url_rule('/post/<url_str>', view_func=UserView.as_view('usesadfr'))
