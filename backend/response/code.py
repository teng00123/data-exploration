import json

from flask import jsonify, send_file, make_response, Response, stream_with_context
import io

class SuccessResponse:

    def __init__(self,data=None, message='success',code=200):
        self.data = data
        self.message = message
        self.code = code

    def to_response(self):

        response = {
            "code":self.code,
            "message":self.message,
            "data":self.data
        }
        return jsonify(response)


class ErrorResponse:

    def __init__(self, error_data=None, message='error', code=201):
        self.error_data = error_data
        self.message = message
        self.code = code

    def to_response(self):
        response = {
            "code": self.code,
            "message": self.message,
            "error_data": self.error_data
        }
        return jsonify(response)


class FileResponse:
    def __init__(self, file_path=None, file_content=None, file_type='application/octet-stream', filename='file'):
        """
        初始化文件响应类。

        :param file_path: 文件路径，如果提供，将从这个路径读取文件。
        :param file_content: 文件内容，如果提供，将直接使用这个内容作为文件。
        :param file_type: 文件MIME类型。
        :param filename: 返回给客户端的文件名。
        """
        self.file_path = file_path
        self.file_content = file_content
        self.file_type = file_type
        self.filename = filename

    def to_response(self):
        """
        根据提供的文件路径或文件内容创建响应。

        :return: Flask响应对象。
        """
        if self.file_path:
            # 从文件路径返回文件
            return send_file(self.file_path, mimetype=self.file_type, as_attachment=True, download_name=self.filename)
        elif self.file_content:
            # 从文件内容返回文件
            file_io = io.BytesIO(self.file_content)
            file_io.seek(0)
            return send_file(file_io, mimetype=self.file_type, as_attachment=True, download_name=self.filename)
        else:
            # 没有提供文件路径或内容
            return make_response('No file provided', 400)

class StreamResponse:
    def __init__(self,data=None, message='success',code=200):
        self.data = data
        self.message = message
        self.code = code

    def stream_response(self):
        for chunk in self.data:
            yield json.dumps(chunk) + '\n'

    def to_response(self):
        return Response(stream_with_context(self.stream_response()), content_type='text/plain')