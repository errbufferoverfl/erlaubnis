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
	Waiting_Approval --> Unauthorised: Grant Denyed
	Waiting_Approval --> Timed_Out: Grant Unserviced
	Authorised --> Revoked: Grant Revoked
	Revoked --> [*]
	Timed_Out --> [*]
	Unauthorised --> [*]
	Authorised --> [*]
```





## Quickstart

```shell
cd rfc-oauth
poetry install
export FLASK-APP=run.py
flask run
```