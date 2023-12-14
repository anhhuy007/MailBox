import flet as ft
import login as Login
import mail_compose_view as MailComposeView
import mail_item_view as MailItemView
import inbox_mail_view as InboxMailView
import filter_mail_view as FilterMailView
import spam_mail_view as SpamMailView
from mail_content_view import MailInfo, FileAttachment
import os
import sys
import asyncio

# Add a directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "model\\"))  # noqa
from model import pop3 as POP3Client
from model import myFunction
import json


def getDate(date):
    # raw data: "21:46:55 07/12/2023"
    # return: "07/12/2023"
    return date[9:]


class AppHeader(ft.UserControl):

    async def close_user_profile(self, e):
        self.user_profile.open = False
        await self.user_profile.update_async()

    def __init__(self, _on_fetch_email_clicked, user_email, user_password):
        super().__init__()
        self.on_fetch_email_clicked = _on_fetch_email_clicked
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
        self.user_profile = ft.AlertDialog(
            modal=True,
            title=ft.Text("User profile"),
            content=ft.Container(
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=150,
                    width = 200,
                    spacing=10,
                    controls=[
                        ft.Row(
                            [
                                ft.Icon(ft.icons.EMAIL_ROUNDED),
                                ft.Text("Email: " + user_email),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.icons.PASSWORD_ROUNDED),
                                ft.Text("Password: " + user_password),
                            ]
                        ),
                    ])
            ),
            actions=[
                ft.OutlinedButton(
                    text="Close",
                    on_click=self.close_user_profile,
                    icon=ft.icons.CLOSE_ROUNDED
                ),
                ft.FilledButton(
                    text="Sign out",
                    on_click=self.on_sign_out_clicked,
                    icon=ft.icons.LOGOUT_ROUNDED
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    async def on_user_profile_clicked(self, e):
        print("User profile clicked")
        self.user_profile.open = True
        await self.update_async()

    async def on_sign_out_clicked(self, e):
        print("Sign out")
        # clear authentication_info.json
        authen_info_path = os.path.join(os.path.dirname(__file__), '..', 'authentication_info.json')
        with open(authen_info_path, "w") as json_file:
            data_dict_ = {
                "user_email": "",
                "user_password": ""
            }
            json.dump(data_dict_, json_file)
            # close file
            json_file.close()

        # exit app
        await self.page.window_destroy_async()

    async def did_mount_async(self):
        self.page.overlay.append(self.user_profile)
        await self.update_async()

    async def will_unmount_async(self):
        self.page.overlay.remove(self.user_profile)
        await self.update_async()

    def build(self):
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
                        ft.Container(
                            on_click=self.on_user_profile_clicked,
                            content=ft.CircleAvatar(
                                foreground_image_url="https://sohanews.sohacdn.com/thumb_w/1000/160588918557773824/2021/9/14/photo1631588006082-16315880063578503538.jpg",
                                content=ft.Text("User"),
                            )
                        )
                    ]
                )

            ]
        )


def ComposeButton(user_email: str):
    class ComposeButton(ft.FloatingActionButton):

        def __init__(self):
            super().__init__()
            self.icon = ft.icons.CREATE
            self.text = "Compose"
            self.bs = MailComposeView.MailComposeView(user_email)
            self.on_click = self.show_bs

        async def show_bs(self, e):
            print("Show BS")
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

    def __init__(self, user_email: str, user_password: str):
        super().__init__()
        self.inbox_page = InboxMailView.InboxPage(user_email)
        self.spam_page = SpamMailView.SpamPage(user_email)
        self.filter_page = FilterMailView.FilterPage(user_email, user_password)
        self.inbox_page.mails.controls.clear()
        self.page_number = 0
        self.currentPage = ft.Container()
        self.compose_button = ComposeButton(user_email)

    def build(self):
        # AppBody attributes
        pages = [
            self.inbox_page,
            self.spam_page,
            self.filter_page
        ]

        page_ = ft.Container(content=pages[0], expand=True)

        # functions
        async def on_page_change(e):
            page_.content = pages[e.control.selected_index]
            self.page_number = e.control.selected_index
            self.currentPage = pages[e.control.selected_index]
            print("Current page: ", e.control.selected_index)
            await self.update_async()

        # navigation rail
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            leading=self.compose_button,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.INBOX_OUTLINED,
                    selected_icon=ft.icons.INBOX_ROUNDED,
                    label="Inbox",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.WARNING_AMBER_ROUNDED,
                    selected_icon=ft.icons.WARNING_ROUNDED,
                    label="Spam"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FILTER_ALT_OUTLINED,
                    selected_icon=ft.icons.FILTER_ALT_ROUNDED,
                    label="Filter"
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
                page_
            ],
        )


class MailApp(ft.UserControl):

    async def on_fetch_mail_clicked(self, e):
        if self.app_body.page_number != 0:
            return

        print("Fetch email")
        # get email from server
        self.client.run_pop3()

        # read all json files from folder mailBox
        folder = os.path.join(os.path.dirname(__file__), '..', 'MailBox', self.user_email, 'Inbox')
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
                mail = MailItemView.MailItemView(mail_info, self.user_email)
                self.app_body.inbox_page.mails.controls.append(mail)

        await self.app_body.inbox_page.mails.update_async()

    async def refresh_inbox(self):
        while True:
            print("Refresh inbox")
            await self.on_fetch_mail_clicked(None)
            await asyncio.sleep(10)  # Sleep for 10 minutes

    def __init__(self, user_email, user_password):
        super().__init__()
        self.app_header = AppHeader(self.on_fetch_mail_clicked, user_email, user_password)
        self.app_body = AppBody(user_email, user_password)
        self.user_email = user_email
        self.user_password = user_password
        self.client = POP3Client.POP3CLIENT(user_email, user_password)

    async def update_async(self):
        await self.app_body.update_async()

    async def did_mount_async(self):
        await self.page.update_async()

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
    async def login():
        # save login info to authentication_info.json
        authen_info_path = os.path.join(os.path.dirname(__file__), '..', 'authentication_info.json')
        with open(authen_info_path, "w") as json_file:
            data_dict_ = {
                "user_email": login_page.user_email.value,
                "user_password": login_page.user_password.value
            }
            json.dump(data_dict_, json_file)
            # close file
            json_file.close()

        # init user email box
        await page.clean_async()
        myFunction.init_user_email_box(login_page.user_email.value)
        mail_app = MailApp(login_page.user_email.value, login_page.user_password.value)
        await page.add_async(mail_app)
        mail_app_async = asyncio.gather(
            asyncio.create_task(mail_app.update_async()),
            asyncio.create_task(mail_app.refresh_inbox())
        )
        await mail_app_async

    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "MailBox"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }
    page.window_resizable = False
    page.theme = ft.Theme(font_family="Open Sans")

    login_page = Login.LoginScreen(login)
    await page.add_async(login_page)

    # read previous login info from authentication_info.json
    authen_info_path = os.path.join(os.path.dirname(__file__), '..', 'authentication_info.json')
    with open(authen_info_path, "r") as json_file:
        data_ = json_file.read()
        data_dict_ = json.loads(data_)
        if data_dict_["user_email"] != "":
            login_page.user_email.value = data_dict_["user_email"]
            login_page.user_password.value = data_dict_["user_password"]
            # close file
            json_file.close()
            await login()
        else:
            await asyncio.gather(
                asyncio.create_task(login_page.update_async()),
            )


ft.app(main)
