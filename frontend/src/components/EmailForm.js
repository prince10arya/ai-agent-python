import React from 'react';
import { useEmailStore } from '../store/useEmailStore';
import { useEmail } from '../hooks/useEmail';
import '../styles/EmailForm.css';

const EmailForm = () => {
  const store = useEmailStore();
  const { handleDraft, handleSend, handleSpeak } = useEmail();

  return (
    <div className="email-form">
      <h2>✉️ Compose Email</h2>
      <form onSubmit={handleSend}>
        <div className="form-group">
          <label htmlFor="recipient">Recipient Email:</label>
          <input
            type="email"
            id="recipient"
            value={store.recipient}
            onChange={(e) => {
              store.setRecipient(e.target.value);
              store.setEmailValid(!e.target.value || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.target.value));
            }}
            placeholder="Enter recipient email address"
            required
          />
          {store.recipient && !store.emailValid && (
            <small>⚠️ Please enter a valid email address</small>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="tone">Tone:</label>
          <select
            id="tone"
            value={store.tone}
            onChange={(e) => store.setTone(e.target.value)}
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
            value={store.prompt}
            onChange={(e) => store.setPrompt(e.target.value)}
            placeholder="Describe what you want to write about..."
            required
          />
        </div>

        <div className="button-group">
          <button type="button" className="btn btn-secondary" onClick={handleDraft} disabled={store.loading}>
            {store.loading ? '⏳ Generating...' : '📝 Generate Draft'}
          </button>
          <button type="submit" className="btn btn-primary" disabled={store.loading}>
            {store.loading ? '⏳ Sending...' : '🚀 Send Email'}
          </button>
        </div>
      </form>

      {store.draft && (
        <div className="draft-preview">
          <h3>✨ Generated Draft (Editable)</h3>
          <div className="form-group">
            <label htmlFor="editSubject">Subject:</label>
            <input
              type="text"
              id="editSubject"
              value={store.editedSubject}
              onChange={(e) => store.setEditedSubject(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="editContent">Content:</label>
            <textarea
              id="editContent"
              value={store.editedContent}
              onChange={(e) => store.setEditedContent(e.target.value)}
            />
          </div>
          <button
            type="button"
            className="btn listen-btn"
            onClick={handleSpeak}
            disabled={store.isSpeaking}
          >
            {store.isSpeaking ? '🔊 Speaking...' : '🔊 Listen to Draft'}
          </button>
        </div>
      )}
    </div>
  );
};

export default EmailForm;
