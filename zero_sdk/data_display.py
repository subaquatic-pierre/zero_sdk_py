from requests.api import head


class DataDisplay:
    def __init__(self) -> None:
        self.is_list_data = None
        self.data = {}
        self.list_data = []
        self.heading = None

    def from_list(self, data_list, fields=[], heading=""):
        self.heading = heading
        self.is_list_data = True
        for el in data_list:
            element_build = {}
            for field in fields:
                val = el.get(field)
                element_build.setdefault(field, val)

            self.list_data.append(element_build)

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
        string_data = f"\n  {self.heading}:\n"
        for el in self.list_data:
            item = "- "
            first = True
            for key, val in el.items():
                if first:
                    line = f"{key} : {val} \n"
                else:
                    line = f"  {key} : {val} \n"

                item = item + line
                first = False
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
