<<<<<<< HEAD
# InsightFL
A basic template for building minimal web applications.

### Introduction
InsightFL is a basic [Flask](http://flask.pocoo.org/) template created specifically to help budding
data scientists in the [Insight Data Science](http://insightdatascience.com/) program get their web applications
off the ground quickly. As a former Insight fellow, I spent way too much time troubleshooting the ins and outs of
web development instead of focusing on what truly mattered, extracting insight from my data.

InsightFL comes with all the necessary tools you'll need to create your web app quickly:

  1. [Twitter Bootstrap](http://getbootstrap.com/) for designing your web pages.
  2. [Bower](http://bower.io/) to easily install third party libraries.
  3. [Reveal.js](http://lab.hakim.se/reveal-js/#/) for creating amazing presentations in HTML.
  4. And its already in version control from the [Git](http://git-scm.com/) go!

To get started building your web app, follow the instructions below to setup your development and production
environments.

### Getting Started <a name="getting-started"></a>
#### System Requirements <a name="system-requirements"></a>
1. [Python](https://www.python.org/downloads/)(v2.7+) with [pip](http://pip.readthedocs.org/en/latest/installing.html) installed.
2. [node](http://nodejs.org/)(v0.10.26+) - make sure to install the packages with [npm](https://www.npmjs.org/): Windows: *.msi*, MacOSX: *.pkg*

#### Dev Environment Setup <a name="environment-setup"></a>
1. Fork the [project](https://github.com/stormpython/insightfl/fork) and clone the repository.

  **Note:** It is helpful to change the repository name **before** cloning. In Github, click on `Settings` on the right-hand
  side of your screen. Within the Settings box at the top of the screen, rename the repository and click `Rename`.

  ```
  git clone git@github.com:<username>/<project>.git
  ```

2. Change into the project directory and install node project dependencies.

  ```
  cd /path/to/project/directory
  npm install
  ```

3. Install virtualenv and fire up a virtual environment.

  ```
  sudo pip install virtualenv
  virtualenv venv
  source venv/bin/activate
  ```

4. Install Python project dependencies.

  ```
  pip install -r requirements.txt
  ```

5. To test your application, run the server.py file: `python server.py`, and open your web browser to
`localhost:5000`.

That's it! You are ready to start coding your project.

### Deploying to AWS

*Note: the setup script assumes you are deploying to an Ubuntu **14.04** Server*

1. Secure copy the setup script (located in the deployment directory) to the remote host.

  ```
  scp -i mykey.pem /path/to/setup.sh ubuntu@ec2-12-345-67-89.us-west-2.compute.amazonaws.com:~
  ```

  where `mykey.pem` is your downloaded key pair from Amazon and `@ec2-12-345-67-89.us-west-2.compute.amazonaws.com`
  is your Amazon EC2 Public DNS.

2. SSH into the remote host and run the setup script. Answer the questions when prompted and wait for
the downloads to finish.

  ```
  ssh -i mykey.pem ubuntu@ec2-12-345-67-89.us-west-2.compute.amazonaws.com
  source setup.sh
  ```

3. Open up a web browser and enter your public DNS: `ec2-12-345-67-89.us-west-2.compute.amazonaws.com`

That's it, you should now have a fully functioning web app!
=======
# Bootstrap Multiselect

Bootstrap Multiselect is a JQuery based plugin to provide an intuitive user interface for using select inputs with the multiple attribute present. Instead of a select a bootstrap button will be shown as dropdown menu containing the single options as checkboxes.

Bootstrap 3 port by [Eduard Dudar](https://github.com/edudar).

## Documentation

Documentation, demonstrations and FAQ: [http://davidstutz.github.com/bootstrap-multiselect/](http://davidstutz.github.com/bootstrap-multiselect/).

**Note**: The demo page is based on JQuery 2 - so for IE 6,7 and 8 the plugin will not work properly. Nevertheless, the plugin should run as expected using the .x branch of jQuery.

## Contribute!

Every pull request is appreciated. To make it easier for me to merge fixes and new features have a look at the following guidelines:

* Include documentation for new options and features to avoid undocumented features.
* Add a thorough description to every pull request - so I am able to understand the purpose of the pull request.
* Have a look at the code as to keep the code as comprehensible and coherent as possible (concerning code style, indentation etc. ...).
* Add comments to your code - to help me understand the committed code.
* Add a single pull request per fix or feature you add.

## License

This project is dual licensed under the Apache License, Version 2.0 and the BSD 3-Clause license.

### Apache License, Version 2.0

Copyright 2012 - 2014 David Stutz

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

### BSD 3-Clause License

Copyright (c) 2012 - 2014 David Stutz
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of the <ORGANIZATION> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
>>>>>>> 7a5590defc606c6ca6a55e5caed28ba051e5f065
