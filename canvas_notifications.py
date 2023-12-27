# Import the Canvas class
from canvasapi import Canvas
import gspread


def enable_ntf(fname: str, lname: str):
    sa = gspread.service_account()
    sh = sa.open("user_data")
    wks = sh.worksheet("user list")
    user_id = 0
    key = ""
    for i in range(2, wks.row_count + 1):
        print(str(wks.cell(i, 2).value), str(wks.cell(i, 3).value))
        print(fname, lname)
        if str(wks.cell(i, 2).value) == fname and str(wks.cell(i, 3).value) == lname:
            user_id = int(wks.cell(i, 1).value)
            print(user_id)
            key = str(wks.cell(i, 7).value)
            print(key)
    wks = sh.worksheet("canv-notf-user-list")
    wks.add_rows(1)
    wks.update_cell(wks.row_count, 1, user_id)
    wks.update_cell(wks.row_count, 2, key)
    print("gotcha")
    return "Enabled"
