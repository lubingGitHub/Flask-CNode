from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.user import User
import os
import uuid

from routes import current_user
from utils import log

main = Blueprint('index', __name__)




@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login u', u)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        print('login', session)
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    # file 上传
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        # 上传文件的名字要处理一下
        # flask也有自带的 secure_filename 函数过滤
        # filename = secure_filename(file.filename)
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        u = current_user()
        User.update(u.id, dict(
            user_image='/uploads/{}'.format(filename)
        ))

    return redirect(url_for(".setting"))


# send_from_directory  flask封装的图片处理
# nginx 静态文件
# 对应的是  <img src="{{ user.user_image }}" title="avatar"/>
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)


@main.route('/setting')
def setting():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('setting.html', user=u)

@main.route("/setting_user", methods=["POST"])
def setting_user():
    form = request.form
    log('要看表单的内容', form)
    u = current_user()
    User.update(u.id, dict(
        username='{}'.format(request.form['username']),
        signature='{}'.format(request.form['signature']),
    ))
    return redirect(url_for(".setting"))

@main.route("/setting_password", methods=["POST"])
def setting_password():
    form  = request.form
    old_pass = request.form['old_pass']
    new_pass = request.form['new_pass']
    u = current_user()
    if User.verification_password(u.id, old_pass):
        User.update(u.id, dict(
            password='{}'.format(User.salted_password(new_pass))
        ))
    return redirect(url_for(".setting"))