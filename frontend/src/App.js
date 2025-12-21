import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api';

function App() {
  const [recipient, setRecipient] = useState('');
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [emailHistory, setEmailHistory] = useState([]);
  const [draft, setDraft] = useState(null);
  const [editedSubject, setEditedSubject] = useState('');
  const [editedContent, setEditedContent] = useState('');
  const [emailValid, setEmailValid] = useState(true);
  const [tone, setTone] = useState('professional');
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [bulkRecipients, setBulkRecipients] = useState('');
  const [showBulk, setShowBulk] = useState(false);

  useEffect(() => {
    fetchEmailHistory();
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/templates/`);
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  const handleTemplateSelect = (e) => {
    const templateId = e.target.value;
    setSelectedTemplate(templateId);
    if (templateId) {
      const template = templates.find(t => t.id === parseInt(templateId));
      if (template) {
        setPrompt(template.content);
        setEditedSubject(template.subject);
      }
    }
  };

  const fetchEmailHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/emails/history`);
      setEmailHistory(response.data);
    } catch (error) {
      console.error('Error fetching email history:', error);
    }
  };

  const showMessage = (text, type) => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => {
      setMessage('');
      setMessageType('');
    }, 5000);
  };

  const handleDraft = async (e) => {
    e.preventDefault();
    if (!recipient.trim() || !prompt.trim()) {
      showMessage('Please fill in both recipient and prompt fields', 'error');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(recipient)) {
      showMessage('Please enter a valid email address', 'error');
      return;
    }
    if (prompt.trim().length < 10) {
      showMessage('Prompt must be at least 10 characters', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/emails/draft`, {
        recipient,
        prompt,
        tone
      });
      setDraft(response.data);
      setEditedSubject(response.data.subject);
      setEditedContent(response.data.content);
      showMessage('Draft generated successfully!', 'success');
    } catch (error) {
      showMessage('Error generating draft: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!recipient.trim() || (!prompt.trim() && !draft)) {
      showMessage('Please fill in both recipient and prompt fields', 'error');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(recipient)) {
      showMessage('Please enter a valid email address', 'error');
      return;
    }
    if (!draft && prompt.trim().length < 10) {
      showMessage('Prompt must be at least 10 characters', 'error');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        draft ? `${API_BASE_URL}/emails/send-draft` : `${API_BASE_URL}/emails/send`,
        draft ? { recipient, subject: editedSubject, content: editedContent } : { recipient, prompt, tone }
      );
      showMessage(`Email sent successfully to ${response.data.recipient}!`, 'success');
      setRecipient('');
      setPrompt('');
      setDraft(null);
      fetchEmailHistory();
    } catch (error) {
      showMessage('Error sending email: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="container">
      <div className="header">
        <h1>🤖 AI Email Agent</h1>
        <p>Draft and send emails with AI assistance</p>
      </div>

      {message && (
        <div className={messageType === 'error' ? 'error' : 'success'}>
          {message}
        </div>
      )}

      <div className="email-form">
        <h2>Compose Email</h2>
        <form onSubmit={handleSend}>
          <div className="form-group">
            <label htmlFor="recipient">Recipient Email:</label>
            <input
              type="email"
              id="recipient"
              value={recipient}
              onChange={(e) => {
                setRecipient(e.target.value);
                setEmailValid(!e.target.value || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.target.value));
              }}
              placeholder="Enter recipient email address"
              required
              style={{ borderColor: recipient && !emailValid ? '#fa709a' : '' }}
            />
            {recipient && !emailValid && (
              <small style={{ color: '#fa709a', fontSize: '13px', marginTop: '5px', display: 'block' }}>
                ⚠️ Please enter a valid email address
              </small>
            )}
          </div>
          
          <div className="form-group">
            <label htmlFor="template">Template (Optional):</label>
            <select
              id="template"
              value={selectedTemplate}
              onChange={handleTemplateSelect}
              style={{ padding: '10px 14px', background: '#0f1419', border: '1px solid #2d3748', borderRadius: '6px', fontSize: '14px', color: '#e6e8eb', width: '100%' }}
            >
              <option value="">-- Select Template --</option>
              {templates.map(t => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="tone">Tone:</label>
            <select
              id="tone"
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              style={{ padding: '10px 14px', background: '#0f1419', border: '1px solid #2d3748', borderRadius: '6px', fontSize: '14px', color: '#e6e8eb', width: '100%' }}
            >
              <option value="professional">Professional</option>
              <option value="casual">Casual</option>
              <option value="friendly">Friendly</option>
              <option value="formal">Formal</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="prompt">Email Prompt:</label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe what you want to write about..."
              required
            />
          </div>

          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={showBulk}
                onChange={(e) => setShowBulk(e.target.checked)}
                style={{ marginRight: '8px' }}
              />
              Send to multiple recipients
            </label>
          </div>

          {showBulk && (
            <div className="form-group">
              <label htmlFor="bulkRecipients">Recipients (comma-separated):</label>
              <textarea
                id="bulkRecipients"
                value={bulkRecipients}
                onChange={(e) => setBulkRecipients(e.target.value)}
                placeholder="email1@example.com, email2@example.com"
                style={{ height: '80px' }}
              />
            </div>
          )}

          <div className="button-group">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={handleDraft}
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate Draft'}
            </button>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Send Email'}
            </button>
          </div>
        </form>

        {draft && (
          <div style={{ marginTop: '20px' }}>
            <h3>Generated Draft (Editable):</h3>
            <div className="form-group">
              <label htmlFor="editSubject">Subject:</label>
              <input
                type="text"
                id="editSubject"
                value={editedSubject}
                onChange={(e) => setEditedSubject(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="editContent">Content:</label>
              <textarea
                id="editContent"
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
                style={{ height: '200px' }}
              />
            </div>
          </div>
        )}
      </div>

      <div className="email-history">
        <h2>Email History</h2>
        {emailHistory.length === 0 ? (
          <div className="loading">No emails sent yet</div>
        ) : (
          emailHistory.map((email) => (
            <div key={email.id} className="email-item">
              <div className="email-header">
                <div className="email-subject">{email.subject}</div>
                <div className={`email-status status-${email.status}`}>
                  {email.status.toUpperCase()}
                </div>
              </div>
              <div className="email-meta">
                To: {email.recipient} | {formatDate(email.created_at)}
              </div>
              <div className="email-content">
                <strong>Prompt:</strong> {email.prompt}
                <br /><br />
                <strong>Content:</strong><br />
                {email.content}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;