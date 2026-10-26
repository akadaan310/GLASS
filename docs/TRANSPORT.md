# Glass continuity and shift-language transport
Status: command grammar and deployment contract.

## Shared command model
Read commands: state(commission), events(commission, after), weight(commission), entity(id), forms(id, profile), source(id).
Write commands: declare-region, declare-transition, append-intent, append-outcome, submit-artifact, publish-unit.
Each write carries commission ID, agent/principal ID, expected cursor, idempotency key, source pins, and lease epoch.
The current CLI implements region/rule/intent/outcome/state/weight/spell; intent IDs provide one-result admission.
Transport adapters add principal authentication, scoped capabilities, lease epochs, and retry-key response caching.

## Proposed address grammar
/glass/v1/commissions/{id}/state
/glass/v1/commissions/{id}/events?after={cursor}
/glass/v1/commissions/{id}/weights/{weight-id}
/glass/v1/atlas/entities/{id}/forms/{profile}
/glass/v1/commissions/{id}/commands/{operation}

GET returns projections and allowed-command descriptions. POST applies authenticated version-bound commands.
PURL and SEURL bridges get separate versioned adapters after inspecting their existing grammars and authority contracts.
The path segments are typed language tokens. A parsed path lowers to a command IR; the same IR drives CLI, HTTP, and MCP projections.

## Proposed MCP tools
glass_state, glass_events, glass_declare, glass_intend, glass_observe, glass_entity, glass_forms, glass_publish.
Tools return cursor, active configuration, artifact references, and pending intents.
A hosted MCP deployment receives an authenticated endpoint and a deployment receipt. Its tool registry exposes these declared capabilities.

## Oracle installation contract
Checkout GLASS/main; build native tools for host architecture; configure a scoped Git credential through the host secret store; preserve private originals under a separate restricted source root.
Choose a stable /srv/glass root with repository, sources, journals, receipts, exports, and tool registry directories.
Install the publisher trigger service and the HTTP/MCP adapter after transport tests.
Record server identity, architecture, source commit, binaries and hashes, service names, endpoint, health observation, and recovery command.
Current server discovery returned an empty connected-server list. The deployment commission awaits the Oracle connection.

## Continuous publication contract
A running watcher queues approved-path changes. A single publisher serializes main integration and writes immutable attempt receipts.
Timer retries use a new receipt ID for each attempt. A queued unit retains its source snapshot and pending main commit.
Remote advancement becomes a reconciliation commission while independent acquisition work can continue.
The supplied native publisher executes one publication attempt; service installation belongs to the deployment commission.
