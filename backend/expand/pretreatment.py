import pandas as pd
import json

from werkzeug.datastructures.file_storage import FileStorage


def load_execl(file_path:FileStorage) -> list:
    # Load Excel file
    excel_data = pd.read_excel(file_path, sheet_name="数据资源信息")

    # Convert the DataFrame to JSON format
    json_data = excel_data.to_json(orient='records', force_ascii=False)

    # Convert the JSON string to UTF-8 bytes
    utf8_encoded_json_data = json_data.encode('utf-8')

    # If you need to print it as a string
    utf8_encoded_json_str = utf8_encoded_json_data.decode('utf-8')

    # Convert the JSON string to a list of dictionaries
    data_list = json.loads(utf8_encoded_json_str)

    return data_list