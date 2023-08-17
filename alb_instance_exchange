import boto3
import json
import time

elbv2_client = boto3.client('elbv2')
ec2_client = boto3.client('ec2')
instance_id1 = '1台目のインスタンスID'
instance_id2 = '2台目のインスタンスID' 
target_group_arn = 'ターゲットグループのARN'

def lambda_handler(event, context):
    Message = json.loads(event['Records'][0]['Sns']['Message'])
    deregister_instance_id = Message['Trigger']['Dimensions'][0]['value']

    # アラートになったのが1台目のEC2の場合の処理
    if deregister_instance_id == instance_id1:
        elbv2_client.deregister_targets(
            TargetGroupArn=target_group_arn,
            Targets=[
                {
                    'Id': deregister_instance_id,
                },
            ]
        )

        # 2台目のインスタンスを起動
        ec2_client.start_instances(
            InstanceIds=[instance_id2]
        )

        # 2台目のインスタンスが起動するまで無限ループさせる
        while True:
            time.sleep(3)
            response = ec2_client.describe_instance_status(
                InstanceIds=[instance_id2]
            )
            if len(response['InstanceStatuses']) > 0:
                instance_status = response['InstanceStatuses'][0]['InstanceState']['Name']
                if instance_status == 'running':
                    break

        # ターゲットグループへアタッチ
        elbv2_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[
                {
                    'Id': instance_id2,
                },
            ]
        )

        # 1台目のインスタンスを停止
        ec2_client.stop_instances(
            InstanceIds=[deregister_instance_id]
        )

    # アラートになったのが2台目のEC2の場合の処理
    else:
        elbv2_client.deregister_targets(
            TargetGroupArn=target_group_arn,
            Targets=[
                {
                    'Id': deregister_instance_id,
                },
            ]
        )

        # 1台目のインスタンスを起動
        ec2_client.start_instances(
            InstanceIds=[instance_id1]
        )

        # 2台目のインスタンスが起動するまで無限ループさせる
        while True:
            time.sleep(3)
            response = ec2_client.describe_instance_status(
                InstanceIds=[instance_id1]
            )
            if len(response['InstanceStatuses']) > 0:
                instance_status = response['InstanceStatuses'][0]['InstanceState']['Name']
                if instance_status == 'running':
                    break

         # ターゲットグループへアタッチ
        elbv2_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[
                {
                    'Id': instance_id1,
                },
            ]
        )

        # 2台目のインスタンスを停止
        ec2_client.stop_instances(
            InstanceIds=[deregister_instance_id]
        )
