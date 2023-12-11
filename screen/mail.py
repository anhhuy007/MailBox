import flet as ft
import mail_content_view as MailContentView
import mail_compose_view as MailComposeView
from mail_content_view import MailInfo, FileAttachment
import os
import sys
import threading
import time
import asyncio

# Add a directory to sys.path
sys.path.append('D:\MailBox\screen\model')
from model import pop3 as POP3Client
from model import myFunction


def getDate(date):
    # raw data: "21:46:55 07/12/2023"
    # return: "07/12/2023"
    return date[9:]


# def on_fetch_email_clicked(e):
#     print("Fetch email")
#     # get email from server
#     client = POP3Client.POP3CLIENT("hahuy@fitus.edu.vn", "123")
#     client.run_pop3()

class AppHeader(ft.UserControl):

    def __init__(self, _on_fetch_email_clicked):
        super().__init__()
        self.on_fetch_email_clicked = _on_fetch_email_clicked

    def build(self):
        self.iconTitle = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            width=100,
            controls=[
                ft.Icon(name=ft.icons.MAIL_ROUNDED, size=30),
                ft.Text(
                    "MailBox",
                    size=25,
                    weight=ft.FontWeight.BOLD
                )
            ]
        )

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=1200,
            controls=[
                self.iconTitle,

                ft.TextField(
                    label="Find in mailbox",
                    width=500,
                    prefix_icon=ft.icons.SEARCH_OUTLINED,
                    border_radius=100,
                    content_padding=10
                ),

                ft.Row(
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.DOWNLOAD_ROUNDED,
                            icon_size=30,
                            autofocus=False,
                            on_click=self.on_fetch_email_clicked

                        ),
                        ft.CircleAvatar(
                            foreground_image_url="https://sohanews.sohacdn.com/thumb_w/1000/160588918557773824/2021/9/14/photo1631588006082-16315880063578503538.jpg",
                            content=ft.Text("User")
                        )
                    ]
                )

            ]
        )


class Mail(ft.UserControl):

    async def on_email_clicked(self, e):
        print("on click")
        self.bs.open = True
        await self.bs.update_async()

    async def seen_mail_clicked(self, e):
        print("seen_mail_clicked")
        myFunction.seen_mail(self.mail_info.id)
        self.seen_mail_status.value = True
        await self.seen_mail_status.update_async()

    def __init__(self, mail_info: MailInfo):
        super().__init__()
        self.mail_info = mail_info
        self.bs = MailContentView.MailContentView(self.mail_info, self.seen_mail_clicked)
        self.bs.open = False
        self.seen_mail_status = ft.Checkbox(
            value=True if self.mail_info.seen == 1 else False,
            disabled=True
        )

    def build(self):
        return ft.Container(
            bgcolor=ft.colors.GREY_100,
            padding=ft.padding.all(5),
            content=ft.Row(
                width=1050,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=self.seen_mail_status,
                                width=10
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=50),
                                content=ft.Text(
                                    value=self.mail_info.sender,
                                    width=180,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=ft.Text(
                                    value=str(self.mail_info.subject),
                                    width=260,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=ft.Text(
                                    value=str(self.mail_info.body),
                                    width=360,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=ft.Text(
                                    value=getDate(self.mail_info.date),
                                    width=100,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                            ),
                        ]
                    )
                ]
            ),
            on_click=self.on_email_clicked
        )

    async def did_mount_async(self):
        self.page.overlay.append(self.bs)
        await self.page.update_async()

    # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    async def will_unmount_async(self):
        self.page.overlay.remove(self.bs)
        await self.page.update_async()


class InboxPage(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.mails = ft.Column(
            spacing=3,
            scroll=ft.ScrollMode.ALWAYS
        )

    def build(self):
        # read all json files from folder mailBox
        folder = os.path.join(os.path.dirname(__file__), '..','mailBox')
        mail_list = []
        for file in os.listdir(folder):
            if file.endswith(".json"):
                mail_list.append(file)

        # sort mail_list by date
        mail_list.sort(key=lambda x: os.path.getmtime(folder + "/" + x), reverse=True)
        self.mails.controls.clear()
        for file in mail_list:
            with open(folder + "/" + file, "r") as json_file:
                data = json_file.read()
                mail_info = MailInfo.from_json(data)
                mail = Mail(mail_info)
                self.mails.controls.append(mail)

        inbox_title = ft.Container(padding=ft.padding.only(top=10, left=5), content=ft.Row(width=1050, controls=[
            ft.Container(
                margin=ft.margin.only(left=15),
                width=10
            ),

            ft.Container(
                margin=ft.margin.only(left=50),
                content=ft.Text("Sender", width=180, weight=ft.FontWeight.BOLD),
            ),

            ft.Container(
                margin=ft.margin.only(left=15),
                content=ft.Text("Title", width=260, weight=ft.FontWeight.BOLD),
            ),

            ft.Container(
                margin=ft.margin.only(left=15),
                content=ft.Text("Content", width=360, weight=ft.FontWeight.BOLD),
            ),

            ft.Container(
                margin=ft.margin.only(left=15),
                content=ft.Text("Date", width=100, weight=ft.FontWeight.BOLD),
            )

        ]))

        return ft.Card(
            elevation=10,
            surface_tint_color=ft.colors.WHITE,
            content=ft.Column(
                controls=[
                    inbox_title,
                    ft.Container(
                        border_radius=10,
                        content=self.mails
                    )
                ]
            )
        )


def ComposeButton():
    class ComposeButton(ft.FloatingActionButton):

        def __init__(self):
            super().__init__()
            self.icon = ft.icons.CREATE
            self.text = "Compose"
            self.on_click = self.show_bs
            self.bs = MailComposeView.MailComposeView()

        def bs_dismissed(self, e):
            print("Dismissed!")

        async def show_bs(self, e):
            self.bs.open = True
            await self.bs.update_async()

        async def close_bs(self, e):
            self.bs.open = False
            await self.bs.update_async()

        # happens when example is added to the page (when user chooses the BottomSheet control from the grid)
        async def did_mount_async(self):
            self.page.overlay.append(self.bs)
            await self.page.update_async()

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        async def will_unmount_async(self):
            self.page.overlay.remove(self.bs)
            await self.page.update_async()

    compose_button = ComposeButton()
    compose_button.width = 140

    return compose_button


class AppBody(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.inbox_page = InboxPage()
        self.inbox_page.mails.controls.clear()

    def build(self):
        # AppBody attributes

        pages = [
            self.inbox_page,
            ft.Container(content=ft.Text("Page 2")),
            ft.Container(content=ft.Text("Page 3")),
        ]

        page = ft.Container(content=pages[0], expand=True)

        # functions
        async def on_page_change(e):
            page.content = pages[e.control.selected_index]
            print("Current page: ", e.control.selected_index)
            await self.update_async()

        # navigation rail
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            leading=ComposeButton(),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.INBOX_OUTLINED,
                    selected_icon=ft.icons.INBOX_ROUNDED,
                    label="Inbox",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SEND_OUTLINED,
                    selected_icon=ft.icons.SEND_ROUNDED,
                    label="Sent"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS_ROUNDED,
                    label="Setting"
                ),
            ],
            on_change=on_page_change
        )

        return ft.Row(
            expand=True,
            height=600,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                rail,
                ft.VerticalDivider(width=2, color=ft.colors.BLACK),
                page
            ],
        )


class MailApp(ft.UserControl):

    async def on_fetch_mail_clicked(self, e):
        print("Fetch email")
        # get email from server
        client = POP3Client.POP3CLIENT("mail1@gmail.com", "123")
        client.run_pop3()

        # read all json files from folder mailBox
        folder = os.path.join(os.path.dirname(__file__), '..') + "\\mailBox"
        mail_list = []
        for file in os.listdir(folder):
            if file.endswith(".json"):
                mail_list.append(file)

        # sort mail_list by date
        mail_list.sort(key=lambda x: os.path.getmtime(folder + "/" + x), reverse=True)

        # clear inbox page
        self.app_body.inbox_page.mails.controls.clear()

        # add new mail to inbox page
        for file in mail_list:
            with open(folder + "/" + file, "r") as json_file:
                data = json_file.read()
                mail_info = MailInfo.from_json(data)
                mail = Mail(mail_info)
                self.app_body.inbox_page.mails.controls.append(mail)

        await self.app_body.inbox_page.mails.update_async()

    async def refresh_inbox(self):
        while True:
            print("Refresh inbox")
            # get email from server
            # self.on_fetch_mail_clicked(None)
            await asyncio.sleep(10)

    def __init__(self):
        super().__init__()
        self.app_header = AppHeader(self.on_fetch_mail_clicked)
        self.app_body = AppBody()
        self.refresh_thread = threading.Thread(target=self.refresh_inbox)

    async def did_mount_async(self):
        # self.refresh_thread.start()
        await self.app_body.inbox_page.update_async()
        await self.update_async()

    async def will_unmount_async(self):
        print("Mail app unmount")
        self.app_body.inbox_page.controls.clear()

    def build(self):
        return ft.Column(
            expand=True,
            controls=[
                self.app_header,
                self.app_body
            ]
        )


async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "MailBox"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }

    page.window_resizable = False

    page.theme = ft.Theme(font_family="Open Sans")
    await page.add_async(MailApp())


ft.app(main)
