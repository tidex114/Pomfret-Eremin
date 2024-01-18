# Import the Canvas class
from canvasapi import Canvas
import gspread

sa = gspread.service_account()
sh = sa.open("user_data")


def enable_ntf(fname: str, lname: str):
    wks = sh.worksheet("user list")
    user_id = 0
    key = ""
    for i in range(2, wks.row_count + 1):
        if str(wks.cell(i, 2).value) == fname and str(wks.cell(i, 3).value) == lname:
            user_id = int(wks.cell(i, 1).value)
            key = str(wks.cell(i, 7).value)
    wks = sh.worksheet("canv-notf-user-list")
    wks.add_rows(1)
    wks.update_cell(wks.row_count, 1, user_id)
    wks.update_cell(wks.row_count, 2, key)
    return "Enabled"


def disable_ntf(fname: str, lname: str):
    wks = sh.worksheet("canv-notf-user-list")
    if wks.row_count == 1:
        return "You are not on the list..."
    wks = sh.worksheet("user list")
    user_id = 0
    for i in range(2, wks.row_count + 1):
        if str(wks.cell(i, 2).value) == fname and str(wks.cell(i, 3).value) == lname:
            user_id = int(wks.cell(i, 1).value)
            break
    wks = sh.worksheet("canv-notf-user-list")
    for i in range(2, wks.row_count + 1):
        if str(wks.cell(i, 1).value == user_id):
            wks.delete_row(i)
    return "Disabled"

