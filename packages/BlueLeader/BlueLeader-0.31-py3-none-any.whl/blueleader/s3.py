import os
import boto3

class S3Manager(object):
    def __init__(self,
                 aws_region,
                 destination_bucket,
                 destination_folder,
                 local_static_folder,
                 aws_profile):

        self._aws_region = aws_region
        self._destination_bucket = destination_bucket
        self._destination_folder = destination_folder
        self._local_static_folder = local_static_folder
        
        session = boto3.Session(profile_name=aws_profile,
                                region_name=aws_region)
        self._s3_client = session.client('s3')
        
    def upload_static(self, ignore=[]):
        """
        Upload local static assets from `local_static_folder` to 
        `destination_bucket`/`destination_folder`
        """
        # Iterate through and upload files
        for filename in os.listdir(self._local_static_folder):
            filepath = self._local_static_folder + filename
            if filename in ignore:
                print("Skipping file %s" % filename)
                continue
            else:
                print("Uploading static asset %s" % filename)
            key = self._destination_folder + "/" + filename
            self.upload_file(filepath, key)

    def update_static_routes(self, template_file, output_file, mapping):
        """
        Update all static routes in a given file, using mapping.

        Example:
        if mapping = {"bundle_url": "main-ec1246.js"} 
        then we'll transform {bundle_url} into 
          https://s3-us-west-1.amazonaws.com/bucket/folder/main-ec1246.js
        """
        # Generate and upload new index file referencing bundle
        with open(template_file, 'r') as fp:
            template = fp.read()
            rendered = template
            for item in mapping:
                item_url = "https://s3-%s.amazonaws.com/%s/%s/%s" %\
                             (self._aws_region,
                              self._destination_bucket,
                              self._destination_folder,
                              mapping[item])
                rendered = template.replace("{%s}" % item, item_url)
            with open(output_file, 'w') as fp:
                fp.write(rendered)

    def upload_file(self, local_file, key, ExtraArgs=None):
        self._s3_client.upload_file(local_file,
                                    self._destination_bucket,
                                    key,
                                    ExtraArgs=ExtraArgs
        )
        self._s3_client.put_object_acl(ACL='public-read',
                                       Bucket=self._destination_bucket,
                                       Key=key)
