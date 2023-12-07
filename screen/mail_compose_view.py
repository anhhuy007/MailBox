import flet as ft

#import error right here, fix this
from model import smtp

def MailComposeView():
    class MailComposeView(ft.BottomSheet):

        async def on_close(self, e):
            self.open = False
            await self.update_async()

        def check_valid_info(self):
            print("Value: ", self.textfield_title.value)

            self.to = str(self.textfield_to.value)
            self.cc = str(self.textfield_cc.value)
            self.bcc = str(self.textfield_bcc.value)
            self.title = str(self.textfield_title.value)
            self.content = str(self.textfield_content.value)

            if self.title == "":
                self.title = "No title"

            return self.to != ""

        async def send_mail_clicked(self, e):
            if self.check_valid_info():
                # send email here
                print("OK data")
                client = smtp.SMTPCLIENT("codingAkerman@fit.hcmus.edu.vn",self.to, self.cc,
                                     self.bcc, self.title, self.content,"txtattach.txt")
                
                client.send_mail()

        def __init__(self):
            super().__init__()
            self.to = ""
            self.cc = ""
            self.bcc = ""
            self.title = ""
            self.content = ""

            self.textfield_to = ft.TextField(
                hint_text="To",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_cc = ft.TextField(
                hint_text="CC",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_bcc = ft.TextField(
                hint_text="BCC",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_title = ft.TextField(
                hint_text="Title",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_content = ft.TextField(
                hint_text="Content",
                height=150,
                width=630,
                border_color='transparent',
                text_size=13,
                multiline=True,
                max_length=1000
            )

            header = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "New email",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Container(
                        content=ft.Icon(ft.icons.CLOSE, size=20),
                        on_click=self.on_close
                    )
                ]
            )

            to = ft.Container(
                padding=ft.padding.only(top=20, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_to
                    ]
                )
            )

            cc = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_cc
                    ]
                )
            )

            bcc = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_bcc
                    ]
                )
            )

            title = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_title
                    ]
                )
            )

            content = ft.Container(
                padding=ft.padding.only(top=0, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_content
                    ]
                )
            )

            send_and_attach = ft.Container(
                padding=ft.padding.only(top=0),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.FilledButton(
                            "Send",
                            icon=ft.icons.SEND_ROUNDED,
                            on_click=self.send_mail_clicked
                        ),

                        ft.Container(
                            content=ft.Icon(ft.icons.ATTACH_FILE)
                        )
                    ]
                )
            )

            self.content = ft.Container(
                padding=ft.padding.only(left=20, right=20, top=10),
                height=500,
                width=1000,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        header,
                        to,
                        ft.Divider(thickness=1, height=1),
                        cc,
                        ft.Divider(thickness=1, height=1),
                        bcc,
                        ft.Divider(thickness=1, height=1),
                        title,
                        ft.Divider(thickness=1, height=1),
                        content,
                        send_and_attach,
                    ]
                )
            )

    return MailComposeView()
