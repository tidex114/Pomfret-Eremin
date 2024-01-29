import gspread

sa = gspread.service_account()
sh = sa.open("user_data")


def warn(nick):
    wks = sh.worksheet("user list")
    for i in range(2, wks.row_count + 1):
        fname = wks.cell(i, 2).value
        lname = wks.cell(i, 3).value
        if fname == nick[0] and lname == nick[1]:
            value = int(wks.cell(i, 8).value)
            if value == 0:
                wks.update_cell(i, 8, value + 1)
                return 1
            elif value == 1:
                wks.update_cell(i, 8, value + 1)
                return 2
            elif value == 2:
                wks.update_cell(i, 8, value + 1)
                return 3
    return -1
