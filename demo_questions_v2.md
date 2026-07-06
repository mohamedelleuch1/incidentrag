# Questions de test — démo IncidentRAG (corpus : eclipse-mosquitto/mosquitto)

À réutiliser Jour 3 (test du prompt) et Jour 4 (démo finale devant jury).

1. Mosquitto client can't connect, getting connection refused
2. Websockets support not available after building from source
3. TLS handshake fails when connecting from Firefox but works in Chrome
4. Broker segfaults after running for a few days
5. High memory usage / OOM error after extended uptime
6. Bridge connection between two brokers keeps disconnecting
7. Unable to open password file / permission denied on password_file
8. Docker container fails to start after upgrading Mosquitto version
9. Client gets disconnected with "exceeded timeout" even though keepalive is respected
10. Retained messages not delivered to new subscribers

## Notes
- Ces questions ont été recoupées avec les vrais titres présents dans incidents_clean.json
  (issues websockets, TLS, segfault, bridge, password_file, docker, etc. sont bien représentées).
- Garder au moins 1 question "difficile" (ex: la 9) où le système doit répondre avec
  une confiance faible s'il ne trouve pas de cas suffisamment similaires.
- Pour la démo, prévoir d'alterner : une question "facile" (résolue clairement dans
  plusieurs issues) et une question plus ambiguë, pour montrer le score de confiance.
