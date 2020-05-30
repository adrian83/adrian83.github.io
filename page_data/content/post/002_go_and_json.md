---
title: Go and JSON   
date: 2020-01-16
draft: false
categories:
- Go
- JSON
tags:
- Go
- JSON
---


### Transforming data structures into JSON and the other way around is something, that is done quite often when creating APIs. Below you can find a few, in my opinion, most frequent transformations to and from JSON written in Go programming language.

#### Introduction

In this post we will see, how to marshal and unmarshal JSON into Go structures. We will see two most common cases where JSON and Go structures have compatible types and when the transformation is done by implementing custom logic.

#### I. JSON and Go structures are similar and can be mapped without any additional manipulations.

##### 1. Marshaling Go structures into JSON, when corresponding fields have compatible types.


```
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type User struct {
	Name      string    `json:"name"`
	BirthDate time.Time `json:"birthDate"`
}

func main() {

	user := User{
		Name:      "John",
		BirthDate: time.Date(1993, time.November, 4, 23, 0, 0, 0, time.UTC),
	}

	bts, err := json.Marshal(&user)
	if err != nil {
		panic(err)
	}

	fmt.Println(string(bts))
}
```

Output:
```
{"name":"John","birthDate":"1993-11-04T23:00:00Z"}
```


##### 2. Unmarshalling JSON into Go structures, when corresponding fields have compatible types.

```
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type User struct {
	Name      string    `json:"name"`
	BirthDate time.Time `json:"birthDate"`
}

func main() {

	jsonBts := []byte(`{"name":"John","birthDate":"1993-11-04T23:00:00Z"}`)

	var user User
	if err := json.Unmarshal(jsonBts, &user); err != nil {
		panic(err)
	}

	fmt.Println(user)
}
```

Output: 
```
{John 1993-11-04 23:00:00 +0000 UTC}
```

#### II. JSON and Go structures are incompatible and transformation code needs to be implemented..

A bit more complex case is, when we have two incompatible sides of transformation. Fortunately, we can implement our custom marshalling / unmarshalling by adding functions `MarshalJSON() ([]byte, error)` and `UnmarshalJSON(data []byte) error` to Go structure.


##### 1. Marshalling Go structures into JSON with custom implementation.

```
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

const dateLayout = "2006-01-02"

type User struct {
	Name      string    `json:"name"`
	BirthDate time.Time `json:"birthDate"`
}

func (u *User) MarshalJSON() ([]byte, error) {

	userRepr := struct {
		Name      string `json:"name"`
		BirthDate string `json:"birthDate"`
	}{
		Name:      u.Name,
		BirthDate: u.BirthDate.Format(dateLayout),
	}

	return json.Marshal(&userRepr)
}

func main() {

	user := User{
		Name:      "John",
		BirthDate: time.Date(1993, time.November, 4, 23, 0, 0, 0, time.UTC),
	}

	bts, err := json.Marshal(&user)
	if err != nil {
		panic(err)
	}

	fmt.Println(string(bts))
}
```

Output:
```
{"name":"John","birthDate":"1993-11-04"}
```



##### 2. Unmarshalling JSON into Go structures with custom implementation.

```
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

const dateLayout = "2006-01-02"

type User struct {
	Name      string    `json:"name"`
	BirthDate time.Time `json:"birthDate"`
}

func (u *User) UnmarshalJSON(data []byte) error {

	type userRepr struct {
		Name      string `json:"name"`
		BirthDate string `json:"birthDate"`
	}

	var user userRepr

	if err := json.Unmarshal(data, &user); err != nil {
		return err
	}

	t, err := time.Parse(dateLayout, user.BirthDate)
	if err != nil {
		return err
	}

	u.Name = user.Name
	u.BirthDate = t

	return nil
}

func main() {

	jsonBts := []byte(`{"name":"John","birthDate":"1993-11-04"}`)

	var user User

	if err := json.Unmarshal(jsonBts, &user); err != nil {
		panic(err)
	}

	fmt.Println(user)
}
```

Output:
```
{John 1993-11-04 00:00:00 +0000 UTC}
```