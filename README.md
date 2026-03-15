# diagpack-can
DiagPack CAN est une toolbox Linux/SocketCAN qui permet d’observer, rejouer et stresser le bus CAN d’un prototype afin de révéler rapidement les limites de robustesse et d’observabilité du firmware.  Elle sert à :  capturer les échanges CAN  rejouer des scénarios  injecter des perturbations  produire des logs exploitables

Elle sert à :
- capturer les échanges CAN
- rejouer des scénarios
- injecter des perturbations
- produire des logs exploitables

Le but est de mettre en évidence ce que le firmware ne dit pas :
- erreurs silencieuses
- absence de diagnostics
- manque de compteurs
- gestion d’erreurs incohérente
- watchdog inefficace
- comportement non déterministe
