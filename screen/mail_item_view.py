import flet as ft
import mail_content_view as MailContentView
from mail_content_view import MailInfo
from model import myFunction


def MailItemView(mail_info: MailInfo):
    def getDate(date):
        # raw data: "21:46:55 07/12/2023"
        # return: "07/12/2023"
        return date[9:]

    class MailItemView(ft.UserControl):
        async def seen_mail_clicked(self, e):
            print("seen_mail_clicked")
            myFunction.seen_mail(self.mail_info.id)
            self.seen_mail_status.value = True
            await self.seen_mail_status.update_async()

        def __init__(self):
            super().__init__()
            self.mail_info = mail_info
            self.email_detail = MailContentView.MailContentView(self.mail_info, self.seen_mail_clicked)
            self.email_detail.open = False
            self.seen_mail_status = ft.Checkbox(
                value=True if self.mail_info.seen == 1 else False,
                disabled=True
            )

        async def show_email_detail(self, e):
            print("Show email detail")
            self.email_detail.open = True
            await self.email_detail.update_async()

        async def close_bs(self, e):
            self.email_detail.open = False
            await self.email_detail.update_async()

        async def did_mount_async(self):
            self.page.overlay.append(self.email_detail)
            await self.page.update_async()

        async def will_unmount_async(self):
            if not self.email_detail.open:
                self.page.overlay.remove(self.email_detail)
            await self.page.update_async()

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
                on_click=self.show_email_detail
            )

    return MailItemView()
