import boto3
from datetime import datetime, timedelta

one_month_ago = datetime.now() - timedelta(days=30)
one_month_ago_int = int(one_month_ago.timestamp() * 1000)

logs = boto3.client('logs')

log_groups = logs.describe_log_groups()

for log_group in log_groups['logGroups']:
    log_group_name = log_group['logGroupName']
    log_stream = logs.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=1
            )
    last_event_timestamp = log_stream['logStreams'][0]['lastEventTimestamp']
    
    if last_event_timestamp < one_month_ago_int:
        logs.delete_log_group(logGroupName=log_group_name)
        print(log_group_name  + 'は削除されました。')