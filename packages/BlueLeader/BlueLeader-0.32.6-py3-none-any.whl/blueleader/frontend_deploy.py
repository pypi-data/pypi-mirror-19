import boto3
import os
import json
import argparse
import subprocess
import WebpackManager from webpack

"""
Frontend deployment script. 
usage: frontend_deploy.py [-h] (--production | --dev)

- Generates a webpack config, setting the publicPath appropriately

- Runs webpack on the generated config.

- Uploads local static assets from `local_static_folder` to 
  `destination_bucket`/`destination_folder`, excluding all generated
  javascript bundles except the current one.

- Updates index.html in the given s3 bucket, generating index.html from 
a templated index file given the current bundle name and location.
"""

# Settings
region = "us-west-1"
webpack_config_template = 'webpack-config.prod.js.template'
prod_destination_bucket = "signal-static-assets"
dev_destination_bucket = "signal-static-assets-dev"
destination_folder = "static"
local_static_folder = "./static/bundles/"



def upload_static(s3_client, local_static_folder, current_bundle,
                  destination_folder, destination_bucket):
    """
    Upload local static assets from `local_static_folder` to 
    `destination_bucket`/`destination_folder`, excluding all generated
    javascript bundles except the current one.
    """
    # Iterate through and upload files
    for filename in os.listdir(local_static_folder):
        filepath = local_static_folder + filename
        if "main-" in filename and ".js" in filename:
            if filename != current_bundle:
                print("Skipping old bundle %s" % filename)
                continue
            else:
                print("Uploading current bundle %s" % filename)
        else:
            print("Uploading static asset "+filename)
        key = destination_folder + "/" + filename
        s3_client.upload_file(filepath, destination_bucket, key)
        s3_client.put_object_acl(ACL='public-read', Bucket=destination_bucket, Key=key)


def update_index(s3_client, region, destination_bucket,
                 destination_folder, current_bundle):
    """
    Update index.html in the given s3 bucket, by replacing {bundle_url}
    in index.html.out with the URL of the current bundle.
    """
    # Generate and upload new index file referencing bundle
    with open('index.html.template', 'r') as fp:
        template = fp.read()
        bundle_url = "https://s3-%s.amazonaws.com/%s/%s/%s" %\
                     (region, destination_bucket, destination_folder, current_bundle)
        rendered = template.replace("{bundle_url}", bundle_url)
        with open('index.html.out', 'w') as fp:
            fp.write(rendered)
        s3_client.upload_file("./index.html.out", destination_bucket, "index.html", ExtraArgs={'ContentType': 'text/html'})
        s3_client.put_object_acl(ACL='public-read', Bucket=destination_bucket, Key="index.html")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--production", help="Build and deploy to production", action="store_true")
    group.add_argument("--dev", help="Build and deploy to dev servers", action="store_true")
    args = parser.parse_args()

    # Configure AWS client
    session = boto3.Session(profile_name="signal",
                            region_name=region)
    s3_client = session.client('s3')

    # Determine our destination bucket
    destination_bucket = None
    if args.production is True:
        print("Deploying for production...")
        destination_bucket = prod_destination_bucket
    elif args.dev is True:
        print("Deploying for development...")
        destination_bucket = dev_destination_bucket
    else:
        raise Exception("Neither production nor dev flags set")

    webpack = WebpackManager(webpack_config_template,
                             public_path = ("https://s3-%s.amazonaws.com/%s/%s/" %\
                                            (region, destination_bucket, destination_folder)))
                             
    # Generate webpack config, run webpack and gather stats
    webpack.generate_webpack_config()
    print("================ Running Webpack =================")
    res = webpack.run_webpack()
    print(res)
    print("==================================================")
    current_bundle = webpack.current_bundle()

    # Upload files to S3
    upload_static(s3_client, local_static_folder, current_bundle,
                  destination_folder, destination_bucket)
    update_index(s3_client, region, destination_bucket,
                 destination_folder, current_bundle)
    
if __name__ == '__main__':
    main()
