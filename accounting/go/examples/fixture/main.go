package main

import (
	"fmt"
	"log"

	accounting "github.com/dev-null-GmbH/d0-sdk/accounting/go"
	"github.com/dev-null-GmbH/d0-sdk/accounting/go/fixture"
)

func main() {
	for _, profile := range []accounting.Profile{accounting.Production, accounting.Test} {
		id, err := fixture.Run(profile)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%s: balanced unposted draft %s\n", profile, id)
	}
}
