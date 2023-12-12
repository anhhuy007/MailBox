import flet as ft
import os
from mail_content_view import MailInfo
from mail_item_view import MailItemView


def InboxPage(user_email: str):
    class InboxPage(ft.UserControl):

        def __init__(self):
            super().__init__()
            self.mails = ft.Column(
                spacing=3,
                scroll=ft.ScrollMode.ALWAYS,
                on_scroll_interval=0,
                height=560
            )

        def build(self):
            # read all json files from folder mailBox
            folder = os.path.join(os.path.dirname(__file__), '..', 'MailBox')
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
                    mail = MailItemView(mail_info, user_email)
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

    return InboxPage()
