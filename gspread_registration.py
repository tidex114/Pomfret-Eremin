import gspread

sa = gspread.service_account()
sh = sa.open("user_data")


def registrate(user_id: int):
    wks = sh.worksheet("user list")
    for i in range(2, wks.row_count + 1):
        if int(wks.cell(i, 1).value) == user_id:
            f_name = wks.cell(i, 2).value
            l_name = wks.cell(i, 3).value
            y_grad = wks.cell(i, 4).value
            faculty_bool = wks.cell(i, 6).value

            if faculty_bool == "NO":
                fac_true_bool = False
            elif faculty_bool == "YES":
                faculty_true_bool = True

            user_info = [f_name, l_name, y_grad, fac_true_bool]
            return user_info
    return False
