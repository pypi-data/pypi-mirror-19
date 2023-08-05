{{ header }}

package {{ name }}

import (
    "github.com/nuagenetworks/go-bambou/bambou"
    "fmt"
    "strings"
)

var (
    _URLPostfix string
)

// Returns a new Session
func NewSession(username, password, organization, url string) (*bambou.Session, *{{root_api|capitalize}}) {

    root := New{{root_api|capitalize}}()
    url += _URLPostfix

    session := bambou.NewSession(username, password, organization, url, root)

    return session, root
}

func init() {

    _URLPostfix = "/" + SDKAPIPrefix + "/v" + strings.Replace(fmt.Sprintf("%.1f", SDKAPIVersion), ".", "_", 100)
}
