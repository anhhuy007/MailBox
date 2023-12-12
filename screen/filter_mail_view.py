import flet as ft
import os
from mail_content_view import MailInfo
from mail_item_view import MailItemView


def FilterPage():
    def getDirectoryList(current_directory: str):
        subdirectories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
        return subdirectories

    class FilterPage(ft.UserControl):
        def __init__(self):
            super().__init__()
            self.mails = ft.Column(
                spacing=3,
                scroll=ft.ScrollMode.ALWAYS,
                height=460
            )
            self.filter_option = ft.Dropdown(
                label="Select filter",
                autofocus=True,
                text_size=17,
                height=60,
                content_padding=ft.padding.only(left=15, top=5, bottom=5, right=15),
            )
            self.options = getDirectoryList("D:\MailBox\Filter\hahuy@fitus.edu.vn")
            for option in self.options:
                self.filter_option.options.append(ft.dropdown.Option(option))

        def build(self):
            # read all json files from folder mailBox
            folder = os.path.join(os.path.dirname(__file__), '..', 'mailBox')
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
                    mail = MailItemView(mail_info)
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

            card = ft.Card(
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

            return ft.Container(
                padding=ft.padding.only(top=10),
                border_radius=10,
                bgcolor=ft.colors.WHITE,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            height=60,
                            controls=[
                                ft.Text(
                                    "Open folder: ",
                                    size=17,
                                    weight=ft.FontWeight.BOLD
                                ),
                                self.filter_option,
                                ft.OutlinedButton(
                                    "Apply",
                                    width=100,
                                    height=40,
                                )
                            ]
                        ),
                        card
                    ]
                )
            )

    return FilterPage()