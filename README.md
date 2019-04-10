# Work Time Management service 

This README.md assumes that you have already installed the go compiler, if you didn't, please, refer to: https://golang.org/doc/install

## Files:

### serviceWTM.go:
back-end goLang script
### serviceWTM_test.go:
test script which checks whether or not url's hadnlers in service script are working properly

## Building

In development environment run `go run serviceWTM.go -dev`.

But if you need an executable file for some reasons, you can start with `go build` and then `./worktimemanagement -dev`(again: use -dev flag for launching service using development environment config)

## Flags for running the service

For info about flags run `go run serviceWTM.go -h`

## Test

Run `go test` in a service directory to start testing the service, the results and mistakes(if there were any) will be shown in the same terminal you've launched the command.


## Troubleshooting

This service must be allocated in a GOPATH folder to work properly.
If you recieve message that your gopath is missing some of the packages which are needed in order to launch server/test then open terminal in the service folder and type `go get ./`

----
(All of the commands are for linux terminal)

# API FAQ

## Database configuration

To service work properly, you need to build database in a `/dbscripts/db-wtm` directory using local Dockerfile, additional info could be found there in a README.md file.

### Note: if you have any errors, check for these things: 
- **If you have a mariadb image in your docker by running `docker image ls | grep mariadb` command**

- **If you have a mariadb containter launched before (they you need to just start it by running `docker start mariadb`(or any other name of the container which is refered to current version of db-wtm database)**

- **Do you have rights to run docker without using sudo, if not - run it with sudo, or add your user to local docker group(you can find guides on the Internet)**

- **Note: the service will load and execute script which will fill database with test data, no further actions are required. The service will notify if everything is done right or not.**


## Requests 

### All requests bodies are raw JSON(application/json)

---
## GET requests:

### wtmgmt/activities/

### Request url:

`GET: wtmgmt/activities/*user_id*` - get all activities that are created by user who has id of *user_id*

### Response:

>>>
```
[
    {
        "ActivityID": 3,
        "Date": "2018-10-22",
        "ProjectID": 1,
        "StartTime": "13:32:00",
        "EndTime": "15:12:00",
        "Payment": 342,
        "Description": "Decide what to do"
    },
    {
        "ActivityID": 4,
        "Date": "2018-10-23",
        "ProjectID": 1,
        "StartTime": "14:04:00",
        "EndTime": "19:03:00",
        "Payment": 427,
        "Description": "Do what I've decided to do"
    },
    ...
]

```
>>>


### wtmgmt/activitiesToday/

### Request url:

`GET: wtmgmt/activitiesDate/?=*user_id*&Date=*date*` - get activities that are created today by user who has id of *user_id*.

### Note that here JSON will not return data as in previous response.

### Example of request: wtmgmt/activitiesDate/?id=2&Date=2018-10-22

### Response:

>>>
```
[
    {
        "ActivityID":21,
        "ProjectID":3,
        "StartTime":"17:21:00",
        "EndTime":"21:40:00",
        "Payment":0,
        "Description":"Write awesome RESTAPI in Go"
    },
    ...
]

```
>>>

### /test

### Request url:

`GET: /test` - just a test page which returns 200 code and nothing else, might be helpful for testing the connection to service.

---

---
## POST request:

### wtmgmt/POST

### Request url:

`POST: wtmgmt/POST`

### Desired request JSON structure:

>>>
```
[
    {
	"AccountID":2,
	"Date":"2018-11-27", 
	"ProjectID":3,
	"StartTime":"17:21",
	"EndTime":"21:40",
	"Payment":0,
	"Description":"Check if RESTAPI is working"
    }
]

```
>>>
---








