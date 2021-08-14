from requests.api import head


class DataDisplay:
    def __init__(self, heading="", is_list_data=False, list_data=[], data={}) -> None:
        self.is_list_data = is_list_data
        self.data = data
        self.list_data = list_data
        self.heading = heading

    @staticmethod
    def from_list(data_list, fields=[], heading=""):
        list_data = []
        for el in data_list:
            element_build = {}
            for field in fields:
                val = el.get(field)
                element_build.setdefault(field, val)

            list_data.append(element_build)
        return DataDisplay(
            heading=heading,
            is_list_data=True,
            list_data=list_data,
        )

    def format_balance(self):
        if self.is_list_data:
            for el in self.list_data:
                balance = el.get("balance")
                if balance:
                    el["balance"] = "%.10f" % (balance / 10000000000)
        else:
            balance = self.data.get("balance")
            if balance:
                self.data["balance"] = "%.10f" % (balance / 10000000000)

    def build_list_display(self):
        self.format_balance()
        string_data = f"  {self.heading}:\n"
        for el in self.list_data:
            item = "- "
            el_length = len(el.keys())
            index = 0
            for key, val in el.items():
                # Add hyphen at start of each object
                if index == 0:
                    line = f"{key} : {val}"
                else:
                    line = f"  {key} : {val}"

                index += 1

                # Add new line after each key: value, not last line
                if index == el_length:
                    item = item + line
                else:
                    item = item + line + "\n"

            string_data = string_data + item

        return string_data

    def build_display(self):
        self.format_balance()

    def __str__(self) -> str:
        if self.is_list_data:
            data = self.build_list_display()
            return data

        else:
            data = self.build_display()
            return data
