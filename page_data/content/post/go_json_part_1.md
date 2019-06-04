---
title: "Working with JSON in GO - Part 1"
date: 2019-05-15
draft: false
tags:
- go
- golang
- json
---

If you want an easy way to transform Go structure into JSON representation or vice versa you can use json tags for straightforward transformation or implement one simple method to gain more controll over the process.
<!--more-->


#### Introduction

Changing JSON into structures or structures into JSON is (at least for me) very frequent task and thus it should be relatively easy. Below you can see two most commonly used ways to transform structures to and from JSON.






#### Marshall (basic)

Simplest case of marshalling is to transform Go structure into JSON with identical (or similar) structure. In such case we can use JSON tags which give us limited controll over the transformation. 

For presentation purposes I've used `bts, err := json.MarshalIndent(user, "", "\t")` but in 'production' code probably `bts, err := json.Marshal(user)` would be better.

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
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v",
		u.FirstName, u.LastName, u.Married)
}

func main() {

	jsonBytes := []byte(`{
				"firstName": "John",
				"lastName":  "Smith",
				"married":   false}
			`)

	user := new(User)
	if err := json.Unmarshal(jsonBytes, user); err != nil {
		panic(err)
	}

	fmt.Println(user)
}
```

Output:

```
{
	"firstName": "John",
	"lastName": "Smith",
	"married": false
}
```



#### Unmarshall (basic)

Reverse operation to the one presented above is unmarshalling. In this case we can also use JSON tags to affect the transformation

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
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v",
		u.FirstName, u.LastName, u.Married)
}

func main() {

	jsonBytes := []byte(`{
				"firstName": "John",
				"lastName":  "Smith",
				"married":   false
			}`)

	user := new(User)
	if err := json.Unmarshal(jsonBytes, user); err != nil {
		panic(err)
	}

	fmt.Println(user)
}
```

Output

```
FirstName: John, LastName: Smith, Married: false
```


#### Marshall

If we need more controll over the transformation we can implement simple method in our model. In case of marshalling we need to add `MarshalJSON() ([]byte, error)`. 


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
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v",
		u.FirstName, u.LastName, u.Married)
}

func main() {
	user := &User{
		FirstName: "John",
		LastName:  "Smith",
		Married:   true,
	}

	bts, err := json.MarshalIndent(user, "", "\t")
	if err != nil {
		panic(err)
	}

	fmt.Println(string(bts))
}
```

Output:

```
{
	"firstName": "John",
	"lastName": "Smith",
	"married": "Yes"
}
```




#### Unmarshall

If we want to reverse the process from the example presented above we need to implement `UnmarshalJSON(data []byte) error` method.

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
	if strings.TrimSpace(strings.ToLower(instance.Married)) == "yes" {
		married = true
	}

	u.FirstName = instance.FirstName
	u.LastName = instance.LastName
	u.Married = married

	return nil
}

func (u *User) String() string {
	return fmt.Sprintf("FirstName: %v, LastName: %v, Married: %v",
		u.FirstName, u.LastName, u.Married)
}

func main() {
	jsonBytes := []byte(`{
				"firstName":"John",
				"lastName":"Smith",
				"married":"Yes"
			}`)

	user := new(User)
	if err := json.Unmarshal(jsonBytes, user); err != nil {
		panic(err)
	}

	fmt.Println(user)
}
```

Output:

```
FirstName: John, LastName: Smith, Married: true
```




#### Summary

Yes I know the code is definitly not the shortes example of JSON marshallig / unmarshalling but it has other advantages like full controll over the process. 



#### Sources
1. [Go programming language](https://golang.org/)
2. [JSON package - documentation](https://golang.org/pkg/encoding/json/)
3. [Run the code in Go playground](https://play.golang.org/)
   