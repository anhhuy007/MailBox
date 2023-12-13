import flet as ft
import os
from flet import (
    Container, UserControl, Stack, Image, Text, Column, TextField, colors, FilledButton, OutlinedButton, Row
)


def LoginScreen(callback):
    class LoginScreen(UserControl):
        def __init__(self):
            super().__init__()
            self.bg_path = os.path.join(os.path.dirname(__file__), '..\\assets\\login_background.jpg')
            self.user_email = TextField(
                border_radius=18,
                border=ft.border.all(1, '#44f4f4f4'),
                bgcolor='transparent',
                prefix_icon=ft.icons.MAIL_ROUNDED,
                label="Enter your email",
            )
            self.user_password = TextField(
                border_radius=18,
                border=ft.border.all(1, '#44f4f4f4'),
                bgcolor='transparent',
                label='Enter your password',
                prefix_icon=ft.icons.LOCK_ROUNDED,
                suffix_icon=ft.icons.VISIBILITY_ROUNDED,
                password=True,
            )
            self.body = Container(Stack([
                Image(
                    src=self.bg_path
                ),
                Container(
                    Container(
                        Column(
                            [
                                Text(
                                    "Login to MailBox",
                                    color=colors.BLACK,
                                    weight=ft.FontWeight.W_700,
                                    size=26,
                                ),

                                Container(
                                    Column(
                                        spacing=25,
                                        controls=[
                                            self.user_email,
                                            self.user_password
                                        ])
                                ),

                                Container(
                                    content=Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=30,
                                        controls=[
                                            FilledButton(
                                                "Cancel",
                                                on_click=self.on_cancel,
                                                width=150,
                                                height=50,
                                            ),

                                            OutlinedButton(
                                                "Login",
                                                on_click=self.on_login,
                                                width=150,
                                                height=50,
                                            )
                                        ])
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND
                        ),
                        width=400,
                        height=400,
                        border_radius=18,
                        blur=ft.Blur(10, 12, ft.BlurTileMode.MIRROR),
                        border=ft.border.all(1, colors.GREY_100),
                        alignment=ft.alignment.center,
                        padding=20,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=150)
                )
            ]))
            self.is_login = False
            print("Path: ", self.bg_path)

        def valid_login_information(self):
            return str(self.user_email.value) != "" and str(self.user_password.value) != ""

        def on_cancel(self, e):
            pass

        async def on_login(self, e):
            print("On login clicked")
            await self.update_async()
            print("User email: ", self.user_email.value)
            print("User password: ", self.user_password.value)
            if self.user_email.value != '' and self.user_password.value != "":
                self.is_login = True
                await callback()
            else:
                print("Invalid login")

        async def check_login(self):
            print("Login button clicked")
            self.is_login = True

        async def update_async(self):
            await self.user_email.update_async()
            await self.user_password.update_async()
            await self.body.update_async()

        async def did_mount_async(self):
            self.is_login = False

        async def will_unmount_async(self):
            pass

        def build(self):
            return self.body

    return LoginScreen()
