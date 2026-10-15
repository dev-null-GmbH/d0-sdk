package fixture

import (
	"testing"

	accounting "github.com/dev-null-GmbH/d0-sdk/accounting/go"
)

func TestBothProfilesBalancedDraft(t *testing.T) {
	for _, profile := range []accounting.Profile{accounting.Production, accounting.Test} {
		id, err := Run(profile)
		if err != nil {
			t.Fatalf("%s: %v", profile, err)
		}
		if id != "je_"+suffix {
			t.Fatalf("%s: wrong draft %s", profile, id)
		}
	}
}
