---
title: "Custom JSON Marshalling and Unmarshalling in Go"
date: 2019-05-15
draft: true
tags:
- go
- golang
- json
---

If you want an easy way to transform Go structure into JSON representation or vice versa you can take advantage of json or implementthat will give you better controll over the transformation.
<!--more-->


#### Introduction

Changing JSON into structures or structures into JSON is (at least for me) very frequent task and thus it should be relatively easy.  Let's check how those tasks can be achieved in Go.

// All redundant data will be skipt and all properties that do not have their responding data in JSON will have default values.
// In most cases using json tags is what you want to do


#### Unmarshall (basic)

In example presented below JSON is directly translated into Go structure.

```
package main

import (
	"encoding/json"
	"fmt"
)

type User struct {
	FirstName string `json:"firstName"`
	LastName  string `json:"lastName"`
	Married   bool   `json:"married"`
}

func (u *User) String() string {
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v", u.FirstName, u.LastName, u.Married)
}

func main() {

	jsonStr := "{\"firstName\":\"John\",\"lastName\":\"Smith\",\"married\":false}"
	jsonBytes := []byte(jsonStr)

	user := new(User)
	if err := json.Unmarshal(jsonBytes, user); err != nil {
		panic(err)
	}

	fmt.Println(user)
}
```



#### Marshall (basic)

In example presented below Go structure is directly translated into JSON.

```
package main

import (
	"encoding/json"
	"fmt"
)

type User struct {
	FirstName string `json:"firstName"`
	LastName  string `json:"lastName"`
	Married   bool   `json:"married"`
}

func (u *User) String() string {
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v", u.FirstName, u.LastName, u.Married)
}

func main() {
	user := &User{
		FirstName: "John",
		LastName:  "Smith",
		Married:   false,
	}

	bts, err := json.Marshal(user)
	if err != nil {
		panic(err)
	}

	fmt.Println(string(bts))
}

```



#### Unmarshall
```
package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

type User struct {
	FirstName string `json:"firstName"`
	LastName  string `json:"lastName"`
	Married   bool   `json:"married"`
}

func (u *User) UnmarshalJSON(data []byte) error {

	type tmpStruct struct {
		FirstName string `json:"firstName"`
		LastName  string `json:"lastName"`
		Married   string `json:"married"`
	}

	instance := new(tmpStruct)
	if err := json.Unmarshal(data, instance); err != nil {
		return err
	}

	var married bool
	if strings.TrimSpace(strings.ToLower(instance.Married)) == "true" {
		married = true
	}

	u.FirstName = instance.FirstName
	u.LastName = instance.LastName
	u.Married = married

	return nil
}

func (u *User) String() string {
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v", u.FirstName, u.LastName, u.Married)
}

func main() {
	jsonStr := "{\"firstName\":\"John\",\"lastName\":\"Smith\",\"married\":\"true\"}"
	jsonBytes := []byte(jsonStr)

	user := new(User)
	if err := json.Unmarshal(jsonBytes, user); err != nil {
		panic(err)
	}

	fmt.Println(user)
}
```



#### Marshall

```
package main

import (
	"encoding/json"
	"fmt"
)

type User struct {
	FirstName string `json:"firstName"`
	LastName  string `json:"lastName"`
	Married   bool   `json:"married"`
}

func (u *User) MarshalJSON() ([]byte, error) {
	type tmpStruct struct {
		FirstName string `json:"firstName"`
		LastName  string `json:"lastName"`
		Married   string `json:"married"`
	}

	married := "No"
	if u.Married {
		married = "Yes"
	}

	instance := tmpStruct{
		FirstName: u.FirstName,
		LastName:  u.LastName,
		Married:   married,
	}

	return json.Marshal(instance)
}

func (u *User) String() string {
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v", u.FirstName, u.LastName, u.Married)
}

func main() {
	user := &User{
		FirstName: "John",
		LastName:  "Smith",
		Married:   true,
	}

	bts, err := json.Marshal(user)
	if err != nil {
		panic(err)
	}

	fmt.Println(string(bts))
}
```



#### Summary

Building infrastructure is not an easy task. Keeping it as a code is a first and very importants step. Code presented above is just a very basic example of how you can create infrastructure in AWS. Beside that it will help you to keep your resouces and money under controll 



#### Sources
1. [Working with stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html)
2. [Using Amazon CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
3. [Boto 3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
