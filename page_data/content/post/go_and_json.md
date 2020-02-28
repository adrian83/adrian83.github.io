---
title: Go (Golang) and JSON   
date: 2020-01-16
draft: true
categories:
- Go
- JSON
tags:
- Go
- JSON
---

Below you can find four examples of how to work with JSON in Go.

1. Marshaling Go structures into JSON when coresponding fields have compatible types 
2. Unmarshaling JSON into Go structures when coresponding fields have compatible types
3. Marshaling Go structures into JSON with custom marshaling implementation 
4. Unmarshaling JSON into Go structures with custom unmarshaling implementation 

<br/>

---  

<br/>

- ad 1. If both JSON and Go structures can be easily mapped to eachother such implementation of marshaling should sufice. 

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

<br/>

---  

<br/>

- ad 2. If both JSON and Go structures can be easily mapped to eachother such implementation of unmarshaling should sufice. 

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

<br/>

---  

<br/>

- ad 3. If custom transformation is needed between Go structures and JSON, implementing `MarshalJSON() ([]byte, error)` should be helpful. 

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

<br/>

---  

<br/>

- ad 4. If custom transformation is needed between JSON and Go structures, implementing `UnmarshalJSON(data []byte) error` should be helpful. 

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