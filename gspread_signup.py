import gspread

sa = gspread.service_account()
sh = sa.open("Discord Signups")


def newsignup(event_name: str, event_date: str, event_time: str, max_atendees: int, waitlist: bool):
    if event_name not in str(sh.worksheets()):
        sh.duplicate_sheet(source_sheet_id=0, new_sheet_name=f"{event_name}")
        wks = sh.worksheet("trip list")
        wks.add_rows(1)
        wks.update_cell(wks.row_count, 1, event_name)
        wks.update_cell(wks.row_count, 2, event_date)
        wks.update_cell(wks.row_count, 3, event_time)
        wks.update_cell(wks.row_count, 4, max_atendees)
        wks.update_cell(wks.row_count, 5, waitlist)
        wks.update_cell(wks.row_count, 6, str(sh.worksheet(event_name).id))
    else:
        return "trip already exists"


def adduser(first_name: str, last_name: str, grad_year: int, event_name: str, max_atendees: int, waitlist: bool):
    wks = sh.worksheet(f"{event_name}")
    for fname in wks.col_values(1):
        for lname in wks.col_values(2):
            if fname == first_name and lname == last_name:
                return "You are already on the list!"
    if wks.row_count == 1:
        wks.add_rows(1)
        wks.update_cell(wks.row_count, 1, first_name)
        wks.update_cell(wks.row_count, 2, last_name)
        wks.update_cell(wks.row_count, 3, grad_year)
        wks.update_cell(wks.row_count, 4, 1)
        wks.update_cell(wks.row_count, 5, "NO")
        return "You were added to the list!"
    elif wks.row_count - 1 < max_atendees:
        reg_num = max([eval(i) for i in wks.col_values(4)[-1:]]) + 1
        wks.add_rows(1)
        wks.update_cell(wks.row_count, 1, first_name)
        wks.update_cell(wks.row_count, 2, last_name)
        wks.update_cell(wks.row_count, 3, grad_year)
        wks.update_cell(wks.row_count, 4, reg_num)
        wks.update_cell(wks.row_count, 5, "NO")
        return "You were added to the list!"
    elif wks.row_count - 1 >= max_atendees:
        reg_num = max([eval(i) for i in wks.col_values(4)[-1:]]) + 1
        wks.add_rows(1)
        wks.update_cell(wks.row_count, 1, first_name)
        wks.update_cell(wks.row_count, 2, last_name)
        wks.update_cell(wks.row_count, 3, grad_year)
        wks.update_cell(wks.row_count, 4, reg_num)
        if waitlist:
            wks.update_cell(wks.row_count, 5, "YES")
        else:
            wks.update_cell(wks.row_count, 5, "NO")
            return "You are on the wait list!"
        return "You were added to the list!"


def removeuser(first_name: str, last_name: str, event_name: str, max_attendees: int):
    wks = sh.worksheet(f"{event_name}")
    for row in range(2, wks.row_count + 1):
        print(wks.cell(int(row), 1).value)

        if first_name == wks.cell(int(row), 1).value and last_name == wks.cell(int(row), 2).value:
            num = int(wks.cell(int(row), 4).value)

            for r in range(2, wks.row_count + 1):
                if int(wks.cell(r, 4).value) > num:
                    wks.update_cell(r, 4, int(wks.cell(r, 4).value) - 1)

            wks.delete_rows(int(row))
            if wks.row_count > 1:
                for i in range(2, max_attendees + 2):
                    wks.update_cell(i, 5, '')
            return f"You were removed from the list!"
    return "It seems you are not on the list..."


def get_signups():
    wks = sh.worksheet("trip list")
    tripnames = wks.col_values(1)[1:]
    dates = wks.col_values(2)[1:]
    times = wks.col_values(3)[1:]
    atendees = wks.col_values(4)[1:]
    wl = wks.col_values(5)[1:]
    wks_ids = wks.col_values(6)[1:]
    return tripnames, dates, times, atendees, wl, wks_ids


def removesignup(name: str):
    wks = sh.worksheet(name)
    sh.del_worksheet(wks)

