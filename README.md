# Argon challenge


## Init

### Frontend

```
npm i
npm run dev
```

### Backend

Configure `venv`
```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
```
pip install -r requirements.txt
python app.py
```

### Dataset

GitHub has a file limit of 100MB so the JSON dataset must be downloaded here `https://drive.google.com/file/d/1SmZ7j0aCrX71Qxjj-Ne_qsMkBLCuXFmT/view?usp=sharing` and added to the root of the backend directory `argon_challenge_backend/ctg-studies.json`.


## Project

Enable the user to search through a medical trial database using keywords and synonyms. This project requires a list of synonyms for different conditions then adds matches for each to the results list.


## Future work

*How do we allow her to search for NSCLC trials -AND- immunotherapy related drugs?*
We can repeat the process on the backend with an additional keyword related to treatments. Each treatment will similarly include a list of synonyms for it. As the backend process iterates through the list of trials, it only includes those that mention both the disease as well as the therapy.

*How would you deploy your software?*
The use of standard tools and decoupling of the frontend and backend API service enable a number of options for hosting. A simple option would be to host the Flask service on AWS Elastic Beanstalk or even as serverless Lambda functions. The frontend could be hosted on Vercel's hosting platform for straightforward developer experience and strong CD integrations, or alternatively on AWS Cloudfront with S3.

*What are the alternatives to loading the dataset into memory, and why would you want to use those alternatives?*
As the dataset grows, a traditional relational database like PostgreSQL or a NoSQL alternative like MongoDB will prove more scalable and performant. Even more, Elasticsearch would be a great choice not just for scalability, but also for synonym-based and fuzzy search as well as search ranking features.

*How do we evaluate completeness of results?*
A number of approaches should be used in combination to evaluate completeness. First, a baseline dataset could be created to measure return values against. Second, we can measure both the relevance of returned trials as well as how many relevant trials are returned. This way we can ensure that the results are both high quality and not missing important trials. This could happen in the case of a missing synonym or a normalization misconfiguration, for example. Lastly, user feedback can be incorporated where in-house testers or real-world users can evaluate the usefulness of the results. This could be incorporated with simple UI elements like upvotes or input fields to request missing trials.
