months = [
    "January", "February", "March",
    "April", "May", "June", "July",
    "August", "September", "October",
    "November", "December",
    ]


def convert(date: str) -> str:
    for i in date:
        if i.isalpha():
            if date[0].isnumeric():
                raise ValueError

            else:
                if date.count(",") != 1:
                    raise ValueError

                else:
                    MM, DD, YYYY = date.replace(",", "").split()
                    if int(DD) < 1 or int(DD) > 31:
                        raise ValueError

                    try:
                        if months.index(MM) < 9:
                            MM = f"0{months.index(MM) + 1}"

                        else:
                            MM = months.index(MM) + 1

                        if int(DD) < 10:
                            DD = f"0{DD}"

                        return f"{YYYY}-{MM}-{DD}"

                    except:
                        raise ValueError

        else:
            try:
                MM, DD, YYYY = date.replace(" ", "").split("/")

                if int(MM) < 1 or int(MM) > 12 or int(DD) < 1 or int(DD) > 31:
                    raise ValueError

                if int(DD) < 10:
                    DD = f"0{DD}"

                if int(MM) < 10:
                    MM = f"0{MM}"

                return f"{YYYY}-{MM}-{DD}"

            except ValueError:
                raise ValueError


if __name__ == "__main__":
    date = input("Date: ")
    print(convert(date))
