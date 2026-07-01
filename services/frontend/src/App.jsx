import React, { useState, Suspense } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

function UploadForm() {
  const { t } = useTranslation();
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [docId, setDocId] = useState(null);

  const upload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('/v2/documents', formData);
      setDocId(res.data.document_id);
      setStatus(t('upload_success', { id: res.data.document_id, status: res.data.status }));
    } catch (err) {
      setStatus(t('upload_failed', { message: err.message }));
    }
  };

  return (
    <div>
      <h1>{t('title')}</h1>
      <div style={{ marginBottom: 10 }}>
        <input type="file" onChange={e => setFile(e.target.files[0])} />
        <button onClick={upload} disabled={!file}>{t('upload')}</button>
      </div>
      {status && <p>{status}</p>}
    </div>
  );
}

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UploadForm />
    </Suspense>
  );
}

export default App;
