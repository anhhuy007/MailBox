import flet as ft
from typing import List
import json
from model import myFunction


class FileAttachment:
    name: str
    type: str
    content: str

    def __init__(self, name: str, type: str, content: str) -> None:
        self.name = name
        self.type = type
        self.content = content

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)


class MailInfo:
    id: str
    user_email: str
    date: str
    sender: str
    to: str
    cc: str
    bcc: str
    subject: int
    body: int
    file_num: int
    file_list: List[FileAttachment]
    seen: int
    file_saved: int

    def __init__(self, id: str, user_email: str, date: str, sender: str, to: str, cc: str, bcc: str, subject: int,
                 body: int,
                 file_num: int, file_list: [FileAttachment], seen: int, file_saved: int) -> None:
        self.id = id
        self.user_email = user_email
        self.date = date
        self.sender = sender
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.body = body
        self.file_num = file_num
        self.file_list = [FileAttachment(**file_data) for file_data in file_list]
        self.seen = seen
        self.file_saved = file_saved

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f"MailInfo({self.id}, {self.user_email}, {self.date}, {self.sender}, {self.to}, {self.cc}, {self.bcc}, {self.subject}, {self.body}, {self.file_num}, {self.file_list}, {self.seen}, {self.file_saved})"


def MailContentView(mail_info: MailInfo, _seen_mail_clicked, user_email):
    def getAttachmentsName(file_list: List[FileAttachment]):
        ans: str = ""

        for file in file_list:
            ans += file.name + ", "

        # remove last ", "
        ans = ans[:-2]

        return ans

    class MailContentView(ft.BottomSheet):
        async def on_close(self, e):
            self.open = False
            await self.update_async()

        async def save_file_result(self, e: ft.FilePickerResultEvent):
            print("On save file result")
            self.save_file_path = e.path if e.path else "Canceled!"
            print(f"Destination path: {e.path}")
            myFunction.save_attach(mail_info.id, self.save_file_path, user_email)

        async def download_attachments(self, e):
            print("download_attachments")

            # get destination folder
            await self.save_file_dialog.get_directory_path_async()

        async def did_mount_async(self):
            self.page.overlay.append(self.save_file_dialog)
            await self.page.update_async()

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        async def will_unmount_async(self):
            self.page.overlay.remove(self.save_file_dialog)
            await self.page.update_async()

        async def seen_mail_clicked(self, e):
            print("seen_mail_clicked")
            myFunction.seen_mail(mail_info.id, mail_info.subject, mail_info.sender, mail_info.body, user_email)
            await _seen_mail_clicked(e)

        def get_receiver_list(self):
            ans: str = ""

            if mail_info.to != "":
                ans += mail_info.to + ", "

            elif mail_info.cc != "":
                ans += mail_info.cc + ", "

            elif mail_info.bcc != "":
                # just get user email in bcc list
                for email in mail_info.bcc.split(", "):
                    if email == mail_info.user_email:
                        ans += email + ", "

            # remove last ", "
            ans = ans[:-2]

            return ans

        def __init__(self):
            super().__init__()

            header = ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        str(mail_info.subject),
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        width=580,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),

                    ft.Container(
                        content=ft.Icon(ft.icons.CLOSE, size=20),
                        on_click=self.on_close
                    )
                ]
            )

            sender = ft.Container(
                padding=ft.padding.only(top=20, bottom=0),
                content=ft.Row(
                    controls=[
                        ft.Text("From: "),
                        ft.Text(
                            value=mail_info.sender,
                            size=13,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            width=550
                        )
                    ]
                )
            )

            to = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        ft.Text("To: "),
                        ft.Text(
                            value=mail_info.to,
                            size=13,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            width=550)
                    ]
                )
            )

            cc = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        ft.Text("CC: "),
                        ft.Text(
                            value=mail_info.cc,
                            size=13,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            width=550)
                    ]
                )
            )

            date = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        ft.Text("Date: "),
                        ft.Text(
                            value=mail_info.date,
                            size=13,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            width=550
                        )
                    ]
                )
            )

            content = ft.Container(
                padding=ft.padding.only(top=20, bottom=0),
                height=250,
                width=630,
                alignment=ft.alignment.top_left,
                content=ft.Row(
                    controls=[
                        ft.Text(
                            value=str(mail_info.body),
                            size=13,
                            max_lines=14,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            width=550
                        )
                    ]
                )
            )

            seen_and_attachment = ft.Container(
                padding=ft.padding.only(top=0),
                content=ft.Column(
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(left=5, bottom=5),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.START,
                                controls=[
                                    ft.Text(
                                        # getAttachmentsName(mail_info.file_list),
                                        "Attachments: " + getAttachmentsName(mail_info.file_list),
                                        size=13,
                                        color=ft.colors.BLUE
                                    ),
                                ]
                            )
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row([
                                    ft.FilledButton(
                                        "Mark as read",
                                        icon=ft.icons.VISIBILITY_ROUNDED,
                                        on_click=self.seen_mail_clicked
                                    ),

                                    ft.FilledButton(
                                        "Download all attachments",
                                        icon=ft.icons.DOWNLOAD_ROUNDED,
                                        on_click=self.download_attachments
                                    ),
                                ]),

                                ft.Row([
                                    ft.Text(f"{str(mail_info.file_num)} file(s) attached"),

                                    ft.Container(
                                        content=ft.Icon(ft.icons.ATTACH_FILE)
                                    )
                                ])
                            ]
                        )
                    ]
                )
            )

            self.save_file_dialog = ft.FilePicker(on_result=self.save_file_result)
            self.save_file_path = ""

            mail_info_section = ft.Column(
                spacing=0,
                controls=[
                    header,
                    sender,
                    to,
                ]
            )

            if mail_info.cc != "":
                mail_info_section.controls.append(cc)

            mail_info_section.controls.append(date)
            mail_info_section.controls.append(content)

            self.content = ft.Container(
                padding=ft.padding.only(left=20, right=20, top=10, bottom=5),
                height=500,
                width=1000,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        mail_info_section,
                        seen_and_attachment,
                    ]
                )
            )

    mail_content_view = MailContentView()
    mail_content_view.open = True
    mail_content_view.is_scroll_controlled = True

    return mail_content_view
