import boto3
import json
import iso8601
import decimal
import datetime
from botocore.exceptions import ClientError
from pyjstore.exception import DSInvalidInputException, DSNotFoundException, DSInvalidKeyException

__all__ = ['DynamoClient']


class _DefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        elif isinstance(o, bytes):
            return o.decode("utf-8")
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        elif isinstance(o, datetime.date):
            return iso8601.parse_date(o)
        elif isinstance(o, datetime.time):
            return o.isoformat()
        return super(_DefaultEncoder, self).default(o)


class DynamoClient:
    _db = boto3.resource('dynamodb')
    _table_repository = {}

    @classmethod
    def put(cls, table, data, key_map, encoder=None):
        model = cls._register_table(table)
        if key_map is None:
            raise DSInvalidKeyException()
        try:
            response = model.get_item(
                Key=key_map
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        else:
            stored_data = response['Item'] if 'Item' in response else None

        if stored_data is None:
            return json.dumps(model.put_item(Item=data), cls=encoder if encoder else _DefaultEncoder)
        else:
            expression = list()
            expression_attribute_values = {}
            for key, value in data.items():
                if key not in key_map:
                    expression.append(key + '= :' + key + ',')
                    expression_attribute_values[':' + key] = value
            if len(expression) < 1:
                raise DSInvalidInputException("provide at-least one attribute to update")
            expression = 'set ' + ''.join(expression)[:-1]
            return json.dumps(model.update_item(
                Key=key_map,
                UpdateExpression=expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            ), cls=encoder if encoder else _DefaultEncoder)

    @classmethod
    def get(cls, table, key_map, attributes=None, encoder=None):
        if key_map is None:
            raise DSInvalidKeyException()
        model = cls._register_table(table)
        try:
            response = model.get_item(
                Key=key_map
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        else:
            if 'Item' in response:
                item = response['Item']
                if attributes is None:
                    return json.dumps(item, cls=encoder if encoder else _DefaultEncoder)
                else:
                    data = {}
                    for key in attributes:
                        if key in item:
                            data[key] = item[key]
                    return json.dumps(data, cls=encoder if encoder else _DefaultEncoder)
            else:
                raise DSNotFoundException()

    @classmethod
    def get_in_batch(cls, request_items, encoder=None):
        try:
            response = cls._db.batch_get_item(
                RequestItems=request_items
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        else:
            return json.dumps(response['Responses'], cls=encoder if encoder else _DefaultEncoder)

    @classmethod
    def get_in_batch_from_table(cls, table, key_maps, encoder=None):
        if key_maps is None:
            raise DSInvalidKeyException()
        try:
            response = cls._db.batch_get_item(
                RequestItems={
                    table: {
                        'Keys': key_maps
                    }
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        else:
            return json.dumps(response['Responses'][table], cls=encoder if encoder else _DefaultEncoder)

    @classmethod
    def _register_table(cls, table):
        model = cls._table_repository[table] if table in cls._table_repository else None
        if model is None:
            model = cls._db.Table(table)
            cls._table_repository[table] = model
        return model
