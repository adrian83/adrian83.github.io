[adrian@adrian-pc vpc-infrastructure]$ 
[adrian@adrian-pc vpc-infrastructure]$ aws cloudformation package --template-file main.yml --s3-bucket cloudformation-deployments-bucket --output-template-file packaged.yml

Successfully packaged artifacts and wrote output template to file packaged.yml.
Execute the following command to deploy the packaged template
aws cloudformation deploy --template-file /home/data/work/projects/aws-samples/vpc-infrastructure/packaged.yml --stack-name <YOUR STACK NAME>
[adrian@adrian-pc vpc-infrastructure]$ aws cloudformation deploy --template-file /home/data/work/projects/aws-samples/fargate/packaged.yml --stack-name fargate-demo --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM

Waiting for changeset to be created..
Waiting for stack create/update to complete
Successfully created/updated stack - fargate-demo

