import React, { useState, useEffect } from 'react';
import axios from 'axios';

function RulesEditor() {
  const [rules, setRules] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [conditions, setConditions] = useState([{ field: '', operator: 'eq', value: '' }]);
  const [action, setAction] = useState('manual_review');

  const fetchRules = async () => {
    const res = await axios.get('/api/rules');
    setRules(res.data);
  };

  useEffect(() => { fetchRules(); }, []);

  const addCondition = () => setConditions([...conditions, { field: '', operator: 'eq', value: '' }]);

  const updateCondition = (index, key, value) => {
    const newCond = [...conditions];
    newCond[index][key] = value;
    setConditions(newCond);
  };

  const createRule = async () => {
    await axios.post('/api/rules', { name, description, conditions, action });
    fetchRules();
    setName(''); setDescription(''); setConditions([{ field: '', operator: 'eq', value: '' }]);
  };

  const deleteRule = async (id) => {
    await axios.delete(`/api/rules/${id}`);
    fetchRules();
  };

  return (
    <div>
      <h2>Compliance Rules</h2>
      <div style={{ marginBottom: 10 }}>
        <input placeholder="Rule name" value={name} onChange={e => setName(e.target.value)} />
        <input placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
        {conditions.map((c, i) => (
          <div key={i}>
            <input placeholder="Field" value={c.field} onChange={e => updateCondition(i, 'field', e.target.value)} />
            <select value={c.operator} onChange={e => updateCondition(i, 'operator', e.target.value)}>
              <option value="eq">eq</option><option value="neq">neq</option>
              <option value="gt">gt</option><option value="lt">lt</option>
            </select>
            <input placeholder="Value" value={c.value} onChange={e => updateCondition(i, 'value', e.target.value)} />
          </div>
        ))}
        <button onClick={addCondition}>Add Condition</button>
        <select value={action} onChange={e => setAction(e.target.value)}>
          <option value="approve">Approve</option>
          <option value="reject">Reject</option>
          <option value="manual_review">Manual Review</option>
        </select>
        <button onClick={createRule}>Create Rule</button>
      </div>
      <ul>
        {rules.map(r => (
          <li key={r.id}>
            <b>{r.name}</b> ({r.action})
            <button onClick={() => deleteRule(r.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RulesEditor;
