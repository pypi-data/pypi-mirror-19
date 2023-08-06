# RichPackager
Python package suite to ship with standard package (built by Setuptools), project data files, offline dependence and others.


### Advantage
Pack your whole python project offline.

Usually there're not only code but many data like htmls or dependences needed for running in your project. 
This suite is a single script to package your code, pip dependences and others offline, then deploy it with creating virtualenv to make every thing One-Click to run.

### How to pack
1. make an dir named 'requirements_info'.
2. put your pypi requirements.txt into requirements_pypi.txt.
3. put dev package link (Support git, hg, svn, or bzr) requirements.txt into requirements_dev_release.txt; And put dev package name/ver into requirements_release.txt.
4. mark files or dirs that you want to pack and app category in the rich_package.json. 
5. make sure all things mentioned before are included and commited in your VCS path(Now only support svn.).
6. then run 
```
python rich_packager.py p -p /user/bin/python3 -l http://to.package.com/proj_to_package

```
to pack your whole project. The script will download all pip package and make everything offline.
7.the dist is in ./rich_dist_center/{{ app_category }}/xx.rich

### How to deploy
run 
```
python rich_packager.py p -p /user/bin/python3 -l http://to.package.com/proj_to_package

```
to unpack and deploy dist to the according path. Then use {{ deploy path}}/venv/bin/python to run your code.


###Usage
```
usage: rich_packager.py [-h] -p PYTHON_PATH [-l VCS_PATH] [-tp DIST_PATH]
                        [-dp DEPLOY_PATH]
                        {p,d}

Rich dist Packager!

positional arguments:
  {p,d}                 Select run mode.

optional arguments:
  -h, --help            show this help message and exit
  -p PYTHON_PATH, --python_path PYTHON_PATH
                        Python Interpreter path.
  -l VCS_PATH, --vcs_path VCS_PATH
                        VCS path to fetch.
  -tp DIST_PATH, --dist_path DIST_PATH
                        Dist path.
  -dp DEPLOY_PATH, --deploy_path DEPLOY_PATH
                        Path to deploy dist to.
```

