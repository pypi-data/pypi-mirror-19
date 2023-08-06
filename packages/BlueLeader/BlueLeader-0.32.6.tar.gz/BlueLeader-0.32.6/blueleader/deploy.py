import boto3
import os
import json
import argparse
import subprocess
import shutil
from blueleader.webpack import WebpackManager
from blueleader.s3 import S3Manager

"""
Frontend deployment script. 
usage: deploy.py [-h] (--production | --dev) config.json

- Generates a webpack config, setting the publicPath appropriately

- Runs webpack on the generated config.

- Uploads local static assets from `local_static_folder` to 
  `destination_bucket`/`destination_folder`, excluding all generated
  javascript bundles except the current one.

- Updates index.html in the given s3 bucket, generating index.html from 
a templated index file given the current bundle name and location.
"""

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--production", help="Build and deploy to production", action="store_true")
    group.add_argument("--dev", help="Build and deploy to dev servers", action="store_true")
    group.add_argument("--local", help="Build but don't deploy.", action="store_true")
    parser.add_argument('config_file', help="A blue leader JSON config file")
    args = parser.parse_args()

    config = None
    with open(args.config_file, 'r') as fp:
        config = json.load(fp)

    required = ['region',
                'webpack_config_template',
                'local_webpack_config_template',
                'local_public_path',
                'source_directory',
                'prod_destination_bucket',
                'dev_destination_bucket',
                'destination_folder',
                'local_static_folder',
                'aws_profile']

    for k in required:
        if k not in config:
            raise Exception("Required config paramter %s not in config file %s" % (k, args.config_file))
        
    # Determine our destination bucket and public path
    destination_bucket = None
    public_path = "https://s3-%s.amazonaws.com/%s/%s/" %\
                                            (config['region'],
                                             destination_bucket,
                                             config['destination_folder'])
    webpack_template = config['webpack_config_template']

    if args.production is True:
        print("Deploying for production...")
        config['deploy_mode'] = "production"        
        destination_bucket = config['prod_destination_bucket']
        if "prod_public_path" in config:
            public_path = config["prod_public_path"]
    elif args.dev is True:
        print("Deploying for development...")
        config['deploy_mode'] = "dev"        
        destination_bucket = config['dev_destination_bucket']
        if "dev_public_path" in config:
            public_path = config["dev_public_path"]
    elif args.local is True:
        print("Building locally")
        config['deploy_mode'] = "local"
        public_path = config['local_public_path']            
        webpack_template = config['local_webpack_config_template']            
    else:
        raise Exception("Neither production, dev, nor local flags set")

    print("All assets will reference the static URI: %s" % public_path)

    # Store config in a javascript file accessible to our project
    js_module_file = os.path.join(config['source_directory'], "blueleader.js")
    with open(js_module_file, 'w') as f:
        x = json.dumps(config)
        f.write("export default %s" %x)
        print("Generated javascript module at %s" % js_module_file)
    
    webpack = WebpackManager(webpack_template,
                             public_path = public_path)

    # Generate webpack config, run webpack and gather stats
    print("================ Running Webpack =================")
    res = webpack.run_webpack()
    print(res)
    print("==================================================")
    current_bundle = webpack.current_bundle()
    print("Current webpack bundle: %s" % current_bundle)
    # Upload generated and static assets to S3
    index_output_file = "index.html.out"
    s3 = S3Manager(config['region'], destination_bucket,
                   config['destination_folder'],
                   config['local_static_folder'],
                   config['aws_profile'],
                   public_path
    )
    s3.update_static_routes("index.html.template", "index.html.out",
                            {"bundle_url": current_bundle})

    if args.local is True:
        print("Local configuration complete. Exiting")
        shutil.copyfile("index.html.out", "index.html")
        exit(1)
    else:
            s3.upload_static()
            s3.upload_file(index_output_file, "index.html",
                           ExtraArgs={'ContentType': "text/html",
                                      'CacheControl': "max-age=60"
                           })
            subprocess.Popen("rm %s" % index_output_file,
                             shell=True,
                             stdout=subprocess.PIPE).stdout.read().decode('utf-8')

if __name__ == '__main__':
    main()
