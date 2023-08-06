import os
import json
import subprocess

class WebpackManager(object):
    def __init__(self,
                 webpack_config_template,
                 public_path,
                 stats_file = "webpack-stats.json"):
        self._webpack_config_template = webpack_config_template
        self._public_path = public_path
        self._outfile = "generated-webpack-config.out"
        self._stats_file = stats_file

    def current_bundle(self):
        """
        Returns the name of the current javascript bundle
        """
        stats = self._webpack_stats()
        return stats['chunks']['main'][0]['name']

    def _generate_webpack_config(self):
        """
        Generate a webpack config from a template, replacing variables as necessary
        - {public_path}: Replaced with the given public path for static assests (CDN etc)
        """
        config = ""
        with open(self._webpack_config_template, 'r') as fp:
            config = fp.read()
            
        replace = {"public_path": self._public_path}
        for k in replace:
            config = config.replace("{%s}" % k, replace[k])
        
        with open(self._outfile, 'w') as fp:
            return fp.write(config)

    def run_webpack(self):
        """
        Run webpack using the given config file
        """
        self._generate_webpack_config()
        res = subprocess.Popen("webpack --config %s" % self._outfile,
                                shell=True,
                                stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        subprocess.Popen("rm %s" % self._outfile,
                                shell=True,
                                stdout=subprocess.PIPE).stdout.read().decode('utf-8')        
        return res

    def _webpack_stats(self):
        """
        Gather information about most recent webpack run
        """
        with open(self._stats_file, 'r') as fp:
            webpack_stats = json.load(fp)
        if webpack_stats['status'] != 'done':
            raise Exception('Webpack did not successfully complete')
        return webpack_stats
        
