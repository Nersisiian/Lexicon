# Velero Backup & Restore

## Install Velero
```bash
velero install --provider aws --bucket lexicon-backups --secret-file ./credentials-velero
Schedule Backup
Daily backups at 02:00 UTC with 30?day retention.

bash
kubectl apply -f deploy/velero/daily-backup-schedule.yaml
Restore
bash
velero restore create --from-backup daily-backup
Verify
bash
velero backup get
velero restore get
