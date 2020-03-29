---
title: Go (Golang) and JSON   
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


##### The simplest cases are, when JSON and Go structures are very similar and can be mapped without any additional manipulations.


###### Marshaling Go structures into JSON, when corresponding fields have compatible types.


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


###### Unmarshalling JSON into Go structures, when corresponding fields have compatible types.

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

##### A bit more complex case is, when we have two incompatibe sides of transformation. Fortunately, we can implement our custom marshalling / unmarshalling by adding functions `MarshalJSON() ([]byte, error)` and `UnmarshalJSON(data []byte) error` to Go structure.



###### Marshalling Go structures into JSON with custom implementation.

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



###### Unmarshalling JSON into Go structures with custom implementation.

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