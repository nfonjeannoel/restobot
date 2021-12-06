import datetime
import json

import boto3
import os


def add_to_aws(file_name, save_store):
    # remember to change file name to the json you want

    s3 = boto3.resource('s3', aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxx",
                        aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxadded menu variations")
    s3object = s3.Object('tw-external-dumps1',
                         f"opentable/canada/{str(datetime.datetime.utcnow().isocalendar()[0]) + '-' + str(datetime.datetime.utcnow().isocalendar()[1])}/{file_name.split('/')[-1]}.json")
    s3object.put(
        Body=(bytes(json.dumps(save_store).encode('UTF-8'))))


if __name__ == '__main__':
    for file in os.listdir():
        if '.json' in file:
            add_to_aws(str(file), file)
