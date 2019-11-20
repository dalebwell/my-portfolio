import json
import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    location = {
        "bucketName": 'portfoliobuild.solocollab.online',
        "objectKey": 'portfoliobuild.zip'
    }
    job = event.get("CodePipeline.job")
    
    if job:
        for artifact in job["data"]["inputArtifacts"]:
            if artifact["name"] = "BuildArtifact":
                location = artifact["location"]["s3Location"]
                
    print "Building portfolio from " + str(location)
    
    s3 = boto3.resource('s3')

    portfolio_bucket = s3.Bucket('portfolio.solocollab.online')
    build_bucket = s3.Bucket(location["bucketName"])

    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    
    print "Job done"
    
    if job:
        codepipeline = boto3.client('codepipeline')
        coddepioeline.put_job_success_result(jobId=job["id"])