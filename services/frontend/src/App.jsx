import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [docId, setDocId] = useState(null);

  const upload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('/v2/documents', formData);
      setDocId(res.data.document_id);
      setStatus(`Document ${res.data.document_id} uploaded with status ${res.data.status}`);
    } catch (err) {
      setStatus(`Upload failed: ${err.message}`);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: 20 }}>
      <h1>Lexicon Compliance Platform</h1>
      <div style={{ marginBottom: 10 }}>
        <input type="file" onChange={e => setFile(e.target.files[0])} />
        <button onClick={upload} disabled={!file}>Upload</button>
          <RulesEditor />\n  </div>
      {status && <p>{status}</p>}
        <RulesEditor />\n  </div>
  );
}

export default App;
