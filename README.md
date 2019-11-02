# nuveo-awesome-api
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/mdcg/nuveo-awesome-api/blob/master/LICENSE)

## Introduction

First of all, I would like to thank Nuveo for the opportunity to show some of my work, then THANK YOU SO MUCH! Next I will talk about the technologies I have chosen for this project, as well as some architectural decisions.

## Stack

The technologies used in this project are:

- Docker;
- Docker Compose;
- Django;
- PostgreSQL;
- Redis;

Why use Docker? Because, Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package. By doing so, thanks to the container, the developer can rest assured that the application will run on any other Linux machine regardless of any customized settings that machine might have that could differ from the machine used for writing and testing the code.

The entire application is already configured to run in the Docker container. For that reason, I suggest you have Docker and Docker Compose installed on your machine.

To install them, just click on the links below:

- [Install Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

Why use Redis? Because it is simple. *Simple is better than complex*.

## Architectural Decisions

### JSON Responses

[JSend](https://github.com/omniti-labs/jsend) is a specification that lays down some rules for how JSON responses from web servers should be formatted. JSend focuses on application-level (as opposed to protocol- or transport-level) messaging which makes it ideal for use in REST-style applications and APIs. There are lots of web services out there providing JSON data, and each has its own way of formatting responses. Also, developers writing for JavaScript? front-ends continually re-invent the wheel on communicating data from their servers. While there are many common patterns for structuring this data, there is no consistency in things like naming or types of responses. Also, this helps promote happiness and unity between backend developers and frontend designers, as everyone can come to expect a common approach to interacting with one another.

You can read more about this pattern by clicking [here](https://github.com/omniti-labs/jsend).

### Authentication

To create and consume workflows, the user must be authenticated. That way we can know who created the workflow and who consumed it. For this project, I chose to use JWT authentication.

### JSON to CSV

To handle the JSON to CSV conversion, the logic I used was to "flatten" as follows:

```javascript
"data": {
	"test": {
		"foo": "bar",
		"lorem": "ipsum",
		"buzz": "fizz"
	},
	"test_flatten": {
		"ultricies": {
			"consectetur": "adipiscing"
		},
		"dolor": "sit"
	}
}
```

Will become:

```csv
test__foo,test__buzz,test__lorem,test_flatten__dolor,test_flatten__ultricies__consectetur
bar,fizz,ipsum,sit,adipiscing
```

## First steps

Now that I have explained the architectural decisions of the project a bit, let's work!

Initially we need to set our environment variables. To do this, go to the `config` folder of the project root directory and run the following command:

```shell
cp .env-example .env
```

After we create our `.env` file we will start Docker. Make sure you have installed [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [Docker Compose](https://docs.docker.com/compose/install/) on your machine.

In the project root folder, where the `Dockerfile` and `docker-compose.yml` files are located, run the following command:

```shell
$ docker-compose up
```

***PS: Keep in mind that for many Docker and Docker Compose commands, you need to give 'sudo' privileges. If the above command does not work, add 'sudo' and try again.***

It should take a while for the container build, so have a little patience. If everything goes well, you'll see a response on your terminal much like this:

```shell
Starting nuveo-awesome-api_redis_1   ... done
Starting nuveo-awesome-api_db_1    ... done
Starting nuveo-awesome-api_web-dev_1 ... done
Attaching to nuveo-awesome-api_db_1, nuveo-awesome-api_redis_1, nuveo-awesome-api_web-dev_1
db_1       | LOG:  database system was shut down at 2019-11-02 05:47:57 UTC
redis_1    | 1:C 02 Nov 2019 05:47:59.702 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis_1    | 1:C 02 Nov 2019 05:47:59.702 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=1, just started
redis_1    | 1:C 02 Nov 2019 05:47:59.702 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
web-dev_1  | Python 3.6.9
db_1       | LOG:  MultiXact member wraparound protections are now enabled
redis_1    | 1:M 02 Nov 2019 05:47:59.707 * Increased maximum number of open files to 10032 (it was originally set to 1024).
redis_1    | 1:M 02 Nov 2019 05:47:59.708 * Running mode=standalone, port=6379.
redis_1    | 1:M 02 Nov 2019 05:47:59.708 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
redis_1    | 1:M 02 Nov 2019 05:47:59.708 # Server initialized
redis_1    | 1:M 02 Nov 2019 05:47:59.708 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis_1    | 1:M 02 Nov 2019 05:47:59.708 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
redis_1    | 1:M 02 Nov 2019 05:47:59.708 * DB loaded from disk: 0.000 seconds
redis_1    | 1:M 02 Nov 2019 05:47:59.708 * Ready to accept connections
db_1       | LOG:  database system is ready to accept connections
db_1       | LOG:  autovacuum launcher started
web-dev_1  | No changes detected
web-dev_1  | No changes detected in app 'api'
web-dev_1  | Operations to perform:
web-dev_1  |   Apply all migrations: admin, api, auth, contenttypes, sessions
web-dev_1  | Running migrations:
web-dev_1  |   No migrations to apply.
web-dev_1  | Watching for file changes with StatReloader
web-dev_1  | Performing system checks...
web-dev_1  | 
web-dev_1  | System check identified no issues (0 silenced).
web-dev_1  | November 02, 2019 - 05:48:13
web-dev_1  | Django version 2.2.6, using settings 'core.settings'
web-dev_1  | Starting development server at http://0.0.0.0:8000/
web-dev_1  | Quit the server with CONTROL-C.
```

Now that we have everything configured and our server is running, we can finally test our application.

## Routes

The full documentation is published in Postman. You can see it by clicking [here](https://documenter.getpostman.com/view/1977265/SW132JSa?version=latest). If you want something faster, please keep reading.

### Signup (POST)
`http://localhost:8000/api/v0/signup`

Request example:

```shell
curl --location --request POST "http://localhost:8000/api/v0/signup" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --form "first_name=Mauro" \
  --form "last_name=de Carvalho" \
  --form "username=mdcg" \
  --form "password=123456" \
  --form "email=mauro@python.com"
```

Response example:

```javascript
{
    "status": "success",
    "data": {
        "user": {
            "username": "mdcg",
            "email": "mauro@python.com",
            "first_name": "Mauro",
            "last_name": "de Carvalho",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3NjE2NzEsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.iy1B_j1QW1TbVlW9LAcCr-rOuqI18f0qMKklM486CSo"
        }
    }
}
```

### Signin (POST)
`http://localhost:8000/api/v0/signin` 

Request example:

```shell
curl --location --request POST "http://localhost:8000/api/v0/signin" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --form "username=mdcg" \
  --form "password=123456"
```

Response example:

```javascript
{
    "status": "success",
    "data": {
        "user": {
            "username": "mdcg",
            "email": "mauro@python.com",
            "first_name": "Mauro",
            "last_name": "de Carvalho",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3NjE2OTMsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.FamV6N8Xwhq71ui-rKJi4CUWg1KHs4SLNypm28QMXls"
        }
    }
}
```

### Create a workflow (POST)
`http://localhost:8000/api/v0/workflow`

Request example:

```shell
curl --location --request POST "http://localhost:8000/api/v0/workflow" \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3NTQ4NzIsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.VeKpHmXeDrUzWuSZQO991xP7caGZcfpj_iGxuk5A3fg" \
  --data "{
	\"data\": {
		\"test\": {
			\"foo\": \"bar\",
			\"lorem\": \"ipsum\",
			\"buzz\": \"fizz\"
		},
		\"test_flatten\": {
			\"ultricies\": {
				\"consectetur\": \"adipiscing\"
			},
			\"dolor\": \"sit\"
		}
	},
	\"steps\": [
		\"Create a foobar\",
		\"Read lorem ipsum\",
		\"Delete buzzfizz\"
	]
}"
```

Response example:

```javascript
{
    "status": "success",
    "data": {
        "workflow": {
            "public_id": "8b087cab-36e0-451e-8fcc-339d68f2970b",
            "status": "inserted",
            "data": {
                "test": {
                    "foo": "bar",
                    "lorem": "ipsum",
                    "buzz": "fizz"
                },
                "test_flatten": {
                    "ultricies": {
                        "consectetur": "adipiscing"
                    },
                    "dolor": "sit"
                }
            },
            "steps": [
                "Create a foobar",
                "Read lorem ipsum",
                "Delete buzzfizz"
            ],
            "created_by": {
                "username": "mdcg",
                "email": "mauro@python.com"
            },
            "produced_by": null
        }
    }
}
```

### List workflows (GET)
`http://localhost:8000/api/v0/workflow`

Request example:

```shell
curl --location --request GET "http://localhost:8000/api/v0/workflow" \
  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3NTQ4NzIsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.VeKpHmXeDrUzWuSZQO991xP7caGZcfpj_iGxuk5A3fg"
```

Response example:

```javascript
{
    "status": "success",
    "data": {
        "workflow": [
            {
                "public_id": "8b087cab-36e0-451e-8fcc-339d68f2970b",
                "status": "inserted",
                "data": {
                    "test": {
                        "foo": "bar",
                        "buzz": "fizz",
                        "lorem": "ipsum"
                    },
                    "test_flatten": {
                        "dolor": "sit",
                        "ultricies": {
                            "consectetur": "adipiscing"
                        }
                    }
                },
                "steps": [
                    "Create a foobar",
                    "Read lorem ipsum",
                    "Delete buzzfizz"
                ],
                "created_by": {
                    "username": "mdcg",
                    "email": "mauro@python.com"
                },
                "produced_by": null
            }
        ],
        "links": {
            "next": null,
            "previous": null
        },
        "count": 1
    }
}
```

### Details of a workflow (GET)
`http://localhost:8000/api/v0/workflow/<workflow_public_id>`

Request example:

```shell
curl --location --request GET "http://localhost:8000/api/v0/workflow/bc6d748d-623c-4fa5-94d6-edcfcaadd7c4" \
  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3MDY0MTEsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.nnhvr-8j4yu5rD7LbukKoSA5K837AV9AjAzBaxIdgjM"
```

Response example:

```javascript
{
    "status": "success",
    "data": {
        "workflow": {
            "public_id": "8b087cab-36e0-451e-8fcc-339d68f2970b",
            "status": "inserted",
            "data": {
                "test": {
                    "foo": "bar",
                    "buzz": "fizz",
                    "lorem": "ipsum"
                },
                "test_flatten": {
                    "dolor": "sit",
                    "ultricies": {
                        "consectetur": "adipiscing"
                    }
                }
            },
            "steps": [
                "Create a foobar",
                "Read lorem ipsum",
                "Delete buzzfizz"
            ],
            "created_by": {
                "username": "mdcg",
                "email": "mauro@python.com"
            },
            "produced_by": null
        }
    }
}
```

### Updating a workflow (PATCH)
`http://localhost:8000/api/v0/workflow/<workflow_public_id>`

Request example:

```shell
curl --location --request PATCH "http://localhost:8000/api/v0/workflow/bc6d748d-623c-4fa5-94d6-edcfcaadd7c4" \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3MDY0MTEsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.nnhvr-8j4yu5rD7LbukKoSA5K837AV9AjAzBaxIdgjM" \
  --data "{
	\"data\": {
		\"bar\": \"foo\",
		\"lorem\": \"ipsum\",
		\"fizz\": \"buzz\"
	},
	\"steps\": [
		\"Create a foobar\",
		\"Read ipsum\",
		\"Delete fizz\"
	]
}"
```

Response example:

```javascript
{
    "status": "success",
    "data": {
        "workflow": {
            "public_id": "8b087cab-36e0-451e-8fcc-339d68f2970b",
            "status": "inserted",
            "data": {
                "bar": "foo",
                "lorem": "ipsum",
                "fizz": "buzz"
            },
            "steps": [
                "Create a foobar",
                "Read ipsum",
                "Delete fizz"
            ],
            "created_by": {
                "username": "mdcg",
                "email": "mauro@python.com"
            },
            "produced_by": null
        }
    }
}
```

### Delete a workflow (DELETE)
`http://localhost:8000/api/v0/workflow/<workflow_public_id>`

Request example:

```shell
curl --location --request DELETE "http://localhost:8000/api/v0/workflow/bc6d748d-623c-4fa5-94d6-edcfcaadd7c4" \
  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3MDY0MTEsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.nnhvr-8j4yu5rD7LbukKoSA5K837AV9AjAzBaxIdgjM"
```

Response example:

```javascript
{
    "status": "success",
    "data": {
        "workflow": {
            "public_id": "8b087cab-36e0-451e-8fcc-339d68f2970b",
            "status": "inserted",
            "data": {
                "bar": "foo",
                "fizz": "buzz",
                "lorem": "ipsum"
            },
            "steps": [
                "Create a foobar",
                "Read ipsum",
                "Delete fizz"
            ],
            "created_by": {
                "username": "mdcg",
                "email": "mauro@python.com"
            },
            "produced_by": null
        }
    }
}
```

If you try to make a request again:

```javascript
{
    "status": "fail",
    "data": null
}
```

### Consume a workflow (POST)
`http://localhost:8000/api/v0/workflow/consume` 

Request example:

```shell
curl --location --request POST "http://localhost:8000/api/v0/workflow/consume" \
  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6Im1kY2ciLCJleHAiOjE1NzI3NTQ4NzIsImVtYWlsIjoibWF1cm9AcHl0aG9uLmNvbSJ9.VeKpHmXeDrUzWuSZQO991xP7caGZcfpj_iGxuk5A3fg"
```

Response example:

```csv
test__foo,test__buzz,test__lorem,test_flatten__dolor,test_flatten__ultricies__consectetur
bar,fizz,ipsum,sit,adipiscing
```

## Testing

To perform automated project testing, you first need to know how to access a container in Docker. If you are unfamiliar, read the session text **Misc => Accessing a Docker Container**. There you will have everything you need to know to perform this function.

Once you have learned how to access it, you will execute the following command in the `src /` folder:

```shell
$ python manage.py test api
```

## Misc

### Accessing a Docker Container

If you need to access the application container to manually perform some migration or anything, use the following commands:

```shell
$ docker ps
```

After executing this command, you will have access to the ID (a hexadecimal string displayed in the first column) and the container name (displayed in the final column). Copy one of the two and run the following command:

```shell
$ docker exec -it <container name or id> sh
```

### Debugging

If you need to debug the application, before adding 'pdb' to your code, run the following command:

```shell
$ docker attach <container name or id>
```

If you don't know how to access the container name or ID, go to **"Misc => Accessing a Docker Container"**.

## Conclusion

Again, I would like to thank Nuveo for the opportunity. Any questions or problems, just contact me. Cya! ;)