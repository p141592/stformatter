from marshmallow import fields, Schema

class BaseNodeDBSerializator(Schema):
    id = fields.UUID()
    type = fields.String() # Тип объекта строкой
    format_sign = fields.Boolean(allow_none=True) # Признак формата в строке Boolean
    parent = fields.Method("get_parent", deserialize="load_parent", allow_none=True) # ForeignKey на родителя объекта
    position = fields.Integer() # Позиция в списке children у родителя
    path = fields.String(allow_none=True) # Полный путь до файла
    filename = fields.String(allow_none=True) # Название файла
    line_number = fields.Integer(allow_none=True) # Номер строки
    content = fields.String(allow_none=True) # Содержит исходную строку целиком

    def get_parent(self, obj):
        return obj.parent.id

    def load_parent(self, value):
        return value
