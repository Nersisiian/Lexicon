{{- define "compliance.image" -}}
{{ .Values.global.imageRegistry }}/{{ .Values.global.imageOwner }}/{{ .Values.global.imageRepo }}/{{ .image }}:{{ .tag }}
{{- end -}}