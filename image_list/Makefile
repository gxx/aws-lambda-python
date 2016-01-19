ACCOUNT_ID = 111111111111
ROLE_NAME = lambda_role
FUNCTION_NAME = ListImage
REGION = us-west-1
TIMEOUT = 15
MEMORY_SIZE = 512
ZIPFILE_NAME = list_image.zip
HANDLER = handler.handle_list_image

clean_pyc :
	find . | grep .pyc$ | xargs rm

install_deps :
	pip install -r requirements.txt -t .

build : install_deps clean_pyc
	zip $(ZIPFILE_NAME) -r *

create : build
	aws lambda create-function --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --role arn:aws:iam::$(ACCOUNT_ID):role/$(ROLE_NAME)  --handler $(HANDLER) --runtime python2.7 --timeout $(TIMEOUT) --memory-size $(MEMORY_SIZE)

update : build
	aws lambda update-function-code --region $(REGION) --function-name $(FUNCTION_NAME) --zip-file fileb://$(ZIPFILE_NAME) --publish
