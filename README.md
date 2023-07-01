# OAuth 2.1

A Python / Flask implementation of [The OAuth 2.1 Authorization Framework](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-08). For demo purposes only.

**Protocol Flow**

The abstract OAuth 2.1 protocol flow and the interaction between the four key roles is summarized by the following sequence diagram.

```mermaid
sequenceDiagram
    autonumber
    Client ->> Resource Owner: Authorization Request
    activate Resource Owner
    Resource Owner -->> Client: Authorization Grant
    deactivate Resource Owner
    
    Client ->> Authorization Server: Authorization Grant
    activate Authorization Server
    Authorization Server -->> Client: Access Token
    deactivate Authorization Server
    
    Client ->> Resource Server: Access Token
    activate Resource Server
    Resource Server -->> Client: Protected Resource
    deactivate Resource Server
```

**Erlaubnis Authorization State Diagram**

```mermaid
stateDiagram-v2
	[*] --> Request
	Request --> Verifing: Exchange Client Params
	Verifing --> Waiting_Approval: Grant Valid
	Verifing --> Unauthorised: Grant Invalid
	Waiting_Approval --> Authorised: Grant Approved
	Waiting_Approval --> Unauthorised: Grant Denied
	Waiting_Approval --> Timed_Out: Grant Unserviced
	Authorised --> Revoked: Grant Revoked
	Revoked --> [*]
	Timed_Out --> [*]
	Unauthorised --> [*]
	Authorised --> [*]
```

**Erlaubnis Database Schema**

```mermaid
erDiagram
    USER {
        string id
        string username
        string password
        datetime created_at 
        datetime updated_at
    }
    
    ROLE {
        integer id
        string name
        string description
    }
    
    CLIENT {
        string id
        string client_name
        string token_endpoint_auth_method
        array grant_types
    }
    
    METADATA {
        string logo_uri
        array contacts
        string policy_uri
        string tos_uri
        string client_uri
    }
    
    CONFIGURATION {
        integer version
        string jwks
        string jwks_uri
        string scope
    }
    
    REGISTRATION_RECORD {
        int id
        foreign_key user_id
        foreign_key client_id
        datetime installation_time
    }
    
    INSTALLATION_RECORD {
        int id
        foreign_key user_id
        foreign_key client_id
        foreign_key configuration
        datetime installation_time
    }
    
    STATE_RECORD {
        foreign_key user_id
        foreign_key client
        string state
    }
    
    USER ||--o{ ROLE : has
    USER ||--o{ CLIENT : registers
    REGISTRATION_RECORD ||--o{ CLIENT : generates
    INSTALLATION_RECORD ||--o{ CLIENT : generates
    STATE_RECORD ||--o{ CLIENT : generates
    USER ||--o{ CLIENT : installs
    CLIENT ||--o{ CONFIGURATION : contains
    CLIENT ||--||METADATA : contains
```

## Quickstart

```shell
cd rfc-oauth
poetry install
export FLASK-APP=run.py
flask run
```