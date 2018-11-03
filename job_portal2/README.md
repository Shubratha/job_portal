# CODE CONSOLE

## Development Instructions

#### 1. Clone repo:

```bash
git clone git@bitbucket.org:codekraftk2/job_portal.git
```

#### 2. cd to `job_portal`

#### 3. Create `job_portal` virtualenv

#### 4. Install requirements within the virtualenv

```bash
pip install -r requirements.txt
pip install -r dev_requirements.txt
```

#### 5. Create `job_portal` database in your MySQL terminal

```bash
mysql -u root
```

```sql
CREATE DATABASE job_portal;
```

#### 6. Exit MySQL and run initial database migrations

```bash
python manage.py migrate
```

#### 7. Start the server!

```bash
python manage runserver
```

