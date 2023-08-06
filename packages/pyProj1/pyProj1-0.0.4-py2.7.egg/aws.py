import boto3
client = boto3.client('cloudformation',
    aws_access_key_id='ASIAJVH535O4CXD2PS4Q',
    aws_secret_access_key='OY0Ac8hfSri+2pYTLyARA6RL960tRg9azmS30+Uw',
    aws_session_token='FQoDYXdzENP//////////wEaDIfFuPyu+JZJloRJ9yLgAQud7pwENc/ei8N3K/jObtIhAnGtAlESNJollHwFATIRGterVCF8eFJ5GbCJxfvt0FnfejWY23P/mv1J1CIqI8g/EeR2A1W/NjvhRrnvdMm5VPIYMraSM0BRBk25I2l3lzPBsfxee5zgTMzojHhm+ZtVCCM+se9Qi+9SjQJAlDJ1omOaT8jxNaW/6LfD5nC7tLULkMLQV5w538+R5OISqkZG7DtBHrXxuRSy7pTsqtHxgO7AMTsTwbubC5G0x22Dx+hKJc8wzW5s0xcbDuUHzgaBL0qheZcfAqSgOvs/LmIhKNDSnMQF',
);
response = client.describe_stacks(
    StackName='BMS-ServiceCatalogTestInfra-dev'
);
output = response['Stacks'][0]['Outputs']
for key in output:
	print key['OutputKey'];
	if key['OutputKey'] == 'EBCustomEndpoint':
		print 'value=',key['OutputValue'];