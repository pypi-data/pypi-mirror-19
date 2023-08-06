import boto3
import json
import decimal
from botocore.exceptions import ClientError
from pyjstore.exception import DSInvalidInputException, DSNotFoundException, DSInvalidKeyException

__all__ = ['JsonStore']


class _DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(_DecimalEncoder, self).default(o)


class JsonStore:
    _db = boto3.resource('dynamodb')
    _table_repository = {}

    @classmethod
    def put(cls, table, primary_key, data, key_map=None):
        model = cls._register_table(table)
        if key_map is None:
            if primary_key is None:
                raise DSInvalidKeyException()
            key_map = {
                'id': primary_key
            }
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
            return json.dumps(model.put_item(Item=data), cls=_DecimalEncoder)
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
            ), cls=_DecimalEncoder)

    @classmethod
    def get(cls, table, primary_key, attributes=None):
        model = cls._register_table(table)
        try:
            response = model.get_item(
                Key={
                    'id': primary_key
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        else:
            if 'Item' in response:
                item = response['Item']
                if attributes is None:
                    return json.dumps(item, cls=_DecimalEncoder)
                else:
                    data = {}
                    for key in attributes:
                        if key in item:
                            data[key] = item[key]
                    return json.dumps(data, cls=_DecimalEncoder)
            else:
                raise DSNotFoundException()

    @classmethod
    def _register_table(cls, table):
        model = cls._table_repository[table] if table in cls._table_repository else None
        if model is None:
            model = cls._db.Table(table)
            cls._table_repository[table] = model
        return model
