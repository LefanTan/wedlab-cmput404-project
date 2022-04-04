# CMPUT404 Project - Distributed Social Networking
- [Project Details](/project-details.org)
 
The web is fundamentally interconnected and peer to peer. There’s no really great reason why we should all use facebook.com or google+ or myspace or something like that. If these social networks came up with an API you could probably link between them and use the social network you wanted. Furthermore you might gain some autonomy.

Thus in the spirit of diaspora https://diasporafoundation.org/ we want to build something like diaspora but far far simpler.

This blogging/social network platform will allow the importing of other sources of posts (github, twitter, etc.) as well allow the distributing sharing of posts and content.

## Heroku Deployment (Active)
> [cmput404-project-w22.herokuapp.com](https://cmput404-project-w22.herokuapp.com)
>  - Approved Login Credentials for Public:
>    - Username: `team02user`
>    - Password: `user`
#### Web Service API Endpoint
- [cmput404-project-w22.herokuapp.com/service](https://cmput404-project-w22.herokuapp.com/service)
#### API Endpoints Documentation
- [cmput404-project-w22.herokuapp.com/service/docs](https://cmput404-project-w22.herokuapp.com/service/docs)
#### Example HTTPIE command for authenticated get authors
- `http --auth team02admin:admin GET https://cmput404-project-w22.herokuapp.com/service/authors/`

## Local Deployment
#### Instructions
1. `git clone` this repo
2. `cd wedlab-cmput404-project` to navigate to the project folder
3. Create a python virtual environment in the project folder and activate the environment
4. Run `pip install -r requirements.txt` to install project package dependencies
5. Install [Docker engine](https://docs.docker.com/engine/install/)
6. Run `docker-compose up` to spin up your local postgres server. If you want to access the database from a database browser, here is the details:
   - Host: localhost
   - Port: 5432
   - Database: postgres
   - Username: admin
   - Password: root
6. Run `python manage.py migrate` to apply migration to the postgres server
7. Create a copy of the `.env.example` and name it `.env`. Then: 
   - Add a secret key (for example `SECRET_KEY = *`)
   - Change `USE_AWS_S3_MEDIA` to `false`
   - If you want to test locally but use the heroku postgres server instead of the above local docker postgres server, change `TEST` to `true`
8. Create superuser:
   - Local: Run `python manage.py create_admin`
   - Heroku: Run `heroku run -a cmput404-project-w22 python manage.py create_admin` 
9. Run `heroku local` for non window user to start the server. Access it at `http://localhost:8000`
   - Window doesn't support gunicorn so you'll have to do `heroku local -f Procfile.window` 
10. All the sign ups need to be approved by the superuser through admin panel before any login attempt
11. Credentials of superuser for accessing `http://localhost:8000/admin`:
    - Username: `team02admin`
    - Password: `admin`

## Contributors

| Name                  | GitHub                                                  |
| --------------------- | ------------------------------------------------------- |
| Jia Hui Tan (Lefan)   | [Jia Hui Tan](https://github.com/LefanTan)      |
| Sandip Saha Joy       | [Sandip Saha Joy](https://github.com/sandipsahajoy)    |
| Lewis Ning            | [Lewis Ning](https://github.com/lewisning)              |
| Chen Xu               | [Chen Xu](https://github.com/Chen74)                    |

## License

- [License Details](/LICENSE.md)

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   Copyright 2022 [Jia Hui Tan] [Sandip Saha Joy] [Lewis Ning] [Chen Xu]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   ```
