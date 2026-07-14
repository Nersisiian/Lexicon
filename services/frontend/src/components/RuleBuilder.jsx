import React, { useState } from 'react';
import axios from 'axios';

function RuleBuilder() {
  const [name, setName] = useState('');
  const [field, setField] = useState('');
  const [operator, setOperator] = useState('eq');
  const [value, setValue] = useState('');
  const [action, setAction] = useState('manual_review');
  const [rules, setRules] = useState([]);

  const fetchRules = async () => {
    const res = await axios.get('/api/rules');
    setRules(res.data);
  };

  React.useEffect(() => { fetchRules(); }, []);

  const addRule = async () => {
    await axios.post('/api/rules', {
      name,
      conditions: [{ field, operator, value }],
      action,
      description: ''
    });
    fetchRules();
    setName(''); setField(''); setValue('');
  };

  return (
    <div>
      <h2>Rule Builder</h2>
      <input placeholder="Rule name" value={name} onChange={e => setName(e.target.value)} />
      <input placeholder="Field" value={field} onChange={e => setField(e.target.value)} />
      <select value={operator} onChange={e => setOperator(e.target.value)}>
        <option value="eq">=</option>
        <option value="neq">!=</option>
        <option value="gt">&gt;</option>
        <option value="lt">&lt;</option>
      </select>
      <input placeholder="Value" value={value} onChange={e => setValue(e.target.value)} />
      <select value={action} onChange={e => setAction(e.target.value)}>
        <option value="approve">Approve</option>
        <option value="reject">Reject</option>
        <option value="manual_review">Manual Review</option>
      </select>
      <button onClick={addRule}>Add Rule</button>
      <ul>
        {rules.map(r => (
          <li key={r.id}><b>{r.name}</b>: {r.conditions[0]?.field} {r.conditions[0]?.operator} {r.conditions[0]?.value} > {r.action}</li>
        ))}
      </ul>
    </div>
  );
}

export default RuleBuilder;
