## GitHub Copilot Chat

- Extension Version: 0.26.7 (prod)
- VS Code: vscode/1.99.3
- OS: Windows

## Network

User Settings:
```json
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 140.82.121.6 (338 ms)
- DNS ipv6 Lookup: Error (249 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (7 ms)
- Electron fetch (configured): timed out after 10 seconds
- Node.js https: HTTP 200 (4883 ms)
- Node.js fetch: timed out after 10 seconds
- Helix fetch: HTTP 200 (2034 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.114.22 (1996 ms)
- DNS ipv6 Lookup: Error (1684 ms): getaddrinfo ENOTFOUND api.individual.githubcopilot.com
- Proxy URL: None (37 ms)
- Electron fetch (configured): HTTP 200 (4396 ms)
- Node.js https: HTTP 200 (4799 ms)
- Node.js fetch: HTTP 200 (973 ms)
- Helix fetch: HTTP 200 (5638 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).