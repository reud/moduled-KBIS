# -*- coding: utf-8 -*-

# This software includes the work that is distributed in the Apache License 2.0

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import Database
import traceback
import Notifer as notif
import EnviromentVar as envi
import budgetHandler as budget

VERSION='0.0.1'
VERSION_NAME='TZBNV'
app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variabl

bud = budget.Budget()
bud.renew()
print(bud.budget_reserve_fund)
if not bud.receipts_and_expenditure:
    notif.output('Error:会計管理簿が読めていない可能性があります。')
    notif.output('出納の値がNoneになっていました。')
    exit(1)


try:
    db = Database.DataBases()
    notif.output('db　LINE_IDの登録されているメンバーを表示します。')
    print(db.Search('at', 'all'))
except:
    notif.output(traceback.format_exc())
    exit(0)

channel_secret = envi.LINE_CHANNEL_SECRET
channel_access_token = envi.LINE_CHANNEL_ACCESS_TOKEN

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

is_register_mode = False


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global is_register_mode
    bud.renew()
    text = event.message.text
    notif.output(f'メッセージが届きました。内容:\n{text}')
    if isinstance(event.source, SourceUser):  # ユーザが登録済みか確認　登録済みなら本名を入手しておく
        try:
            userdata = db.Search('at', event.source.user_id)  # リストを取得　内容はDatabase.pyを確認
            isRegistered = True
            notif.output('ユーザは登録済でした。')
            notif.output(f'現在ユーザの情報: {userdata}')
        except KeyError:
            isRegistered = False
            notif.output('未登録のユーザです。')


    print(is_register_mode)



    if text == 'menu' and isRegistered:  # 登録済みか確認したい
        notif.output('登録済ユーザーメニューの表示に移行します。')
        print(userdata)
        menu_buttons = ButtonsTemplate(  # 一応登録済みの時のメニュー　アクションの最大数は4
            title=f'ようこそ{userdata[0][1]}さん', text='\n入出金データは午前5時30分から6時間間隔で更新されます。\n最新でない可能性もあるのでご了承ください', actions=[  # リストにタプルなので注意
                MessageAction(label='滞納額照会', text='check'),
                MessageAction(label='判別予算状況照会', text='team_check'),
                MessageAction(label='全体の残高照会',text='budget'),
                MessageAction(label='KBISについて', text='about'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Menu alt text', template=menu_buttons)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'menu' and not isRegistered:
        menu_buttons = ButtonsTemplate(
            title='同意確認',
            text=f'登録ボタンを押し、\r\n指示に従って進めてください',
            actions=[
                MessageAction(label='登録', text='register')
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='Newbie Menu alt Text',
            template=menu_buttons
        )
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text=='budget' and isRegistered:
        menu_buttons = ButtonsTemplate(  # 一応登録済みの時のメニュー　アクションの最大数は4
            title='全体の残高照会', text=f'全体の関係残高は{bud.receipts_and_expenditure:,}円です。', actions=[  # リストにタプルなので注意
                MessageAction(label='メニューに戻る', text='menu'),
            ])
        template_message = TemplateSendMessage(
            alt_text=f'全体の関係残高は{bud.receipts_and_expenditure:,}円です。', template=menu_buttons)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'register' and not isRegistered:
        is_register_mode = True
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='「名字 名前」の形で名前を教えてください'),
                TextSendMessage(text='名字と名前の間には半角スペースを入れてください\r\n例:'),
                TextSendMessage(text='佐藤 太郎')

            ]
        )
    elif is_register_mode:  # ここクソコード
        try:
            res = db.RegisterOrChanger(event.message.text, event.source.user_id, True)
            if (res == '登録完了しました！'):
                pass
            else:
                raise KeyError()
            print(res)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=f'ようこそ　{event.message.text}　さん'),
                    TextSendMessage(text='登録が完了しました。'),
                    TextSendMessage(text='再度menuと打ってメニューを閲覧してください。')
                ]
            )
            isRegistered = True
            is_register_mode = False
        except KeyError:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='データベースにあなたの名前は見つかりませんでした'),
                    TextSendMessage(text='形式が正しいか確認し、再送信してください'),
                    TextSendMessage(text='どうしてもだめな場合管理者に確認してください。')
                ]
            )
        # nyaa
    elif text == 'check' and isRegistered:
        userdata = db.Search('at', event.source.user_id)
        menu_buttons = ButtonsTemplate(  # 一応登録済みの時のメニュー　アクションの最大数は4
            title='KBIS　滞納額確認', text=f'あなたの滞納額は{userdata[0][3]:,}円です', actions=[  # リストにタプルなので注意
                MessageAction(label='メニューに戻る', text='menu'),
            ])
        template_message = TemplateSendMessage(
            alt_text=f'あなたの滞納額は{userdata[0][3]:,}円です', template=menu_buttons)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'team_check' and isRegistered:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text=f'''～チームごとの残予算額～\n
設計班: {bud.budget_team_design_engineering:,}
翼班: {bud.budget_team_wing:,}
コックピット班: {bud.budget_team_cockpit:,}
接合班: {bud.budget_team_joint:,}
電装班: {bud.budget_team_electrical:,}
デザイン班: {bud.budget_team_design:,}
予備費: {bud.budget_reserve_fund:,}
                '''),
                TextSendMessage(text='menuと送信してメニュー画面に戻ります。')
            ]
        )
    elif text == 'about' and isRegistered:
        userdata = db.Search('at', event.source.user_id)
        menu_buttons = ButtonsTemplate(  # 一応登録済みの時のメニュー　アクションの最大数は4
            title='KBISについて', text=f'Kohken Balance Inquiry System\nVersion {VERSION} ({VERSION_NAME})\n\n2018 GitHub@reud moduled-KBIS',
            actions=[  # リストにタプルなので注意
                MessageAction(label='メニューに戻る', text='menu'),
            ])
        template_message = TemplateSendMessage(
            alt_text='about response', template=menu_buttons)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        pass

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)



@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)



@handler.add(FollowEvent)
def handle_follow(event):
    pass


@handler.add(UnfollowEvent)
def handle_unfollow():
    pass


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='続けるには「menu」と送信してください' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    pass


@handler.add(PostbackEvent)
def handle_postback(event):
    pass


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()

    app.run(debug=options.debug, port=options.port)
