### Installation of dependencies
Install and create a virtual environment from `requirement.txt`. Ensure your python version is 3.11

Run the following command

```
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

### Activating watsonx Orchestrate environment
Assuming your are running watsonx Orchestrate on AWS Cloud (Saas),
Please get your credentials from ![alt text](images/image.png)
```
orchestrate env list
orchestrate env add -n trial-env -u <Service instance URL>
orchestrate env activate trial-env
(Then enter API Key)
```
https://developer.watson-orchestrate.ibm.com/environment/production_import