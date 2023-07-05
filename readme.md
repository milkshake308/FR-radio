## Contexte
Une demande a été faite pour que l’on établisse notre système de gestion audio propre dont voici le cahier de charge résumé :
- Qu’il y ait une lecture automatisée et continue d’une webradio.
- L’URL du flux puisse être modifiée à distance.
- La planification horaire puisse être modifiée à distance.
- La lecture puisse être lancée/arrêtée à distance.
- Que la solution puisse reprendre automatiquement après une panne de courant.
- Que si le matériel échoue, on puisse redéployer une instance de la solution rapidement.

## API
Entre autres, le programme dispose d'une API HTTP rudimentaire permettant :

- `GET /start`
  - Description: Démarre la lecture du lecteur vidéo en cours.
  - Retourne: "Lecture démarrée."

- `GET /stop`
  - Description: Arrête la lecture du lecteur vidéo en cours.
  - Retourne: "Lecture arrêtée."

- `GET /status`
  - Description: Vérifie l'état du lecteur vidéo.
  - Retourne: "Lecteur actif" si la lecture est en cours, sinon "Lecteur arrêté."

- `GET /url`
  - Description: Obtient l'URL du flux audio configuré.
  - Retourne: L'URL du flux audio.

- `POST /url`
  - Description: Met à jour l'URL du flux audio avec le paramètre new_url.
  - Paramètres:
    - new_url: Nouvelle URL du flux audio à configurer.
  - Retourne: "URL mise à jour."

- `GET /schedule`
  - Description: Obtient la programmation horaire configurée.
  - Retourne: La programmation horaire au format JSON.

- `POST /schedule`
  - Description: Met à jour la programmation horaire avec le paramètre schedule.
  - Paramètres:
    - schedule: Nouvelle programmation horaire à configurer au format JSON.
  - Retourne: "Programmation horaire mise à jour."
