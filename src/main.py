import importlib
import re
import typing as t
import os
import importlib


class Render():

    _static_folder: t.Optional[str] = None
    _paths: t.Optional[str] = {}

    def __init__(self, folder) -> None:

        self._static_folder = folder
        for file in os.listdir(self._static_folder):
            if file.endswith(".py") & (not file.startswith("_")):
                path = file.strip(".py")
                filename = self._static_folder + "/" + file+".py"
                self._paths[path] = f"{self._static_folder}/{filename}.index"

    def register(self) -> t.Callable:

        def decorator(res: t.Callable) -> t.ByteString:
            return res

        return decorator

    def get_field_value(self, data, field):

        split_fields = field.split(".")
        field_value = data
        for f in split_fields:
            field_value = field_value[f]
        return field_value

    def hydrate_variable(self, html, data, keyword="${"):
        html_start = 0
        html_end = len(html)
        done = True
        while done:
            data_field_start = html.find(keyword, html_start, html_end)

            if data_field_start == -1:
                done = False
                break

            data_entry_start = data_field_start + len(keyword)
            data_field_end = html.find("}", data_entry_start, html_end)
            data_entry_end = data_field_end + 1

            field = html[data_entry_start:data_field_end]
            field_value = self.get_field_value(data, field)

            value_to_be_replaced = html[data_field_start:data_entry_end]
            html = html.replace(value_to_be_replaced, field_value)

        return html

    def hydrate_for_statement(self, html, data):
        html_start = 0
        html_end = len(html)
        done = True
        while done:
            for_statement_start = html.find("{for")
            if for_statement_start == -1:
                done = False
                break
            for_statement_end = html.find("end}")+4
            html_subset = html[for_statement_start:for_statement_end]

            iterator_name = re.search(
                "(?<=for\s).*(?=\sin)", html_subset).group()
            iterator_item = re.search("(?<=in\s).*(?=\})", html_subset).group()

            iterator_content_start = html_subset.find("}")+1
            iterator_content_end = html_subset.find("{end")
            html_content = html_subset[iterator_content_start:iterator_content_end]
            html_content = html_content.replace(iterator_name+".", "")

            content_data = data[iterator_item]

            print("html_content: ", html_content)
            for_statement_block = ""
            for content in content_data:
                print("content: ", content)
                html_ouput = self.hydrate_variable(
                    html_content, content, "{")
                for_statement_block = for_statement_block + html_ouput + " \n"
            print("for_statement_block: ", for_statement_block)
            html = html.replace(html_subset, for_statement_block)

        return html

    def hydrate_data(self, html, data):
        html = self.hydrate_variable(html, data)
        html = self.hydrate_for_statement(html, data)
        return html

    def wrap_html(self, html):
        file_path = self._static_folder + "/index.html"
        f = open(file_path)
        index_html = f.read()
        index_html = index_html.replace('<div id="app"></div>', html)

        return index_html

    def go(self):
        index_path = self._paths["server"]
        spec = importlib.util.spec_from_file_location(
            "index", "sources/server.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        html = mod.index()
        data = mod.data()
        html = self.hydrate_data(html, data)
        return self.wrap_html(html)
